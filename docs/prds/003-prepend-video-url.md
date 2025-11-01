# PRD 003: Prepend canonical video URL to output

## Description
- Expand the YouTube Transcript Tool (YTT) to prepend the canonical video URL as the first line of all output by default.
- Include the canonical URL in both standard output and clipboard content.
- Make the URL line toggleable via a new `--no-url` flag and honor `--no-metadata` as a disable-all switch.
- Ensure the URL is canonicalized (always `https://www.youtube.com/watch?v=<VIDEO_ID>`) regardless of input format.

## Problem Statement
When pasting YTT output into AI agents, notes, or summaries, users frequently need to include the source video URL for traceability. Currently, users must paste the URL separately or manually locate it from their clipboard history.

## Users / Jobs to Be Done
- CLI users who paste transcripts into AI tools (e.g., ChatGPT, Claude) for summarization and want the source video URL included automatically for reference.
- Users who maintain transcript archives and want the video URL present in all exports for linkage.

## Goals
- Print the canonical YouTube URL (`https://www.youtube.com/watch?v=<VIDEO_ID>`) as the first line of standard output by default.
- Include the same URL at the top of clipboard text when copying is enabled.
- Provide a `--no-url` flag to suppress the URL line when not needed.
- Ensure `--no-metadata` disables URL, title, and description for users who want transcript-only output.

## Non-Goals
- Fetching additional metadata (e.g., view counts, channel info) beyond title and description.
- Adding rich link rendering (e.g., Markdown link syntax `[Video](url)`); plain URL only.
- Persisting URLs in caches or external storage.

## Success Metrics
- Majority of users receive the canonical URL as the first line without additional steps.
- No regressions to existing CLI flags or transcript extraction functionality.
- Users can opt out via `--no-url` and `--no-metadata`.

## Acceptance Criteria
- AC1: Running `ytt fetch <any supported YouTube URL or Markdown link>` (default options) prints the canonical URL (`https://www.youtube.com/watch?v=<VIDEO_ID>`) as the first line of stdout.
- AC2: The clipboard content (when not using `--no-copy`) also starts with the canonical URL line.
- AC3: Running `ytt fetch <url> --no-url` suppresses the URL line in both stdout and clipboard; title/description and transcript remain.
- AC4: Running `ytt fetch <url> --no-metadata` suppresses URL, title, and description; only transcript header and lines appear.
- AC5: The canonical URL is derived from extracted `VideoID` and works with watch URLs, youtu.be, embed, /v, YouTube Shorts, and Markdown link inputs.
- AC6: If the input URL cannot be parsed (edge case), the tool skips the URL line defensively but continues processing the transcript.

## Key Risks & Assumptions
- **Risk**: Some users or scripts may parse the first line and expect the title or transcript content instead of the URL.
  - **Mitigation**: Provide `--no-url` to opt out, document the new default in README and changelog, and ensure `--no-metadata` also disables it.
  - Treat this as a minor feature (non-breaking API in terms of behavior; clarified in release notes).

## References
- Spec: `docs/specs/003-prepend-video-url.md`
- Plan: `docs/plans/003-prepend-video-url.md`
