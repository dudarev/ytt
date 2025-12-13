# Spec 004: Default to clipboard URL when no CLI parameters

- PRD: `docs/prds/004-clipboard-default-url.md`
- Plan: `docs/plans/004-clipboard-default-url.md`

## Overview
When YTT is invoked without arguments, the CLI should attempt to pull a YouTube URL from the clipboard and execute the standard `fetch` flow. This preserves existing invocation patterns while enabling a zero-argument "clipboard" mode.

## Architecture & Data Flow
- CLI entry (`src/ytt/main.py`) inspects `sys.argv[1:]`.
- If no arguments are supplied, the CLI will:
  - Attempt to read clipboard text via a new `ClipboardGateway.read()` API implemented in `PyperclipClipboardGateway`.
  - Validate clipboard contents using the existing `extract_video_id` helper to ensure the string contains a recognizable YouTube URL or Markdown link.
  - If valid, synthesize CLI arguments equivalent to `ytt fetch <clipboard-url>` and continue through the existing parsing and execution path.
- Errors (clipboard read failure or missing/invalid URL) produce actionable messages and exit with status 1.

## CLI/UX Behavior
- `ytt` (no args):
  - Success path: uses clipboard URL, behaves like `ytt fetch <url>` including honoring default metadata and clipboard copy options.
  - Failure modes:
    - Clipboard unavailable/exception: print warning to stderr including the underlying pyperclip error and exit 1.
    - Clipboard text lacks a YouTube URL: print a concise message (e.g., "No YouTube URL found in clipboard. Provide a URL or use 'ytt --help'.") to stderr and exit 1.
- Existing commands (`ytt <url>`, `ytt fetch <url>`, `ytt config ...`) remain unchanged.

## Error Handling
- Catch `pyperclip.PyperclipException` during clipboard read and emit a warning similar to the copy pathway.
- Do not fall back to help text when clipboard lookup fails; exit with status 1 after printing a diagnostic.

## Test Strategy
- Unit tests under `tests/unit/ytt/main/test_main.py` covering:
  - No-arg invocation with valid clipboard URL triggers fetch flow and passes URL through.
  - Clipboard missing/exception raises warning and exits with code 1.
  - Clipboard text without YouTube URL emits the invalid URL message and exits with code 1.
- Adjust any shared helpers to facilitate injection/mocking of clipboard gateway and clipboard content.
