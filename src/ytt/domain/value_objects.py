"""Domain value objects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from urllib.parse import parse_qs, urlparse


@dataclass(frozen=True)
class VideoID:
    """Immutable representation of a YouTube video identifier."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("VideoID cannot be empty")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.value


def extract_video_id(url: str) -> Optional[VideoID]:
    """Extract a :class:`VideoID` from a YouTube URL."""

    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    if parsed_url.netloc in {"www.youtube.com", "youtube.com"} and parsed_url.path == "/watch" and "v" in query_params:
        return VideoID(query_params["v"][0])

    if parsed_url.netloc == "youtu.be" and parsed_url.path:
        return VideoID(parsed_url.path.lstrip("/"))

    if parsed_url.path.startswith("/embed/"):
        parts = parsed_url.path.split("/")
        if len(parts) > 2:
            return VideoID(parts[2])

    if parsed_url.path.startswith("/v/"):
        parts = parsed_url.path.split("/")
        if len(parts) > 2:
            return VideoID(parts[2])

    if parsed_url.path.startswith("/shorts/"):
        parts = parsed_url.path.split("/")
        if len(parts) > 2:
            return VideoID(parts[2])

    return None
