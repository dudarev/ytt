"""Use case for fetching transcripts."""

from __future__ import annotations

import sys
from typing import Callable, Iterable, Optional, Sequence

from ..domain import TranscriptLine, TranscriptService, VideoID, extract_video_id
from ..infrastructure.clipboard import ClipboardGateway
from ..infrastructure.config import ConfigRepository


class FetchTranscriptUseCase:
    """Coordinates fetching transcripts for the CLI."""

    def __init__(
        self,
        transcript_service: TranscriptService,
        config_repository: ConfigRepository,
        clipboard: ClipboardGateway,
        extractor: Callable[[str], Optional[VideoID]] = extract_video_id,
        languages_provider: Optional[Callable[[], Sequence[str]]] = None,
        transcript_fetcher: Optional[Callable[[str, Sequence[str]], Optional[list[TranscriptLine]]]] = None,
    ) -> None:
        self._service = transcript_service
        self._config_repository = config_repository
        self._clipboard = clipboard
        self._extractor = extractor
        self._languages_provider = languages_provider
        self._transcript_fetcher = transcript_fetcher

    def _resolve_preferred_languages(self) -> Sequence[str]:
        if self._languages_provider is not None:
            languages = list(self._languages_provider())
        else:
            languages = self._config_repository.get_preferred_languages()
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
            raise SystemExit(1)
        if isinstance(video_id, VideoID):
            return video_id
        return VideoID(str(video_id))

    def execute(self, url: str, copy_to_clipboard: bool = True) -> Optional[list[TranscriptLine]]:
        video_id = self._ensure_video_id(url)
        languages = self._resolve_preferred_languages()
        if self._transcript_fetcher is not None:
            transcript = self._transcript_fetcher(video_id.value, languages)
        else:
            transcript = self._service.fetch(video_id, languages)
        if not transcript:
            return None
        if copy_to_clipboard:
            self._clipboard.copy(line.text for line in transcript)
        return transcript

    @staticmethod
    def render(transcript: Optional[Iterable[TranscriptLine]]) -> None:
        if not transcript:
            return
        for line in transcript:
            print(line.text)
