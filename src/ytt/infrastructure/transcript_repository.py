"""Transcript repository backed by the YouTube API and local cache."""

from __future__ import annotations

import pickle
import sys
from pathlib import Path
from typing import Iterable, Optional, Sequence

from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    YouTubeTranscriptApi,
)

from ..domain.entities import TranscriptLine
from ..domain.services import TranscriptRepository
from ..domain.value_objects import VideoID


class CachedYouTubeTranscriptRepository(TranscriptRepository):
    """Repository that stores transcripts locally and falls back to the API."""

    def __init__(self, cache_dir: Path) -> None:
        self._cache_dir = cache_dir

    def retrieve(self, video_id: VideoID, preferred_languages: Sequence[str]) -> Optional[list[TranscriptLine]]:
        cache_path = self._cache_path(video_id, preferred_languages)

        if cache_path.exists():
            cached = self._load_cache(cache_path)
            if cached is not None:
                return cached

        transcript_data = self._fetch_from_api(video_id, preferred_languages)
        if transcript_data is not None:
            transcript = self._to_transcript(transcript_data)
            self._save_cache(cache_path, transcript)
            return transcript
        return None

    def _cache_path(self, video_id: VideoID, preferred_languages: Sequence[str]) -> Path:
        languages = sorted({lang.lower() for lang in preferred_languages if lang})
        lang_key = "_".join(languages) if languages else "any"
        return self._cache_dir / f"{video_id.value}_{lang_key}.pkl"

    def _load_cache(self, cache_path: Path) -> Optional[list[TranscriptLine]]:
        try:
            with open(cache_path, "rb") as handle:
                return pickle.load(handle)
        except pickle.UnpicklingError:
            print(f"Warning: Could not unpickle cache file {cache_path}. Fetching again.", file=sys.stderr)
        except FileNotFoundError:
            print(f"Warning: Cache file not found {cache_path} despite check. Fetching again.", file=sys.stderr)
        except Exception as exc:  # pragma: no cover - defensive
            print(f"Warning: Error reading cache file {cache_path}: {exc}. Fetching again.", file=sys.stderr)
        return None

    def _save_cache(self, cache_path: Path, transcript: list[TranscriptLine]) -> None:
        try:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_path, "wb") as handle:
                pickle.dump(transcript, handle)
        except Exception as exc:  # pragma: no cover - defensive
            print(f"Warning: Could not save transcript to cache file {cache_path}: {exc}", file=sys.stderr)

    def _fetch_from_api(self, video_id: VideoID, preferred_languages: Sequence[str]) -> Optional[Iterable[dict]]:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id.value)
            transcript_object = self._find_transcript_object(transcript_list, preferred_languages)
            if transcript_object is None:
                print(
                    f"Error: Could not find a suitable transcript object for video ID: {video_id.value}",
                    file=sys.stderr,
                )
                return None
            return transcript_object.fetch()
        except NoTranscriptFound:
            languages = preferred_languages if preferred_languages else ["any"]
            print(
                f"Error: No transcript found for video ID: {video_id.value} (tried languages: {', '.join(languages)})",
                file=sys.stderr,
            )
        except TranscriptsDisabled:
            print(f"Error: Transcripts are disabled for video ID: {video_id.value}", file=sys.stderr)
        except Exception as exc:  # pragma: no cover - defensive
            print(f"An unexpected error occurred during API fetch: {exc}", file=sys.stderr)
        return None

    @staticmethod
    def _find_transcript_object(transcript_list, preferred_languages: Sequence[str]):
        manual_transcripts = [t for t in transcript_list if not t.is_generated]

        if len(manual_transcripts) == 1:
            return manual_transcripts[0]

        if manual_transcripts and preferred_languages:
            for lang in preferred_languages:
                for transcript in manual_transcripts:
                    if transcript.language == lang:
                        return transcript

        if preferred_languages:
            try:
                return transcript_list.find_generated_transcript(preferred_languages)
            except NoTranscriptFound:
                pass

        if manual_transcripts:
            return manual_transcripts[0]

        generated_transcripts = [t for t in transcript_list if t.is_generated]
        if generated_transcripts:
            return generated_transcripts[0]

        raise NoTranscriptFound("No suitable transcript found in the list.")

    @staticmethod
    def _to_transcript(entries: Iterable) -> list[TranscriptLine]:
        transcript: list[TranscriptLine] = []
        for entry in entries:
            text = entry.text
            start = float(entry.start)
            duration = float(entry.duration)
            transcript.append(TranscriptLine(text=text, start=start, duration=duration))
        return transcript
