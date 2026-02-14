# Spec 006: Clipboard fallback for URL-less fetch flag invocations

- PRD: `docs/prds/006-clipboard-fallback-for-fetch-flags.md`
- Plan: `docs/plans/006-clipboard-fallback-for-fetch-flags.md`

## Overview
Allow fetch invocations that omit a URL to derive it from clipboard when they are clearly fetch-like calls (for example `ytt fetch --refresh` and `ytt --refresh`).

## Architecture & Data Flow
- CLI parser (`src/ytt/application/cli.py`):
  - Make `fetch` positional `youtube_url` optional (`nargs="?"`).
- Arg preparation (`src/ytt/main.py`):
  - Infer `fetch` for top-level invocations where all args are known fetch flags.
  - Preserve URL auto-prefix behavior for direct URLs.
  - Preserve top-level handling for global flags (`--help`, `-h`, `--version`, `-V`).
  - Centralize clipboard read/validation for cases where `fetch` has no URL.

## CLI/UX Behavior
- Works:
  - `ytt`
  - `ytt fetch --refresh`
  - `ytt --refresh`
  - `ytt --no-copy --refresh` (and similar fetch-only flags)
- Remains unchanged:
  - `ytt --help`, `ytt --version`
  - `ytt fetch <url> ...`
- Still errors:
  - Unknown top-level flags (argparse error code 2)

## Error Handling
- When clipboard is empty: print current "Clipboard is empty..." message and help text.
- When clipboard content is not a YouTube URL: print current "No YouTube URL found..." message and help text.
- When clipboard read raises `PyperclipException`: preserve existing warning behavior and exit code.

## Test Strategy
- Unit tests for `_prepare_args`:
  - URL-less fetch + flag uses clipboard.
  - Top-level refresh uses clipboard.
  - Empty/invalid clipboard in both new paths.
  - `--help` not rewritten to fetch.
  - Unknown top-level flag remains argparse error.
- Integration-style CLI tests:
  - `ytt.py fetch --refresh` executes fetch and passes `refresh=True`.
  - `ytt.py --refresh` executes fetch and passes `refresh=True`.
- Run full suite with `pytest -q`.
