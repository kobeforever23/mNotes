from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
import json
from pathlib import Path
from typing import Any

from stress_wizard.governance.models import (
    ApprovalRule,
    ApprovalDecision,
    ApprovalRequest,
    ApprovalResponse,
    GovernanceEvent,
    ReviewerAssignment,
    ReviewerRole,
    ScenarioState,
)
from stress_wizard.governance.rules import evaluate_approval_request


_ALLOWED_TRANSITIONS: dict[ScenarioState, set[ScenarioState]] = {
    ScenarioState.DRAFT: {ScenarioState.SUBMITTED, ScenarioState.ARCHIVED},
    ScenarioState.SUBMITTED: {ScenarioState.UNDER_REVIEW, ScenarioState.WITHDRAWN},
    ScenarioState.UNDER_REVIEW: {
        ScenarioState.CHANGES_REQUESTED,
        ScenarioState.APPROVED,
        ScenarioState.REJECTED,
        ScenarioState.WITHDRAWN,
        ScenarioState.COMPLIANCE_HOLD,
    },
    ScenarioState.CHANGES_REQUESTED: {ScenarioState.REVISED, ScenarioState.ARCHIVED},
    ScenarioState.REVISED: {ScenarioState.SUBMITTED, ScenarioState.ARCHIVED},
    ScenarioState.APPROVED: {ScenarioState.PUBLISHED, ScenarioState.ARCHIVED, ScenarioState.DRAFT},
    ScenarioState.PUBLISHED: {ScenarioState.ARCHIVED, ScenarioState.DRAFT},
    ScenarioState.REJECTED: {ScenarioState.REVISED, ScenarioState.ARCHIVED},
    ScenarioState.WITHDRAWN: {ScenarioState.REVISED, ScenarioState.ARCHIVED},
    ScenarioState.COMPLIANCE_HOLD: {ScenarioState.UNDER_REVIEW, ScenarioState.ARCHIVED},
    ScenarioState.ARCHIVED: set(),
}


class GovernanceWorkflow:
    """Lifecycle state machine + approval tracking for scenarios."""

    def __init__(self, storage_root: str | Path) -> None:
        self.storage_root = Path(storage_root)
        self.storage_root.mkdir(parents=True, exist_ok=True)

    def _scenario_dir(self, scenario_id: str) -> Path:
        path = self.storage_root / scenario_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _state_file(self, scenario_id: str) -> Path:
        return self._scenario_dir(scenario_id) / "approval_status.json"

    def _events_file(self, scenario_id: str) -> Path:
        return self._scenario_dir(scenario_id) / "events.jsonl"

    def init_state(self, scenario_id: str, actor: str) -> None:
        file = self._state_file(scenario_id)
        if file.exists():
            return
        payload = {
            "scenario_id": scenario_id,
            "state": ScenarioState.DRAFT.value,
            "version": 1,
            "locked": False,
            "approval_request": None,
            "updated_at": datetime.now().isoformat(),
            "updated_by": actor,
        }
        file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load_state(self, scenario_id: str) -> dict[str, Any]:
        file = self._state_file(scenario_id)
        if not file.exists():
            self.init_state(scenario_id, actor="system")
        return json.loads(self._state_file(scenario_id).read_text(encoding="utf-8"))

    def save_state(self, scenario_id: str, state: dict[str, Any]) -> None:
        self._state_file(scenario_id).write_text(json.dumps(state, indent=2), encoding="utf-8")

    def _log_event(self, event: GovernanceEvent) -> None:
        with self._events_file(event.scenario_id).open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event.as_dict()) + "\n")

    def _transition(self, scenario_id: str, actor: str, to_state: ScenarioState, details: dict[str, Any] | None = None) -> dict[str, Any]:
        state = self.load_state(scenario_id)
        from_state = ScenarioState(state["state"])
        if to_state not in _ALLOWED_TRANSITIONS.get(from_state, set()):
            raise RuntimeError(f"Invalid transition: {from_state.value} -> {to_state.value}")

        state["state"] = to_state.value
        state["updated_at"] = datetime.now().isoformat()
        state["updated_by"] = actor
        state["locked"] = to_state in {ScenarioState.SUBMITTED, ScenarioState.UNDER_REVIEW, ScenarioState.APPROVED, ScenarioState.PUBLISHED}
        if to_state == ScenarioState.REVISED:
            state["locked"] = False
            state["version"] = int(state.get("version", 1)) + 1
        if to_state == ScenarioState.DRAFT:
            state["locked"] = False

        self.save_state(scenario_id, state)
        self._log_event(
            GovernanceEvent(
                scenario_id=scenario_id,
                actor=actor,
                action="transition",
                from_state=from_state,
                to_state=to_state,
                timestamp=datetime.now(),
                details=details or {},
            )
        )
        return state

    def submit_for_review(self, scenario_id: str, actor: str, request: ApprovalRequest) -> dict[str, Any]:
        state = self._transition(scenario_id, actor, ScenarioState.SUBMITTED, details={"cover_note": request.cover_note})
        state["approval_request"] = self._serialize_request(request)
        self.save_state(scenario_id, state)
        return self._transition(scenario_id, actor, ScenarioState.UNDER_REVIEW)

    def request_changes(self, scenario_id: str, actor: str, reviewer_email: str, comment: str) -> dict[str, Any]:
        state = self.load_state(scenario_id)
        req = self._deserialize_request(state.get("approval_request"))
        req.responses.append(
            ApprovalResponse(
                reviewer_email=reviewer_email,
                decision=ApprovalDecision.CHANGES_REQUESTED,
                comment=comment,
                decided_at=datetime.now(),
            )
        )
        state["approval_request"] = self._serialize_request(req)
        self.save_state(scenario_id, state)
        return self._transition(scenario_id, actor, ScenarioState.CHANGES_REQUESTED, details={"comment": comment})

    def revise(self, scenario_id: str, actor: str, diff_summary: dict[str, Any]) -> dict[str, Any]:
        return self._transition(scenario_id, actor, ScenarioState.REVISED, details=diff_summary)

    def approve(self, scenario_id: str, actor: str, reviewer_email: str, comment: str = "") -> dict[str, Any]:
        state = self.load_state(scenario_id)
        req = self._deserialize_request(state.get("approval_request"))
        req.responses.append(
            ApprovalResponse(
                reviewer_email=reviewer_email,
                decision=ApprovalDecision.APPROVED,
                comment=comment,
                decided_at=datetime.now(),
            )
        )
        state["approval_request"] = self._serialize_request(req)
        self.save_state(scenario_id, state)

        rule_outcome = evaluate_approval_request(req)
        if rule_outcome.approved:
            return self._transition(scenario_id, actor, ScenarioState.APPROVED, details={"reason": rule_outcome.reason})
        return state

    def reject(self, scenario_id: str, actor: str, reviewer_email: str, comment: str) -> dict[str, Any]:
        state = self.load_state(scenario_id)
        req = self._deserialize_request(state.get("approval_request"))
        req.responses.append(
            ApprovalResponse(
                reviewer_email=reviewer_email,
                decision=ApprovalDecision.REJECTED,
                comment=comment,
                decided_at=datetime.now(),
            )
        )
        state["approval_request"] = self._serialize_request(req)
        self.save_state(scenario_id, state)
        return self._transition(scenario_id, actor, ScenarioState.REJECTED, details={"comment": comment})

    def publish(self, scenario_id: str, actor: str) -> dict[str, Any]:
        return self._transition(scenario_id, actor, ScenarioState.PUBLISHED)

    def archive(self, scenario_id: str, actor: str) -> dict[str, Any]:
        return self._transition(scenario_id, actor, ScenarioState.ARCHIVED)

    def withdraw(self, scenario_id: str, actor: str, reason: str) -> dict[str, Any]:
        return self._transition(scenario_id, actor, ScenarioState.WITHDRAWN, details={"reason": reason})

    def compliance_hold(self, scenario_id: str, actor: str, reason: str) -> dict[str, Any]:
        return self._transition(scenario_id, actor, ScenarioState.COMPLIANCE_HOLD, details={"reason": reason})

    @staticmethod
    def _serialize_request(req: ApprovalRequest | None) -> dict[str, Any] | None:
        if req is None:
            return None
        payload = asdict(req)
        payload["submitted_at"] = req.submitted_at.isoformat()
        payload["deadline"] = req.deadline.isoformat()
        payload["rule"] = req.rule.value
        for reviewer in payload["reviewers"]:
            reviewer["role"] = reviewer["role"].value
        for resp in payload["responses"]:
            resp["decision"] = resp["decision"].value
            decided_at = resp["decided_at"]
            if isinstance(decided_at, str):
                resp["decided_at"] = decided_at
            else:
                resp["decided_at"] = decided_at.isoformat()
        return payload

    @staticmethod
    def _deserialize_request(payload: dict[str, Any] | None) -> ApprovalRequest:
        if payload is None:
            raise RuntimeError("Approval request is not configured")

        reviewers = []
        for item in payload.get("reviewers", []):
            reviewers.append(
                ReviewerAssignment(
                    name=item["name"],
                    email=item["email"],
                    role=ReviewerRole(item["role"]),
                    sequence=item.get("sequence", 1),
                )
            )

        responses = []
        for item in payload.get("responses", []):
            responses.append(
                ApprovalResponse(
                    reviewer_email=item["reviewer_email"],
                    decision=ApprovalDecision(item["decision"]),
                    comment=item.get("comment", ""),
                    decided_at=datetime.fromisoformat(item["decided_at"]),
                )
            )

        return ApprovalRequest(
            scenario_id=payload["scenario_id"],
            scenario_name=payload["scenario_name"],
            submitted_by=payload["submitted_by"],
            submitted_at=datetime.fromisoformat(payload["submitted_at"]),
            deadline=datetime.fromisoformat(payload["deadline"]),
            cover_note=payload.get("cover_note", ""),
            rule=ApprovalRule(payload["rule"]),
            quorum_n=int(payload.get("quorum_n", 0)),
            reviewers=reviewers,
            responses=responses,
        )

    def latest_comments(self, scenario_id: str, limit: int = 5) -> list[dict[str, Any]]:
        state = self.load_state(scenario_id)
        if not state.get("approval_request"):
            return []
        req = self._deserialize_request(state.get("approval_request"))
        rows = sorted(req.responses, key=lambda x: x.decided_at, reverse=True)[:limit]
        return [
            {
                "reviewer": row.reviewer_email,
                "decision": row.decision.value,
                "comment": row.comment,
                "timestamp": row.decided_at.isoformat(),
            }
            for row in rows
            if row.comment
        ]
