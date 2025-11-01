"""Command line interface definitions."""

from __future__ import annotations

import argparse

from ..version import get_version


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch YouTube video transcripts or manage configuration.",
        usage="ytt <youtube_url> | ytt config <setting> <value>",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {get_version()}",
        help="Show the ytt version and exit.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    fetch_parser = subparsers.add_parser(
        "fetch",
        help="Fetch transcript for a given URL (default command if none specified)",
    )
    fetch_parser.add_argument("youtube_url", help="The URL of the YouTube video.")
    fetch_parser.add_argument(
        "--no-copy",
        action="store_true",
        help="Do not copy the transcript to the clipboard.",
    )
    fetch_parser.add_argument(
        "--no-title",
        action="store_true",
        help="Do not print the video title before the transcript.",
    )
    fetch_parser.add_argument(
        "--no-description",
        action="store_true",
        help="Do not print the video description before the transcript.",
    )
    fetch_parser.add_argument(
        "--no-url",
        action="store_true",
        help="Do not print the video URL as the first line.",
    )
    fetch_parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="Disable URL, title, and description output.",
    )

    config_parser = subparsers.add_parser("config", help="Configure ytt settings.")
    config_parser.add_argument(
        "setting",
        help="The configuration setting to modify (e.g., languages).",
    )
    config_parser.add_argument(
        "value",
        help="The value to set for the setting (e.g., 'en,es,fr').",
    )

    return parser
