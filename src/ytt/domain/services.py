"""Domain services and interfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol, Sequence

from .entities import TranscriptLine
from .value_objects import VideoID


class TranscriptRepository(Protocol):
    """Port that retrieves transcripts for a video."""

    def retrieve(self, video_id: VideoID, preferred_languages: Sequence[str]) -> Optional[list[TranscriptLine]]:
        """Return a transcript for ``video_id`` or ``None`` if unavailable."""


@dataclass
class TranscriptService:
    """Application-facing domain service for transcripts."""

    repository: TranscriptRepository

    def fetch(self, video_id: VideoID, preferred_languages: Sequence[str]) -> Optional[list[TranscriptLine]]:
        """Fetch a transcript using the configured repository."""

        languages = list(preferred_languages)
        return self.repository.retrieve(video_id, languages)
