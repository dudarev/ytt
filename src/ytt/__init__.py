"""Public package interface for ytt."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional, Sequence

import pyperclip  # re-exported for backwards compatibility

from .domain import TranscriptService, VideoID, extract_video_id
from .domain.entities import TranscriptLine
from .infrastructure import (
    CachedYouTubeTranscriptRepository,
    ConfigRepository,
    PyperclipClipboardGateway,
)
from .main import main

__all__ = [
    "main",
    "extract_video_id",
    "get_config_dir",
    "get_cache_dir",
    "get_config_file_path",
    "load_config",
    "save_config",
    "get_transcript",
    "copy_to_clipboard",
]


def _config_repository() -> ConfigRepository:
    return ConfigRepository()


def get_config_dir() -> Path:
    return _config_repository().config_dir


def get_cache_dir() -> Path:
    return _config_repository().cache_dir


def get_config_file_path() -> Path:
    return _config_repository().config_file


def load_config() -> dict:
    return _config_repository().load()


def save_config(config: dict) -> None:
    _config_repository().save(config)


def get_transcript(video_id: str, preferred_languages: Optional[Sequence[str]] = None) -> Optional[list[TranscriptLine]]:
    languages = list(preferred_languages or [])
    repository = CachedYouTubeTranscriptRepository(_config_repository().cache_dir)
    service = TranscriptService(repository)
    return service.fetch(VideoID(video_id), languages)


def copy_to_clipboard(transcript: Iterable[TranscriptLine]) -> bool:
    gateway = PyperclipClipboardGateway()
    return gateway.copy(line.text for line in transcript)
