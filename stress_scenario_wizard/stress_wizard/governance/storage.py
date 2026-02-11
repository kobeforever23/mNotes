from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from stress_wizard.governance.models import DistributionList, DistributionMember, ReviewerRole


class GovernanceStorage:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.distribution_lists_path = self.root / "distribution_lists.json"
        self.rules_path = self.root / "approval_rules.json"
        self.pending_path = self.root / "pending_approvals.json"

    def load_distribution_lists(self) -> list[DistributionList]:
        if not self.distribution_lists_path.exists():
            return []
        payload = json.loads(self.distribution_lists_path.read_text(encoding="utf-8"))
        out = []
        for item in payload:
            members = [
                DistributionMember(
                    name=m["name"],
                    email=m["email"],
                    role=ReviewerRole(m["role"]),
                )
                for m in item.get("members", [])
            ]
            out.append(DistributionList(name=item["name"], members=members))
        return out

    def save_distribution_lists(self, lists: list[DistributionList]) -> None:
        payload = []
        for entry in lists:
            row = {"name": entry.name, "members": []}
            for member in entry.members:
                row["members"].append(
                    {
                        "name": member.name,
                        "email": member.email,
                        "role": member.role.value,
                    }
                )
            payload.append(row)
        self.distribution_lists_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load_rules(self) -> dict:
        if not self.rules_path.exists():
            return {
                "mandatory_approval_for_export": True,
                "severity_requirements": {"Extreme": ["CRO"]},
                "conditional_routing": {"pnl_threshold": 10000000, "add_role": "Senior Management"},
                "expiration_days": 30,
                "reapproval_on_edit": True,
            }
        return json.loads(self.rules_path.read_text(encoding="utf-8"))

    def save_rules(self, rules: dict) -> None:
        self.rules_path.write_text(json.dumps(rules, indent=2), encoding="utf-8")

    def load_pending(self) -> list[dict]:
        if not self.pending_path.exists():
            return []
        return json.loads(self.pending_path.read_text(encoding="utf-8"))

    def save_pending(self, pending: list[dict]) -> None:
        self.pending_path.write_text(json.dumps(pending, indent=2), encoding="utf-8")

    def upsert_pending(self, scenario_id: str, payload: dict) -> None:
        pending = self.load_pending()
        pending = [row for row in pending if row.get("scenario_id") != scenario_id]
        pending.append(payload)
        self.save_pending(pending)

    def remove_pending(self, scenario_id: str) -> None:
        pending = self.load_pending()
        pending = [row for row in pending if row.get("scenario_id") != scenario_id]
        self.save_pending(pending)
