from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path

CONFIG_FILE = Path(__file__).resolve().parent / "config.json"


@dataclass
class Config:
    """Application configuration."""

    gallery_dl_path: str

    @classmethod
    def load(cls) -> "Config":
        """Load configuration from disk or return defaults."""
        if CONFIG_FILE.exists():
            data = json.loads(CONFIG_FILE.read_text())
            return cls(**data)
        default_path = str(Path(__file__).resolve().parent.parent / "gallery-dl.exe")
        config = cls(gallery_dl_path=default_path)
        config.save()
        return config

    def save(self) -> None:
        """Persist configuration to disk."""
        CONFIG_FILE.write_text(json.dumps(asdict(self), indent=2))
