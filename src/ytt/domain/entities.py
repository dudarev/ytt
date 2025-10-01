"""Domain entities for transcript handling."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TranscriptLine:
    """Represents a single line within a transcript."""

    text: str
    start: float
    duration: float


Transcript = list[TranscriptLine]
"""Convenience alias representing an ordered transcript."""
