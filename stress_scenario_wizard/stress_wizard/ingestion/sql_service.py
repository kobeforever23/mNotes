from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json
from typing import Any

import pandas as pd
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine


SQL_PROFILE_PATH = Path("sql_connection_profiles.json")


@dataclass(slots=True)
class SQLConnectionProfile:
    name: str
    server: str
    database: str
    auth_method: str = "WINDOWS"  # WINDOWS | SQL
    username: str = ""
    encrypted_password_ref: str = ""
    driver: str = "ODBC Driver 18 for SQL Server"
    trust_server_certificate: bool = True


class SQLService:
    """SQL Server helper service using SQLAlchemy."""

    def __init__(self) -> None:
        self._engine: Engine | None = None

    @staticmethod
    def build_connection_string(
        server: str,
        database: str,
        auth_method: str,
        username: str = "",
        password: str = "",
        driver: str = "ODBC Driver 18 for SQL Server",
        trust_server_certificate: bool = True,
    ) -> str:
        common = f"driver={driver.replace(' ', '+')};TrustServerCertificate={'yes' if trust_server_certificate else 'no'}"
        if auth_method.upper() == "WINDOWS":
            return f"mssql+pyodbc://@{server}/{database}?trusted_connection=yes&{common}"
        return f"mssql+pyodbc://{username}:{password}@{server}/{database}?{common}"

    def connect(
        self,
        server: str,
        database: str,
        auth_method: str,
        username: str = "",
        password: str = "",
        driver: str = "ODBC Driver 18 for SQL Server",
        trust_server_certificate: bool = True,
    ) -> Engine:
        conn_str = self.build_connection_string(
            server=server,
            database=database,
            auth_method=auth_method,
            username=username,
            password=password,
            driver=driver,
            trust_server_certificate=trust_server_certificate,
        )
        self._engine = create_engine(conn_str, pool_pre_ping=True)
        with self._engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return self._engine

    @property
    def connected(self) -> bool:
        return self._engine is not None

    def list_schema_tables(self) -> pd.DataFrame:
        if not self._engine:
            return pd.DataFrame(columns=["schema", "table", "columns"])

        inspector = inspect(self._engine)
        rows: list[dict[str, Any]] = []
        for schema in inspector.get_schema_names():
            for table in inspector.get_table_names(schema=schema):
                cols = inspector.get_columns(table, schema=schema)
                rows.append({"schema": schema, "table": table, "columns": ", ".join(c["name"] for c in cols)})
        return pd.DataFrame(rows)

    def preview_table(self, schema: str, table: str, limit: int = 100) -> pd.DataFrame:
        if not self._engine:
            raise RuntimeError("SQL engine is not connected")
        query = text(f"SELECT TOP {int(limit)} * FROM [{schema}].[{table}]")
        return pd.read_sql(query, self._engine)

    def run_query(self, query: str) -> pd.DataFrame:
        if not self._engine:
            raise RuntimeError("SQL engine is not connected")
        return pd.read_sql(text(query), self._engine)

    def save_profile(self, profile: SQLConnectionProfile) -> None:
        payload = []
        if SQL_PROFILE_PATH.exists():
            payload = json.loads(SQL_PROFILE_PATH.read_text(encoding="utf-8"))

        payload = [p for p in payload if p.get("name") != profile.name]
        payload.append(asdict(profile))
        SQL_PROFILE_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load_profiles(self) -> list[SQLConnectionProfile]:
        if not SQL_PROFILE_PATH.exists():
            return []
        payload = json.loads(SQL_PROFILE_PATH.read_text(encoding="utf-8"))
        return [SQLConnectionProfile(**item) for item in payload]
