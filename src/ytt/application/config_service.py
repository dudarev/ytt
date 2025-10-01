"""Application service for configuration operations."""

from __future__ import annotations

from typing import Iterable, List

from ..infrastructure.config import ConfigRepository


class ConfigService:
    """Facade for working with configuration storage."""

    def __init__(self, repository: ConfigRepository) -> None:
        self._repository = repository

    def get_preferred_languages(self) -> List[str]:
        return self._repository.get_preferred_languages()

    def set_preferred_languages(self, languages: Iterable[str]) -> None:
        self._repository.set_preferred_languages(languages)
