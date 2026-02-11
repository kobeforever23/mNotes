from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
import json
from typing import Any


DEFAULT_ROOT = Path.home() / "RiskAnalytics" / "StressScenarios"
DEFAULT_SETTINGS_PATH = Path("app_settings.json")


@dataclass(slots=True)
class GovernanceSettings:
    mode: str = "MANDATORY"  # OFF | OPTIONAL | MANDATORY
    mandatory_export_approval: bool = True
    severe_requires_cro: bool = True
    pnl_threshold_for_senior_routing: float = 10_000_000.0
    approval_expiry_days: int = 30
    reminder_hours: int = 24
    escalation_hours: int = 48
    response_method: str = "IN_APP"  # IN_APP | OUTLOOK_REPLY | WEB_PORTAL | SHARED_DRIVE
    approval_rule_default: str = "UNANIMOUS"  # UNANIMOUS | QUORUM | SEQUENTIAL | PARALLEL


@dataclass(slots=True)
class EmailSettings:
    mode: str = "DISABLED"  # OUTLOOK | SMTP | IN_APP | DISABLED
    smtp_server: str = "smtp.example.com"
    smtp_port: int = 587
    smtp_tls: bool = True
    smtp_user: str = ""
    smtp_password_key: str = "stress_wizard.smtp.password"
    draft_mode: bool = True


@dataclass(slots=True)
class AppSettings:
    root_path: str = str(DEFAULT_ROOT)
    autosave_enabled: bool = True
    autosave_interval_seconds: int = 120
    ai_narrative_enabled: bool = False
    ai_provider: str = "OPENAI"
    ai_model: str = "gpt-4o-mini"
    save_last_session: bool = True
    governance: GovernanceSettings = field(default_factory=GovernanceSettings)
    email: EmailSettings = field(default_factory=EmailSettings)

    @property
    def root_dir(self) -> Path:
        return Path(self.root_path)


def _as_settings_dict(settings: AppSettings) -> dict[str, Any]:
    data = asdict(settings)
    return data


def load_settings(path: Path | str = DEFAULT_SETTINGS_PATH) -> AppSettings:
    settings_path = Path(path)
    if not settings_path.exists():
        settings = AppSettings()
        save_settings(settings, settings_path)
        return settings

    payload = json.loads(settings_path.read_text(encoding="utf-8"))
    governance = GovernanceSettings(**payload.get("governance", {}))
    email = EmailSettings(**payload.get("email", {}))
    core = {k: v for k, v in payload.items() if k not in {"governance", "email"}}
    return AppSettings(**core, governance=governance, email=email)


def save_settings(settings: AppSettings, path: Path | str = DEFAULT_SETTINGS_PATH) -> None:
    settings_path = Path(path)
    settings_path.write_text(
        json.dumps(_as_settings_dict(settings), indent=2),
        encoding="utf-8",
    )
