from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env", override=True)

DEFAULT_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


def _configured_origins() -> list[str]:
    extra_origins = [
        origin.strip()
        for origin in os.getenv("ARC_ALLOWED_ORIGINS", "").split(",")
        if origin.strip()
    ]
    return [*DEFAULT_ALLOWED_ORIGINS, *extra_origins]


ALLOWED_ORIGINS = _configured_origins()


@dataclass(frozen=True)
class Settings:
    app_name: str = "Arc"
    environment: str = os.getenv("ARC_ENV", "development")
    sandbox_mode: str = os.getenv("ARC_SANDBOX_MODE", "openai")
    root_dir: Path = ROOT_DIR

    @property
    def cors_origins(self) -> list[str]:
        return ALLOWED_ORIGINS

    @property
    def data_dir(self) -> Path:
        return self.root_dir / "data"

    @property
    def workspaces_root(self) -> Path:
        return self.data_dir / "workspaces"

    @property
    def workspace_root(self) -> Path:
        return self.workspaces_root / "default"

    @property
    def var_dir(self) -> Path:
        return self.data_dir / "var"

    @property
    def sqlite_path(self) -> Path:
        return self.var_dir / "app.sqlite"

    @property
    def duckdb_path(self) -> Path:
        return self.var_dir / "app.duckdb"


settings = Settings()
