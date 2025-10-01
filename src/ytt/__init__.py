"""Public package interface for ytt."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional, Sequence

import pyperclip  # re-exported for backwards compatibility

from .domain import TranscriptService, VideoID, VideoTranscriptBundle, extract_video_id
from .domain.entities import TranscriptLine, VideoMetadata
from .infrastructure import (
    CachedYouTubeTranscriptRepository,
    ConfigRepository,
    PyperclipClipboardGateway,
    YouTubeMetadataGateway,
)
from .main import main
from .version import get_version

__version__ = get_version()

__all__ = [
    "main",
    "extract_video_id",
    "get_config_dir",
    "get_cache_dir",
    "get_config_file_path",
    "load_config",
    "save_config",
    "get_transcript",
    "get_video_metadata",
    "get_video_bundle",
    "copy_to_clipboard",
    "__version__",
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
    repository = CachedYouTubeTranscriptRepository(
        _config_repository().cache_dir,
        YouTubeMetadataGateway(),
    )
    service = TranscriptService(repository)
    bundle = service.fetch(VideoID(video_id), languages)
    if bundle:
        return bundle.transcript
    return None


def get_video_metadata(video_id: str) -> Optional[VideoMetadata]:
    repository = CachedYouTubeTranscriptRepository(
        _config_repository().cache_dir,
        YouTubeMetadataGateway(),
    )
    service = TranscriptService(repository)
    bundle = service.fetch(VideoID(video_id), [])
    if bundle:
        return bundle.metadata
    return None


def get_video_bundle(
    video_id: str, preferred_languages: Optional[Sequence[str]] = None
) -> Optional[VideoTranscriptBundle]:
    languages = list(preferred_languages or [])
    repository = CachedYouTubeTranscriptRepository(
        _config_repository().cache_dir,
        YouTubeMetadataGateway(),
    )
    service = TranscriptService(repository)
    return service.fetch(VideoID(video_id), languages)


def copy_to_clipboard(transcript: Iterable[TranscriptLine]) -> bool:
    gateway = PyperclipClipboardGateway()
    return gateway.copy(line.text for line in transcript)
