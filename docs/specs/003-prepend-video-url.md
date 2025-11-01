---
title: 003-prepend-video-url
status: draft
owner: gpt-5-codex
last-updated: 2025-11-01
links: { prd: ../prds/003-prepend-video-url.md, plan: ../plans/003-prepend-video-url.md, tasks: null, adrs: [] }
---

## Overview
- Add a single plain URL line at the top of both standard output and clipboard content.
- Format: `https://www.youtube.com/watch?v=<VIDEO_ID>` derived from extracted VideoID (canonicalized), not the raw input.
- Controlled by a new `--no-url` flag; also disabled by `--no-metadata`.

## Functional Requirements
- FR1: Canonicalize the input URL to a standard YouTube watch URL using the extracted VideoID.
- FR2: Print the canonical URL as the first line of stdout by default.
- FR3: Include the canonical URL as the first line of clipboard content when `--no-copy` is not set.
- FR4: Provide a `--no-url` CLI flag to suppress the URL line.
- FR5: Ensure `--no-metadata` disables URL in addition to title and description.
- FR6: If the input URL cannot be parsed (edge case), skip the URL line defensively and continue processing.

## Acceptance Criteria
- AC1: Default output (no flags): first line is canonical URL, blank line, then title/description/transcript sections.
- AC2: Running with `--no-url`: URL line absent; title/description/transcript proceed as normal.
- AC3: Running with `--no-metadata`: URL, title, description absent; only transcript section shown.
- AC4: Markdown links, youtu.be, /v paths, embed URLs, and Shorts links all canonicalize to the standard watch URL.
- AC5: Clipboard content mirrors stdout: starts with canonical URL, respects `--no-url` and `--no-metadata`.

## CLI/UX Behavior

### Default Flow
```
https://www.youtube.com/watch?v=VIDEO_ID

# Video Title

## Description
Description text here.

## Transcript
[transcript lines]
```

### With `--no-url`
```
# Video Title

## Description
Description text here.

## Transcript
[transcript lines]
```

### With `--no-metadata`
```
## Transcript
[transcript lines]
```

### Flag Precedence
- `--no-url`: suppress URL line only; title/description/transcript unchanged.
- `--no-title`: suppress title; URL/description/transcript unchanged.
- `--no-description`: suppress description; URL/title/transcript unchanged.
- `--no-metadata`: suppress URL, title, and description; only transcript shown.

## Data Contracts & Code Changes

### High-Level API Changes
- `application/cli.py`:
  - Add `--no-url` argument (store_true).
  - Update `--no-metadata` help text to "Disable URL, title, and description output."
- `main.py`:
  - Compute `show_url = not (args.no_url or args.no_metadata)`.
  - Pass `show_url` and `input_url` to `FetchTranscriptUseCase.execute()` and `render()`.
- `application/fetch_service.py`:
  - `execute(..., show_url: bool = True, input_url: str | None = None, ...) -> str`.
  - `render(..., show_url: bool = True, input_url: str | None = None) -> str`.
  - `render_lines(..., show_url: bool = True, input_url: str | None = None) -> Iterator[str]`.
  - If `show_url` and `input_url` is provided:
    - Extract VideoID via `extract_video_id(input_url)`.
    - Construct canonical URL: `https://www.youtube.com/watch?v={video_id.value}`.
    - Yield the URL as the first line, followed by a blank line.
  - If `show_url` but no valid `input_url`, skip URL line (defensive).

### Domain / Infrastructure
- No changes to domain entities or value objects.
- VideoID extraction already available in `domain/value_objects.py`.

## Test Strategy
- **Unit tests**: Verify URL canonicalization logic in isolation; test fallback when input_url is missing.
- **Integration tests** (`tests/test_ytt.py`):
  - Default run: assert first output line is the canonical URL.
  - `--no-url`: assert URL is absent; title/description/transcript present.
  - `--no-metadata`: assert URL/title/description absent; only transcript shown.
  - Markdown link input: verify canonicalization works.
  - Clipboard content mirrors stdout regarding URL presence.
  - Flag combinations: e.g., `--no-url --no-title` (URL absent, title absent, description shown).

## Telemetry / Performance
- Negligible impact; URL is constructed once per invocation.

## Error Handling
- If `input_url` cannot be parsed or is None:
  - Log a debug/info message (optional).
  - Skip URL line and continue; do not fail.
- Transcript fetch/rendering errors unchanged.

## Release & Documentation
- **Version bump**: 0.7.0 (minor feature).
- **CHANGELOG.md entry**:
  ```
  ## [0.7.0] - 2025-11-01
  
  ### Added
  - Print the canonical video URL (`https://www.youtube.com/watch?v=<VIDEO_ID>`) as the first line of output by default.
  - Added `--no-url` flag to suppress the URL line when not needed.
  
  ### Changed
  - `--no-metadata` now disables URL, title, and description output (previously only title and description).
  ```
- **README.md**: Add usage note: "By default, the first line of output is the canonical video URL; use `--no-url` to suppress it."

## Notes
- Defaulting ON prioritizes usability and traceability for AI summarization workflows; opt-out mitigates any breaking expectations.
- Canonical URL is always the watch format for consistency, even if input was Shorts or youtu.be.
