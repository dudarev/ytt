"""Command line entrypoint for ytt."""

from __future__ import annotations

import sys
from typing import List

import pyperclip

from .application import ConfigService, FetchTranscriptUseCase, build_parser
from .domain import TranscriptService, extract_video_id
from .infrastructure import (
    CachedYouTubeTranscriptRepository,
    ClipboardGateway,
    ConfigRepository,
    PyperclipClipboardGateway,
    YouTubeMetadataGateway,
)


def _prepare_args(argv: List[str], clipboard: ClipboardGateway):
    parser = build_parser()
    if argv and argv[0] not in {"fetch", "config", "help"}:
        if "http://" in argv[0] or "https://" in argv[0]:
            argv = ["fetch", *argv]
    if not argv:
        try:
            clipboard_text = clipboard.read().strip()
        except pyperclip.PyperclipException:
            raise SystemExit(1)
        if not clipboard_text:
            print(
                "Error: Clipboard is empty. Provide a YouTube URL or use 'ytt --help'.",
                file=sys.stderr,
            )
            parser.print_help(sys.stderr)
            raise SystemExit(1)
        if not extract_video_id(clipboard_text):
            print(
                "Error: No YouTube URL found in clipboard. Provide a URL or use 'ytt --help'.",
                file=sys.stderr,
            )
            parser.print_help(sys.stderr)
            raise SystemExit(1)
        argv = ["fetch", clipboard_text]
    return parser, parser.parse_args(argv)


def main() -> None:
    argv = sys.argv[1:]
    clipboard = PyperclipClipboardGateway()
    parser, args = _prepare_args(argv, clipboard)

    config_repository = ConfigRepository()
    config_service = ConfigService(config_repository)
    metadata_gateway = YouTubeMetadataGateway()
    transcript_repository = CachedYouTubeTranscriptRepository(
        config_repository.cache_dir,
        metadata_gateway,
    )
    transcript_service = TranscriptService(transcript_repository)
    fetch_use_case = FetchTranscriptUseCase(
        transcript_service,
        config_service,
        clipboard,
    )

    if args.command == "help":
        parser.print_help()
        sys.exit(0)
    elif args.command == "config":
        if args.setting.lower() == "languages":
            languages = [lang.strip() for lang in args.value.split(",") if lang.strip()]
            config_service.set_preferred_languages(languages)
        else:
            print(f"Error: Unknown config setting '{args.setting}'. Only 'languages' is supported.", file=sys.stderr)
            raise SystemExit(1)
    elif args.command == "fetch":
        show_title = not (args.no_title or args.no_metadata)
        show_description = not (args.no_description or args.no_metadata)
        show_url = not (args.no_url or args.no_metadata)
        bundle = fetch_use_case.execute(
            args.youtube_url,
            copy_to_clipboard=not args.no_copy,
            show_title=show_title,
            show_description=show_description,
            show_url=show_url,
            input_url=args.youtube_url,
            refresh=args.refresh,
        )
        if bundle:
            FetchTranscriptUseCase.render(
                bundle,
                show_title=show_title,
                show_description=show_description,
                show_url=show_url,
                input_url=args.youtube_url,
            )
        else:
            raise SystemExit(1)
    else:  # pragma: no cover - defensive guard
        parser.print_help(sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
