from __future__ import annotations

from datetime import datetime, timedelta

from stress_wizard.governance.models import ApprovalRequest, ApprovalRule, ReviewerAssignment, ReviewerRole
from stress_wizard.governance.workflow import GovernanceWorkflow


def test_governance_flow_approve(tmp_path) -> None:
    workflow = GovernanceWorkflow(tmp_path)
    scenario_id = "SCN-TEST-1"

    workflow.init_state(scenario_id, actor="alice")
    req = ApprovalRequest(
        scenario_id=scenario_id,
        scenario_name="Test",
        submitted_by="alice",
        submitted_at=datetime.now(),
        deadline=datetime.now() + timedelta(hours=24),
        cover_note="Please review",
        rule=ApprovalRule.UNANIMOUS,
        reviewers=[
            ReviewerAssignment(name="A", email="a@example.com", role=ReviewerRole.APPROVER, sequence=1),
            ReviewerAssignment(name="B", email="b@example.com", role=ReviewerRole.APPROVER, sequence=2),
        ],
    )

    state = workflow.submit_for_review(scenario_id, actor="alice", request=req)
    assert state["state"] == "Under Review"

    state = workflow.approve(scenario_id, actor="a@example.com", reviewer_email="a@example.com")
    assert state["state"] == "Under Review"

    state = workflow.approve(scenario_id, actor="b@example.com", reviewer_email="b@example.com")
    assert state["state"] == "Approved"


def test_governance_changes_requested(tmp_path) -> None:
    workflow = GovernanceWorkflow(tmp_path)
    scenario_id = "SCN-TEST-2"
    workflow.init_state(scenario_id, actor="alice")

    req = ApprovalRequest(
        scenario_id=scenario_id,
        scenario_name="Test2",
        submitted_by="alice",
        submitted_at=datetime.now(),
        deadline=datetime.now() + timedelta(hours=24),
        cover_note="Review",
        rule=ApprovalRule.UNANIMOUS,
        reviewers=[ReviewerAssignment(name="A", email="a@example.com", role=ReviewerRole.APPROVER, sequence=1)],
    )

    workflow.submit_for_review(scenario_id, actor="alice", request=req)
    state = workflow.request_changes(scenario_id, actor="a@example.com", reviewer_email="a@example.com", comment="Need edits")
    assert state["state"] == "Changes Requested"

    state = workflow.revise(scenario_id, actor="alice", diff_summary={"shock_change": True})
    assert state["state"] == "Revised"
