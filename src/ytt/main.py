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
    YouTubeMetadataGateway,
)


def _prepare_args(argv: List[str]):
    parser = build_parser()
    if argv and argv[0] not in {"fetch", "config"}:
        if "http://" in argv[0] or "https://" in argv[0]:
            argv = ["fetch", *argv]
    if not argv:
        parser.print_help(sys.stderr)
        raise SystemExit(1)
    return parser, parser.parse_args(argv)


def main() -> None:
    argv = sys.argv[1:]
    parser, args = _prepare_args(argv)

    config_repository = ConfigRepository()
    config_service = ConfigService(config_repository)
    metadata_gateway = YouTubeMetadataGateway()
    transcript_repository = CachedYouTubeTranscriptRepository(
        config_repository.cache_dir,
        metadata_gateway,
    )
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
        bundle = fetch_use_case.execute(
            args.youtube_url,
            copy_to_clipboard=not args.no_copy,
        )
        if bundle:
            show_title = not (args.no_title or args.no_metadata)
            show_description = not (args.no_description or args.no_metadata)
            FetchTranscriptUseCase.render(
                bundle,
                show_title=show_title,
                show_description=show_description,
            )
        else:
            raise SystemExit(1)
    else:  # pragma: no cover - defensive guard
        parser.print_help(sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
