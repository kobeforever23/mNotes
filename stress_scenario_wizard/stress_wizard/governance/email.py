from __future__ import annotations

from dataclasses import dataclass
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import platform
import smtplib
from typing import Iterable

from jinja2 import Template


LOGGER = logging.getLogger(__name__)


EMAIL_TEMPLATE = Template(
    """
    <html>
    <body style=\"font-family:Segoe UI,Arial,sans-serif;color:#111\">
    <h3>[STRESS SCENARIO — APPROVAL REQUIRED] {{ scenario_name }}</h3>
    <p><strong>Severity:</strong> {{ severity }}<br/>
       <strong>Horizon:</strong> {{ horizon }}<br/>
       <strong>As-of:</strong> {{ as_of }}<br/>
       <strong>Submitted by:</strong> {{ submitted_by }}</p>
    <p>{{ summary }}</p>
    <p>
      <a href=\"{{ approve_link }}\">APPROVE</a> |
      <a href=\"{{ changes_link }}\">REQUEST CHANGES</a> |
      <a href=\"{{ reject_link }}\">REJECT</a>
    </p>
    <hr/>
    <small>Scenario ID: {{ scenario_id }}</small>
    </body>
    </html>
    """
)


@dataclass(slots=True)
class EmailPayload:
    subject: str
    to: list[str]
    cc: list[str]
    bcc: list[str]
    html_body: str
    attachments: list[tuple[str, bytes]]


class OutlookSender:
    def available(self) -> bool:
        return platform.system().lower() == "windows"

    def send(self, payload: EmailPayload, draft_mode: bool = False) -> None:
        if not self.available():
            raise RuntimeError("Outlook COM automation is available only on Windows")

        import win32com.client  # type: ignore

        app = win32com.client.Dispatch("Outlook.Application")
        mail = app.CreateItem(0)
        mail.Subject = payload.subject
        mail.To = ";".join(payload.to)
        mail.CC = ";".join(payload.cc)
        mail.BCC = ";".join(payload.bcc)
        mail.HTMLBody = payload.html_body

        for filename, data in payload.attachments:
            import tempfile
            from pathlib import Path

            tmp = Path(tempfile.gettempdir()) / filename
            tmp.write_bytes(data)
            mail.Attachments.Add(str(tmp))

        if draft_mode:
            mail.Display(True)
        else:
            mail.Send()


class SMTPSender:
    def __init__(self, server: str, port: int, username: str, password: str, tls: bool = True) -> None:
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.tls = tls

    def send(self, payload: EmailPayload) -> None:
        msg = MIMEMultipart()
        msg["Subject"] = payload.subject
        msg["From"] = self.username
        msg["To"] = ",".join(payload.to)
        if payload.cc:
            msg["Cc"] = ",".join(payload.cc)
        msg.attach(MIMEText(payload.html_body, "html"))

        for filename, content in payload.attachments:
            part = MIMEApplication(content)
            part.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(part)

        recipients = payload.to + payload.cc + payload.bcc
        with smtplib.SMTP(self.server, self.port, timeout=30) as smtp:
            if self.tls:
                smtp.starttls()
            if self.username:
                smtp.login(self.username, self.password)
            smtp.sendmail(self.username, recipients, msg.as_string())


def render_submission_email(
    scenario_id: str,
    scenario_name: str,
    severity: str,
    horizon: str,
    as_of: str,
    submitted_by: str,
    summary: str,
    approve_link: str,
    changes_link: str,
    reject_link: str,
) -> str:
    return EMAIL_TEMPLATE.render(
        scenario_id=scenario_id,
        scenario_name=scenario_name,
        severity=severity,
        horizon=horizon,
        as_of=as_of,
        submitted_by=submitted_by,
        summary=summary,
        approve_link=approve_link,
        changes_link=changes_link,
        reject_link=reject_link,
    )


def build_email_payload(
    scenario_id: str,
    scenario_name: str,
    severity: str,
    horizon: str,
    as_of: str,
    submitted_by: str,
    summary_points: Iterable[str],
    to: list[str],
    cc: list[str] | None = None,
    bcc: list[str] | None = None,
    approve_link: str = "http://localhost:8008/approve",
    changes_link: str = "http://localhost:8008/request-changes",
    reject_link: str = "http://localhost:8008/reject",
    attachments: list[tuple[str, bytes]] | None = None,
) -> EmailPayload:
    summary = "<ul>" + "".join(f"<li>{point}</li>" for point in summary_points) + "</ul>"
    subject = f"[STRESS SCENARIO — APPROVAL REQUIRED] {scenario_name} | {severity} | {as_of}"
    html = render_submission_email(
        scenario_id=scenario_id,
        scenario_name=scenario_name,
        severity=severity,
        horizon=horizon,
        as_of=as_of,
        submitted_by=submitted_by,
        summary=summary,
        approve_link=approve_link,
        changes_link=changes_link,
        reject_link=reject_link,
    )

    return EmailPayload(
        subject=subject,
        to=to,
        cc=cc or [],
        bcc=bcc or [],
        html_body=html,
        attachments=attachments or [],
    )


def send_with_best_effort(
    payload: EmailPayload,
    mode: str,
    smtp_server: str = "",
    smtp_port: int = 587,
    smtp_user: str = "",
    smtp_password: str = "",
    smtp_tls: bool = True,
    draft_mode: bool = True,
) -> str:
    mode = mode.upper()
    if mode == "OUTLOOK":
        try:
            OutlookSender().send(payload, draft_mode=draft_mode)
            return "OUTLOOK_SENT"
        except Exception as exc:
            LOGGER.warning("Outlook send failed, fallback to SMTP if configured: %s", exc)
            if smtp_server:
                SMTPSender(smtp_server, smtp_port, smtp_user, smtp_password, tls=smtp_tls).send(payload)
                return "SMTP_SENT"
            raise

    if mode == "SMTP":
        SMTPSender(smtp_server, smtp_port, smtp_user, smtp_password, tls=smtp_tls).send(payload)
        return "SMTP_SENT"

    LOGGER.info("Email mode %s selected; no outbound message sent.", mode)
    return "NO_EMAIL_SENT"
