---
title: 002-markdown-link-video-id
status: draft
owner: gpt-5-codex
last-updated: 2025-10-18
links: { prd: docs/prds/002-markdown-link-video-id.md, plan: docs/plans/002-markdown-link-video-id.md, tasks: null, adrs: [] }
---

## Overview
- Extend `extract_video_id` to detect and unwrap Markdown link syntax before running existing URL parsing logic, enabling CLI and library consumers to paste Markdown-formatted YouTube links without manual cleanup.

## Architecture
- Keep the parsing logic inside `domain.value_objects.extract_video_id` to avoid leaking Markdown concerns across layers.
- Add a lightweight Markdown link detector that strips the square-bracket label and isolates the URL within parentheses when the string matches `[label](url)` or `![alt](url)` patterns.
- Reuse the existing URL parsing flow (`urllib.parse.urlparse`) after extracting the URL; no new dependencies introduced.

## Data & API Contracts
- `extract_video_id` continues to accept a `str` input and return `Optional[VideoID]`.
- On Markdown input, the function should return the same `VideoID` as if called with the raw URL; otherwise `None`.
- No other public interfaces change, so downstream callers (CLI, library functions) benefit automatically.

## CLI / UX Behavior
- Commands like `ytt fetch "[Title](https://www.youtube.com/watch?v=abc123)"` succeed and fetch transcripts using `abc123`.
- Help text or documentation gains a brief note that Markdown links are supported (to be updated separately if desired).

## Error Handling
- If Markdown parsing fails (malformed brackets/parentheses), fall back to existing URL parsing; no new exceptions are raised.
- Invalid or empty inputs still return `None` without raising.

## Telemetry / Performance
- Negligible performance impact due to simple string checks; no telemetry updates needed.

## Test Strategy
- Unit tests covering Markdown watch URLs, short links, embed paths, query params.
- Regression tests ensuring non-Markdown inputs (including partial Markdown) still behave as before.

## Dependencies
- No new packages required; rely on standard library only.

## Links
- PRD: docs/prds/002-markdown-link-video-id.md
- Plan: docs/plans/002-markdown-link-video-id.md
