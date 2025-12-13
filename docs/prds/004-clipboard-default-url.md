# PRD 004: Default to clipboard URL when no CLI parameters

## Description
- Allow YTT to read the YouTube URL from the system clipboard when no positional arguments are provided.
- Preserve existing behavior for explicit URLs and subcommands.
- Provide clear feedback when clipboard contents are missing or invalid.

## Problem Statement
Users often copy a YouTube link and immediately run `ytt` expecting it to "just work." Requiring them to retype or paste the URL as an argument adds friction, especially in quick workflows or when switching between windows.

## Users / Jobs to Be Done
- CLI users who copy a YouTube link and want to fetch transcripts with minimal typing.
- Note-takers and researchers who rely on keyboard-driven workflows and expect the tool to infer the URL from the clipboard.

## Goals
- Running `ytt` with no parameters should attempt to parse a YouTube URL from the clipboard and proceed as if it were passed explicitly.
- Retain support for existing `fetch` and `config` commands without breaking backward compatibility.
- Provide actionable error messages when clipboard reads fail or the clipboard lacks a usable YouTube URL.

## Non-Goals
- Auto-detecting URLs from application focus or browser history.
- Persisting clipboard history or introducing a new clipboard manager.
- Adding GUI affordances for clipboard management.

## Success Metrics
- Clipboard-based invocation succeeds when the clipboard contains a valid YouTube URL (including Markdown link forms) with no extra keystrokes.
- Error handling guides users to supply a URL explicitly if clipboard lookup fails.
- No regressions to existing flags or command parsing.

## Acceptance Criteria
- AC1: Running `ytt` with no arguments reads the clipboard and uses its contents as the YouTube URL if valid.
- AC2: If clipboard access raises an exception (e.g., missing system utility), YTT prints a warning to stderr and exits with a non-zero status instead of showing generic help text.
- AC3: If clipboard text lacks a recognizable YouTube URL, YTT informs the user and exits with a non-zero status.
- AC4: Explicit invocations such as `ytt fetch <url>`, `ytt <url>`, and `ytt config ...` continue to work as before.

## Key Risks & Assumptions
- **Risk**: Clipboard APIs may be unavailable in headless environments.
  - **Mitigation**: Surface clear warnings and fail fast without masking the error.
- **Risk**: Clipboard may contain large text blobs; parsing should remain efficient and avoid copying large buffers unnecessarily.
- **Assumption**: Users have already placed a YouTube URL or Markdown link on the clipboard before running `ytt` without parameters.

## References
- Spec: `docs/specs/004-clipboard-default-url.md`
- Plan: `docs/plans/004-clipboard-default-url.md`
