"""Blank configuration is a supported offline state; secrets never appear in status."""

import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType

from dotenv import dotenv_values

from .paths import inside

PROVIDER_KEYS = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "moonshot": "MOONSHOT_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
}


@dataclass(frozen=True)
class Settings:
    values: Mapping[str, str] = field(repr=False)

    @classmethod
    def load(cls, root: Path, *, environ: Mapping[str, str] | None = None) -> "Settings":
        path = inside(root, ".env")
        parsed = dotenv_values(path, interpolate=False) if path.exists() else {}
        values = {k: v or "" for k, v in parsed.items()}
        values.update(os.environ if environ is None else environ)
        return cls(MappingProxyType(values))

    @property
    def model_name(self) -> str:
        return self.values.get("COUNCIL_MODEL_NAME", "").strip()

    def status(self) -> dict:
        provider = self.values.get("COUNCIL_MODEL_PROVIDER", "").strip().lower()
        key = self.values.get(PROVIDER_KEYS.get(provider, ""), "").strip()
        return {
            "model_configured": bool(provider in PROVIDER_KEYS and self.model_name and key),
            "live_runtime_implemented": False,
            "tidb_configured": all(
                self.values.get(k)
                for k in ("TIDB_HOST", "TIDB_DATABASE", "TIDB_USER", "TIDB_PASSWORD")
            ),
            "filesystem_configured": all(
                self.values.get(k)
                for k in ("TIDB_FILESYSTEM_URL", "TIDB_FILESYSTEM_ID", "TIDB_FILESYSTEM_TOKEN")
            ),
            "mem9_configured": all(
                self.values.get(k)
                for k in (
                    "MEM9_API_URL",
                    "MEM9_TECHNOLOGY_EVOLUTION_API_KEY",
                    "MEM9_SEXUAL_SELECTION_API_KEY",
                    "MEM9_NATURAL_SELECTION_API_KEY",
                    "MEM9_CULTURAL_EVOLUTION_API_KEY",
                    "MEM9_ANGEL_INVESTMENT_API_KEY",
                    "MEM9_VENTURE_CAPITAL_API_KEY",
                    "MEM9_SHARED_API_KEY",
                )
            ),
            "cloud_adapters_implemented": False,
            "telemetry": "local_only",
        }

    def require_live(self) -> None:
        raise ValueError(
            "Live research is not implemented; use prepare for local context documents"
        )
