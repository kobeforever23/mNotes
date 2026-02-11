from __future__ import annotations

from datetime import datetime, timedelta
import json
from pathlib import Path

import pandas as pd
from PySide6.QtWidgets import (
    QComboBox,
    QDateTimeEdit,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableView,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from stress_wizard.app_state import AppState
from stress_wizard.config import AppSettings
from stress_wizard.governance.models import (
    ApprovalRequest,
    ApprovalRule,
    ReviewerAssignment,
    ReviewerRole,
    ScenarioState,
)
from stress_wizard.governance.storage import GovernanceStorage
from stress_wizard.governance.workflow import GovernanceWorkflow
from stress_wizard.ui.signals import AppSignals
from stress_wizard.ui.widgets.pandas_model import LazyDataFrameModel


class GovernanceWidget(QWidget):
    def __init__(self, state: AppState, settings: AppSettings, signals: AppSignals, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.state = state
        self.settings = settings
        self.signals = signals

        gov_root = Path(settings.root_path) / "governance"
        self.storage = GovernanceStorage(gov_root)
        self.workflow = GovernanceWorkflow(gov_root / "scenarios")

        self.pending_model = LazyDataFrameModel(pd.DataFrame())
        self.responses_model = LazyDataFrameModel(pd.DataFrame())

        self._build_ui()
        self._bootstrap_files()
        self._refresh_state_view()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)

        state_group = QGroupBox("Scenario Lifecycle")
        state_layout = QHBoxLayout(state_group)
        self.state_label = QLabel("State: Draft")
        self.version_label = QLabel("Version: 1")
        self.lock_label = QLabel("Locked: No")
        state_layout.addWidget(self.state_label)
        state_layout.addWidget(self.version_label)
        state_layout.addWidget(self.lock_label)
        state_layout.addStretch(1)

        submission_group = QGroupBox("Submit for Approval")
        sub_layout = QFormLayout(submission_group)

        self.reviewers_input = QLineEdit()
        self.reviewers_input.setPlaceholderText("name:email:role;name:email:role")
        self.reviewers_input.setText("Jane Smith:jane@bank.com:Approver;Mark Jones:mark@bank.com:Approver;Model Validation:mv@bank.com:Reviewer")

        self.rule_combo = QComboBox()
        self.rule_combo.addItems([rule.value for rule in ApprovalRule])

        self.quorum_spin = QSpinBox()
        self.quorum_spin.setRange(0, 20)
        self.quorum_spin.setValue(2)

        self.deadline_edit = QDateTimeEdit()
        self.deadline_edit.setDateTime(datetime.now() + timedelta(hours=48))

        self.cover_note = QTextEdit()
        self.cover_note.setPlaceholderText("Submission context and key findings.")
        self.cover_note.setMinimumHeight(70)

        submit_btn = QPushButton("Submit For Review")
        submit_btn.clicked.connect(self._submit)

        sub_layout.addRow("Reviewers", self.reviewers_input)
        sub_layout.addRow("Rule", self.rule_combo)
        sub_layout.addRow("Quorum N", self.quorum_spin)
        sub_layout.addRow("Deadline", self.deadline_edit)
        sub_layout.addRow("Cover Note", self.cover_note)
        sub_layout.addRow("", submit_btn)

        action_group = QGroupBox("Review Actions")
        action_layout = QHBoxLayout(action_group)
        self.actor_email = QLineEdit()
        self.actor_email.setPlaceholderText("reviewer@bank.com")
        self.actor_email.setText("jane@bank.com")
        approve_btn = QPushButton("Approve")
        approve_btn.clicked.connect(self._approve)
        changes_btn = QPushButton("Request Changes")
        changes_btn.clicked.connect(self._request_changes)
        reject_btn = QPushButton("Reject")
        reject_btn.clicked.connect(self._reject)
        publish_btn = QPushButton("Publish")
        publish_btn.clicked.connect(self._publish)
        withdraw_btn = QPushButton("Withdraw")
        withdraw_btn.clicked.connect(self._withdraw)

        action_layout.addWidget(QLabel("Actor"))
        action_layout.addWidget(self.actor_email)
        action_layout.addWidget(approve_btn)
        action_layout.addWidget(changes_btn)
        action_layout.addWidget(reject_btn)
        action_layout.addWidget(publish_btn)
        action_layout.addWidget(withdraw_btn)

        responses_table = QTableView()
        responses_table.setModel(self.responses_model)
        responses_table.setAlternatingRowColors(True)

        pending_table = QTableView()
        pending_table.setModel(self.pending_model)
        pending_table.setAlternatingRowColors(True)

        self.comment_box = QTextEdit()
        self.comment_box.setPlaceholderText("Decision comment")
        self.comment_box.setMinimumHeight(60)

        root.addWidget(state_group)
        root.addWidget(submission_group)
        root.addWidget(action_group)
        root.addWidget(QLabel("Comment"))
        root.addWidget(self.comment_box)
        root.addWidget(QLabel("Approval Responses"))
        root.addWidget(responses_table, stretch=1)
        root.addWidget(QLabel("Governance Dashboard (Pending Index)"))
        root.addWidget(pending_table, stretch=1)

    def _bootstrap_files(self) -> None:
        lists = self.storage.load_distribution_lists()
        if not lists:
            sample = [
                {
                    "name": "Stress Testing Committee",
                    "members": [
                        {"name": "Jane Smith", "email": "jane@bank.com", "role": "Approver"},
                        {"name": "Mark Jones", "email": "mark@bank.com", "role": "Approver"},
                        {"name": "Model Validation", "email": "mv@bank.com", "role": "Reviewer"},
                        {"name": "Compliance", "email": "compliance@bank.com", "role": "Escalation"},
                    ],
                }
            ]
            self.storage.distribution_lists_path.write_text(json.dumps(sample, indent=2), encoding="utf-8")

        if not self.storage.rules_path.exists():
            self.storage.save_rules(
                {
                    "mandatory_approval_for_export": True,
                    "severity_requirements": {
                        "Extreme": ["CRO"],
                        "Severe": ["Desk Head", "Risk Manager"],
                        "Moderate": ["Desk Head"],
                    },
                    "conditional_routing": {"pnl_threshold": 10000000, "auto_add": "Senior Management"},
                    "expiration_days": 30,
                    "reapproval_on_edit": True,
                    "compliance_hold": {"enabled": True, "release_role": "Compliance Officer"},
                }
            )

    def _scenario_id(self) -> str:
        return self.state.ensure_scenario().metadata.scenario_id

    def _parse_reviewers(self) -> list[ReviewerAssignment]:
        out = []
        raw = self.reviewers_input.text().strip()
        if not raw:
            return out
        for seq, chunk in enumerate(raw.split(";"), start=1):
            parts = [p.strip() for p in chunk.split(":")]
            if len(parts) < 3:
                continue
            name, email, role_text = parts[0], parts[1], parts[2]
            role = ReviewerRole(role_text)
            out.append(ReviewerAssignment(name=name, email=email, role=role, sequence=seq))
        return out

    def _submit(self) -> None:
        scenario = self.state.ensure_scenario()
        reviewers = self._parse_reviewers()
        if not reviewers:
            QMessageBox.warning(self, "Reviewers Missing", "Provide at least one reviewer/approver entry.")
            return

        req = ApprovalRequest(
            scenario_id=scenario.metadata.scenario_id,
            scenario_name=scenario.metadata.name,
            submitted_by=scenario.metadata.author,
            submitted_at=datetime.now(),
            deadline=self.deadline_edit.dateTime().toPython(),
            cover_note=self.cover_note.toPlainText().strip(),
            rule=ApprovalRule(self.rule_combo.currentText()),
            quorum_n=int(self.quorum_spin.value()),
            reviewers=reviewers,
            responses=[],
        )

        try:
            self.workflow.init_state(self._scenario_id(), actor=scenario.metadata.author)
            state = self.workflow.submit_for_review(self._scenario_id(), actor=scenario.metadata.author, request=req)
            self.storage.upsert_pending(
                self._scenario_id(),
                {
                    "scenario_id": self._scenario_id(),
                    "scenario_name": scenario.metadata.name,
                    "submitted_by": scenario.metadata.author,
                    "submitted_at": datetime.now().isoformat(),
                    "status": state.get("state"),
                    "deadline": req.deadline.isoformat(),
                    "approvers": [f"{r.name}<{r.email}>" for r in reviewers if r.role == ReviewerRole.APPROVER],
                },
            )
            self.signals.governance_changed.emit()
            self.signals.status_message.emit("Scenario submitted for governance review.")
            self._refresh_state_view()
        except Exception as exc:
            QMessageBox.critical(self, "Submission Failed", str(exc))

    def _approve(self) -> None:
        self._decision("approve")

    def _request_changes(self) -> None:
        self._decision("changes")

    def _reject(self) -> None:
        self._decision("reject")

    def _decision(self, mode: str) -> None:
        actor = self.actor_email.text().strip()
        if not actor:
            QMessageBox.warning(self, "Actor Missing", "Enter reviewer email.")
            return

        comment = self.comment_box.toPlainText().strip()
        scenario_id = self._scenario_id()

        try:
            if mode == "approve":
                state = self.workflow.approve(scenario_id, actor=actor, reviewer_email=actor, comment=comment)
            elif mode == "changes":
                state = self.workflow.request_changes(scenario_id, actor=actor, reviewer_email=actor, comment=comment)
            else:
                state = self.workflow.reject(scenario_id, actor=actor, reviewer_email=actor, comment=comment)

            status = state.get("state")
            if status in {ScenarioState.APPROVED.value, ScenarioState.REJECTED.value, ScenarioState.CHANGES_REQUESTED.value}:
                if status == ScenarioState.APPROVED.value:
                    self.storage.remove_pending(scenario_id)
                else:
                    self.storage.upsert_pending(
                        scenario_id,
                        {
                            "scenario_id": scenario_id,
                            "scenario_name": self.state.ensure_scenario().metadata.name,
                            "submitted_by": self.state.ensure_scenario().metadata.author,
                            "submitted_at": state.get("updated_at"),
                            "status": status,
                            "deadline": "",
                            "approvers": [],
                        },
                    )
            self.signals.governance_changed.emit()
            self._refresh_state_view()
        except Exception as exc:
            QMessageBox.critical(self, "Decision Failed", str(exc))

    def _publish(self) -> None:
        scenario_id = self._scenario_id()
        state = self.workflow.load_state(scenario_id)
        if self.settings.governance.mandatory_export_approval and state.get("state") != ScenarioState.APPROVED.value:
            QMessageBox.warning(self, "Blocked", "Mandatory governance is enabled: scenario must be Approved before publish/export.")
            return
        try:
            self.workflow.publish(scenario_id, actor=self.state.ensure_scenario().metadata.author)
            self.storage.remove_pending(scenario_id)
            self.signals.governance_changed.emit()
            self._refresh_state_view()
            self.signals.status_message.emit("Scenario marked as Published.")
        except Exception as exc:
            QMessageBox.critical(self, "Publish Failed", str(exc))

    def _withdraw(self) -> None:
        try:
            self.workflow.withdraw(self._scenario_id(), actor=self.state.ensure_scenario().metadata.author, reason="Withdrawn by submitter")
            self.storage.remove_pending(self._scenario_id())
            self._refresh_state_view()
        except Exception as exc:
            QMessageBox.critical(self, "Withdraw Failed", str(exc))

    def _refresh_state_view(self) -> None:
        scenario_id = self._scenario_id()
        self.workflow.init_state(scenario_id, actor=self.state.ensure_scenario().metadata.author)
        state = self.workflow.load_state(scenario_id)

        self.state_label.setText(f"State: {state.get('state', 'Unknown')}")
        self.version_label.setText(f"Version: {state.get('version', 1)}")
        self.lock_label.setText(f"Locked: {'Yes' if state.get('locked') else 'No'}")

        req = state.get("approval_request") or {}
        resp = pd.DataFrame(req.get("responses", [])) if req else pd.DataFrame()
        self.responses_model.set_frame(resp)

        pending = pd.DataFrame(self.storage.load_pending())
        self.pending_model.set_frame(pending)
