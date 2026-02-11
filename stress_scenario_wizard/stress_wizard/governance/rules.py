from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from stress_wizard.governance.models import ApprovalRule, ApprovalRequest, ApprovalDecision, ReviewerRole


@dataclass(slots=True)
class GovernanceRuleResult:
    approved: bool
    reason: str


def evaluate_approval_request(req: ApprovalRequest) -> GovernanceRuleResult:
    approvers = [r for r in req.reviewers if r.role == ReviewerRole.APPROVER]
    responses = {r.reviewer_email.lower(): r for r in req.responses}

    if not approvers:
        return GovernanceRuleResult(False, "No approvers assigned.")

    approved_emails = {
        resp.reviewer_email.lower()
        for resp in req.responses
        if resp.decision == ApprovalDecision.APPROVED
    }
    rejected = [resp for resp in req.responses if resp.decision == ApprovalDecision.REJECTED]
    changes = [resp for resp in req.responses if resp.decision == ApprovalDecision.CHANGES_REQUESTED]

    if rejected:
        return GovernanceRuleResult(False, "Rejected by at least one approver.")
    if changes:
        return GovernanceRuleResult(False, "Changes requested by reviewer/approver.")

    if req.rule == ApprovalRule.UNANIMOUS or req.rule == ApprovalRule.PARALLEL:
        all_emails = {r.email.lower() for r in approvers}
        if all_emails.issubset(approved_emails):
            return GovernanceRuleResult(True, "All approvers approved.")
        return GovernanceRuleResult(False, "Awaiting remaining approvers.")

    if req.rule == ApprovalRule.QUORUM:
        n = req.quorum_n if req.quorum_n > 0 else len(approvers)
        if len(approved_emails.intersection({r.email.lower() for r in approvers})) >= n:
            return GovernanceRuleResult(True, f"Quorum reached ({n}).")
        return GovernanceRuleResult(False, f"Awaiting quorum ({n}).")

    if req.rule == ApprovalRule.SEQUENTIAL:
        ordered = sorted(approvers, key=lambda r: r.sequence)
        for reviewer in ordered:
            resp = responses.get(reviewer.email.lower())
            if not resp or resp.decision != ApprovalDecision.APPROVED:
                return GovernanceRuleResult(False, f"Waiting on sequence approver {reviewer.name}.")
        return GovernanceRuleResult(True, "Sequential approvals complete.")

    return GovernanceRuleResult(False, "Unknown approval rule.")


def is_overdue(req: ApprovalRequest, now: datetime | None = None) -> bool:
    now = now or datetime.now()
    return now > req.deadline


def time_remaining(req: ApprovalRequest, now: datetime | None = None) -> timedelta:
    now = now or datetime.now()
    return req.deadline - now
