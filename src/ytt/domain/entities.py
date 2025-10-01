"""Domain entities for transcript handling."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VideoMetadata:
    """Describes metadata associated with a YouTube video."""

    title: str | None
    description: str | None


@dataclass(frozen=True)
class VideoTranscriptBundle:
    """Container that groups transcript lines with their metadata."""

    transcript: list["TranscriptLine"]
    metadata: VideoMetadata


@dataclass(frozen=True)
class TranscriptLine:
    """Represents a single line within a transcript."""

    text: str
    start: float
    duration: float


Transcript = list[TranscriptLine]
"""Convenience alias representing an ordered transcript."""
