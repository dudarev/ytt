# PRD 0002: Extract Video IDs from Markdown Links

## Problem Statement
- Users often copy Markdown-formatted YouTube links (e.g., `[Video Title](https://www.youtube.com/watch?v=abc123&t=2s)`) directly into the CLI or Python API.
- The current `extract_video_id` utility only handles raw URLs, causing Markdown-formatted input to fail and requiring manual cleanup before use.
- This friction undermines the tool's ergonomics, especially for workflows that paste links from documentation or chat transcripts.

## Users / Jobs To Be Done
- **CLI users** who want to paste Markdown links collected from note-taking tools and immediately fetch transcripts.
- **Library consumers** integrating `extract_video_id` into automation scripts that receive Markdown links from upstream systems.

## Goals
- Accept Markdown-style link strings wherever YouTube URLs are supported today (CLI commands, library helpers).
- Preserve existing behavior for plain URLs and already-supported YouTube link variants.

## Non-Goals
- Parsing arbitrary markup languages beyond Markdown link syntax.
- Performing URL validation beyond extracting the `v` parameter or canonical video path.
- Handling non-YouTube providers or playlist/document links.

## Success Metrics
- Zero regressions in existing URL extraction paths (short links, embed URLs, shorts, etc.).
- 100% of Markdown link inputs covered by the documented syntax extract the same video ID as their raw URL counterparts.
- No new user-facing configuration required to enable the behavior.

## Acceptance Criteria
- Given a Markdown link string with a standard YouTube watch URL inside parentheses, when passed to `extract_video_id`, then the function returns the same `VideoID` as when given the raw URL.
- Given a Markdown link string with a youtu.be short URL, when passed to `extract_video_id`, then the function returns the corresponding short link video ID.
- Given input that is neither a valid URL nor a Markdown link containing one, `extract_video_id` continues to return `None`.
- CLI commands that accept video identifiers (e.g., `ytt fetch <url>`) accept Markdown link strings with no additional flags.

## Key Risks / Assumptions
- Assumes Markdown link inputs do not contain nested parentheses that would break simple parsing.
- Potential side effects if `extract_video_id` is ever used on arbitrary text (outside of URLs); must ensure Markdown parsing is gated and safe.
- Requires unit tests to prevent regressions in parsing logic.

## Links
- Spec: docs/specs/002-markdown-link-video-id.md
- Plan: docs/plans/002-markdown-link-video-id.md
