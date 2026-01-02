"""Use case for fetching transcripts."""

from __future__ import annotations

import sys
from typing import Callable, Optional, Sequence

from ..domain import (
    TranscriptService,
    VideoID,
    VideoTranscriptBundle,
    extract_video_id,
)
from ..infrastructure.clipboard import ClipboardGateway
from .config_service import ConfigService


class FetchTranscriptUseCase:
    """Coordinates fetching transcripts for the CLI."""

    def __init__(
        self,
        transcript_service: TranscriptService,
        config_service: ConfigService,
        clipboard: ClipboardGateway,
        extractor: Optional[Callable[[str], Optional[VideoID]]] = None,
    ) -> None:
        self._service = transcript_service
        self._config_service = config_service
        self._clipboard = clipboard
        self._extractor = extractor or extract_video_id

    def _resolve_preferred_languages(self) -> Sequence[str]:
        languages = list(self._config_service.get_preferred_languages())
        if not languages:
            print("Error: Preferred languages not set in configuration.", file=sys.stderr)
            print("Please set them using: ytt config languages <lang1>,<lang2>,...", file=sys.stderr)
            print("Example: ytt config languages en,es,fr", file=sys.stderr)
            raise SystemExit(1)
        return languages

    def _ensure_video_id(self, url: str) -> VideoID:
        video_id = self._extractor(url)
        if video_id is None:
            print(f"Error: Could not extract video ID from URL: {url}", file=sys.stderr)
            print(
                'Tip: Wrap the URL in quotes in your shell (e.g., ytt "https://www.youtube.com/watch?v=VIDEO_ID").',
                file=sys.stderr,
            )
            raise SystemExit(1)
        if isinstance(video_id, VideoID):
            return video_id
        return VideoID(str(video_id))

    def execute(
        self,
        url: str,
        *,
        copy_to_clipboard: bool = True,
        show_title: bool = True,
        show_description: bool = True,
        show_url: bool = True,
        input_url: Optional[str] = None,
    ) -> Optional[VideoTranscriptBundle]:
        video_id = self._ensure_video_id(url)
        languages = self._resolve_preferred_languages()
        bundle = self._service.fetch(video_id, languages)
        if not bundle:
            return None
        if copy_to_clipboard:
            lines = self.render_lines(
                bundle,
                show_title=show_title,
                show_description=show_description,
                show_url=show_url,
                input_url=input_url or url,
            )
            self._clipboard.copy(lines)
        return bundle

    @staticmethod
    def render_lines(
        bundle: Optional[VideoTranscriptBundle],
        *,
        show_title: bool = True,
        show_description: bool = True,
        show_url: bool = True,
        input_url: Optional[str] = None,
    ) -> list[str]:
        if not bundle:
            return []
        metadata = bundle.metadata
        lines: list[str] = []
        # Prepend canonical URL if requested
        if show_url and input_url:
            try:
                video_id = extract_video_id(input_url)
                if video_id:
                    lines.append(f"https://www.youtube.com/watch?v={video_id.value}")
                    lines.append("")
            except Exception:
                # Defensive: if URL extraction fails, skip URL line and continue
                pass
        if show_title and metadata.title:
            lines.append(f"# {metadata.title}")
            lines.append("")
        if show_description and metadata.description:
            lines.append("## Description")
            lines.append("")
            lines.append(metadata.description)
            lines.append("")
        lines.append("## Transcript")
        lines.append("")
        lines.extend(line.text for line in bundle.transcript)
        return lines

    @staticmethod
    def render(
        bundle: Optional[VideoTranscriptBundle],
        *,
        show_title: bool = True,
        show_description: bool = True,
        show_url: bool = True,
        input_url: Optional[str] = None,
    ) -> None:
        for line in FetchTranscriptUseCase.render_lines(
            bundle,
            show_title=show_title,
            show_description=show_description,
            show_url=show_url,
            input_url=input_url,
        ):
            print(line)
