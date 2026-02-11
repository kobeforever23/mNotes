from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class ScenarioState(str, Enum):
    DRAFT = "Draft"
    SUBMITTED = "Submitted for Review"
    UNDER_REVIEW = "Under Review"
    CHANGES_REQUESTED = "Changes Requested"
    REVISED = "Revised"
    APPROVED = "Approved"
    PUBLISHED = "Published/Exported"
    ARCHIVED = "Archived"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"
    COMPLIANCE_HOLD = "Compliance Hold"


class ReviewerRole(str, Enum):
    APPROVER = "Approver"
    REVIEWER = "Reviewer"
    FYI = "FYI"
    ESCALATION = "Escalation"


class ApprovalDecision(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    CHANGES_REQUESTED = "Changes Requested"


class ApprovalRule(str, Enum):
    UNANIMOUS = "UNANIMOUS"
    QUORUM = "QUORUM"
    SEQUENTIAL = "SEQUENTIAL"
    PARALLEL = "PARALLEL"


@dataclass(slots=True)
class DistributionMember:
    name: str
    email: str
    role: ReviewerRole


@dataclass(slots=True)
class DistributionList:
    name: str
    members: list[DistributionMember]


@dataclass(slots=True)
class ReviewerAssignment:
    name: str
    email: str
    role: ReviewerRole
    sequence: int = 1


@dataclass(slots=True)
class ApprovalResponse:
    reviewer_email: str
    decision: ApprovalDecision
    comment: str
    decided_at: datetime


@dataclass(slots=True)
class ApprovalRequest:
    scenario_id: str
    scenario_name: str
    submitted_by: str
    submitted_at: datetime
    deadline: datetime
    cover_note: str
    rule: ApprovalRule
    quorum_n: int = 0
    reviewers: list[ReviewerAssignment] = field(default_factory=list)
    responses: list[ApprovalResponse] = field(default_factory=list)


@dataclass(slots=True)
class GovernanceEvent:
    scenario_id: str
    actor: str
    action: str
    from_state: ScenarioState
    to_state: ScenarioState
    timestamp: datetime
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["from_state"] = self.from_state.value
        data["to_state"] = self.to_state.value
        data["timestamp"] = self.timestamp.isoformat()
        return data
