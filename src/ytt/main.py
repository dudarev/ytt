"""Command line entrypoint for ytt."""

from __future__ import annotations

import sys
from typing import List

from .application import ConfigService, FetchTranscriptUseCase, build_parser
from .domain import TranscriptService
from .infrastructure import (
    CachedYouTubeTranscriptRepository,
    ConfigRepository,
    PyperclipClipboardGateway,
)


def _prepare_args(argv: List[str]):
    parser = build_parser()
    if not argv or argv[0] not in {"fetch", "config"}:
        if argv and ("http://" in argv[0] or "https://" in argv[0]):
            argv = ["fetch", *argv]
        else:
            parser.print_help(sys.stderr)
            raise SystemExit(1)
    return parser, parser.parse_args(argv)


def main() -> None:
    argv = sys.argv[1:]
    parser, args = _prepare_args(argv)

    config_repository = ConfigRepository()
    config_service = ConfigService(config_repository)
    transcript_repository = CachedYouTubeTranscriptRepository(config_repository.cache_dir)
    transcript_service = TranscriptService(transcript_repository)
    clipboard = PyperclipClipboardGateway()

    fetch_use_case = FetchTranscriptUseCase(
        transcript_service,
        config_service,
        clipboard,
    )

    if args.command == "config":
        if args.setting.lower() == "languages":
            languages = [lang.strip() for lang in args.value.split(",") if lang.strip()]
            config_service.set_preferred_languages(languages)
        else:
            print(f"Error: Unknown config setting '{args.setting}'. Only 'languages' is supported.", file=sys.stderr)
            raise SystemExit(1)
    elif args.command == "fetch":
        transcript = fetch_use_case.execute(args.youtube_url, copy_to_clipboard=not args.no_copy)
        if transcript:
            FetchTranscriptUseCase.render(transcript)
        else:
            raise SystemExit(1)
    else:  # pragma: no cover - defensive guard
        parser.print_help(sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
