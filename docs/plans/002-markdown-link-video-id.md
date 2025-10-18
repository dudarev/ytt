---
title: 002-markdown-link-video-id
status: draft
owner: gpt-5-codex
last-updated: 2025-10-18
links: { prd: docs/prds/002-markdown-link-video-id.md, spec: docs/specs/002-markdown-link-video-id.md, tasks: null, adrs: [] }
---

## Task Breakdown
- [x] Update `extract_video_id` to detect Markdown link syntax and extract the enclosed URL.
- [x] Ensure existing URL parsing branches (watch, youtu.be, embed, shorts) still execute after Markdown normalization.
- [x] Add unit tests covering Markdown watch URLs, short links, malformed Markdown, and non-Markdown inputs.
- [x] Update documentation/tests as needed to reflect Markdown support.
- [x] Bump package version to `0.6.0` and record the change in `CHANGELOG.md`.

## Sequencing / Milestones
1. Normalize Markdown input inside `extract_video_id`.
2. Expand test coverage for new and existing URL patterns.
3. Verify CLI commands accept Markdown links via integration-style test or smoke run.
4. Update versioning and changelog.

## Dependencies
- No external dependencies; all work occurs in existing domain utilities and tests.

## Risks / Mitigations
- **Risk:** Overly permissive Markdown detection accidentally strips valid URLs with parentheses.
  - **Mitigation:** Require strict `[text](url)` structure and fallback to existing logic when not matched.
- **Risk:** Breaking existing callers if Markdown detection throws.
  - **Mitigation:** Use safe string operations and defensive checks returning `None` on failure.

## Definition of Done
- Unit tests cover Markdown link parsing and pass locally.
- `extract_video_id` handles Markdown links without regressing other URL formats.
- Version bumped and changelog updated documenting the feature.
- PRD and Spec links remain accurate.
