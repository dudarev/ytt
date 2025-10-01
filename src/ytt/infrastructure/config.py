"""Configuration repository for ytt."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

from appdirs import user_config_dir

CONFIG_DIR_NAME = "ytt"
CONFIG_FILE_NAME = "config.json"
CACHE_DIR_NAME = "cache"


class ConfigRepository:
    """Handles reading and writing the user configuration."""

    def __init__(self, config_dir_name: str = CONFIG_DIR_NAME, config_file_name: str = CONFIG_FILE_NAME) -> None:
        self._config_dir_name = config_dir_name
        self._config_file_name = config_file_name

    @property
    def config_dir(self) -> Path:
        return Path(user_config_dir(self._config_dir_name))

    @property
    def config_file(self) -> Path:
        return self.config_dir / self._config_file_name

    @property
    def cache_dir(self) -> Path:
        return self.config_dir / CACHE_DIR_NAME

    def load(self) -> Dict[str, Any]:
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as handle:
                    return json.load(handle)
            except json.JSONDecodeError:
                print(
                    f"Warning: Could not decode config file at {self.config_file}",
                    file=sys.stderr,
                )
            except Exception as exc:  # pragma: no cover - defensive
                print(f"Warning: Error loading config file {self.config_file}: {exc}", file=sys.stderr)
        return {}

    def save(self, config: Dict[str, Any]) -> None:
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, "w", encoding="utf-8") as handle:
                json.dump(config, handle, indent=4)
        except Exception as exc:  # pragma: no cover - defensive
            print(f"Error saving config file {self.config_file}: {exc}", file=sys.stderr)
            sys.exit(1)

    def get_preferred_languages(self) -> List[str]:
        config = self.load()
        languages = config.get("preferred_languages", [])
        return [lang for lang in languages if isinstance(lang, str) and lang]

    def set_preferred_languages(self, languages: Iterable[str]) -> None:
        config = self.load()
        config["preferred_languages"] = [lang.strip() for lang in languages if lang and lang.strip()]
        self.save(config)
