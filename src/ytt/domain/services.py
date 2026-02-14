"""Domain services and interfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol, Sequence

from .entities import VideoMetadata, VideoTranscriptBundle
from .value_objects import VideoID


class TranscriptRepository(Protocol):
    """Port that retrieves transcripts for a video."""

    def retrieve(
        self,
        video_id: VideoID,
        preferred_languages: Sequence[str],
        *,
        refresh: bool = False,
    ) -> Optional[VideoTranscriptBundle]:
        """Return transcript bundle for ``video_id`` or ``None`` if unavailable."""


class MetadataGateway(Protocol):
    """Port that resolves metadata for a video."""

    def fetch(self, video_id: VideoID) -> VideoMetadata:
        """Fetch metadata for ``video_id``."""


@dataclass
class TranscriptService:
    """Application-facing domain service for transcripts."""

    repository: TranscriptRepository

    def fetch(
        self,
        video_id: VideoID,
        preferred_languages: Sequence[str],
        *,
        refresh: bool = False,
    ) -> Optional[VideoTranscriptBundle]:
        """Fetch transcript bundle using the configured repository."""

        languages = list(preferred_languages)
        return self.repository.retrieve(video_id, languages, refresh=refresh)
