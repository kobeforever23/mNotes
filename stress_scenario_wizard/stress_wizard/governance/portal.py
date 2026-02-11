from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable

from itsdangerous import URLSafeTimedSerializer, BadSignature

try:
    from flask import Flask, request
except Exception:  # pragma: no cover
    Flask = None
    request = None


@dataclass(slots=True)
class ApprovalTokenService:
    secret_key: str
    salt: str = "stress-wizard-approval"

    def _serializer(self) -> URLSafeTimedSerializer:
        return URLSafeTimedSerializer(secret_key=self.secret_key, salt=self.salt)

    def generate(self, scenario_id: str, reviewer_email: str) -> str:
        return self._serializer().dumps({"scenario_id": scenario_id, "reviewer": reviewer_email, "ts": datetime.now().isoformat()})

    def verify(self, token: str, max_age_seconds: int = 7 * 24 * 3600) -> dict:
        try:
            return self._serializer().loads(token, max_age=max_age_seconds)
        except BadSignature as exc:
            raise RuntimeError("Invalid or expired approval token") from exc


def build_portal_app(
    token_service: ApprovalTokenService,
    on_decision: Callable[[str, str, str, str], None],
) -> Flask:
    if Flask is None:
        raise RuntimeError("Flask is not installed")

    app = Flask(__name__)

    @app.get("/approve/<scenario_id>/<token>")
    def approve_page(scenario_id: str, token: str):
        payload = token_service.verify(token)
        if payload.get("scenario_id") != scenario_id:
            return "Token/scenario mismatch", 400
        return (
            "<h2>Scenario Approval</h2>"
            "<form method='post'>"
            "<textarea name='comment' placeholder='Comment'></textarea><br/>"
            "<button name='decision' value='APPROVED'>Approve</button>"
            "<button name='decision' value='CHANGES_REQUESTED'>Request Changes</button>"
            "<button name='decision' value='REJECTED'>Reject</button>"
            "</form>"
        )

    @app.post("/approve/<scenario_id>/<token>")
    def approve_action(scenario_id: str, token: str):
        payload = token_service.verify(token)
        reviewer = payload.get("reviewer", "unknown@example.com")
        decision = request.form.get("decision", "")
        comment = request.form.get("comment", "")
        on_decision(scenario_id, reviewer, decision, comment)
        return "Decision recorded."

    return app
