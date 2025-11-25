---
title: 003-prepend-video-url
status: accepted
owner: gpt-5-codex
last-updated: 2025-11-25
links: { prd: docs/prds/003-prepend-video-url.md, spec: docs/specs/003-prepend-video-url.md, tasks: null, adrs: [] }
---

## Goal
Deliver the prepend-video-url functionality so CLI users receive the canonical video URL as the first line of output by default, improving traceability for AI summarization and transcript archival workflows.

## Architecture Choices
- **Canonicalization at the application edge**: Compute the canonical URL in `main.py` or `fetch_service.py` from the extracted VideoID, not from the raw input. This ensures consistency across all input formats (watch, youtu.be, Shorts, embed, /v, Markdown links).
- **Flag propagation**: Add a `show_url` boolean parameter that flows from CLI argument parsing through `FetchTranscriptUseCase.execute()` and `render()`, mirroring the existing pattern for `show_title`, `show_description`.
- **Defensive handling**: If `input_url` is missing or unparseable (edge case), skip the URL line but continue processing; do not fail the command.
- **Backward compatibility**: Provide `--no-url` opt-out; ensure `--no-metadata` also disables URL. Treat as a minor version bump; document in CHANGELOG.

## Implementation Notes
- Leverage existing `extract_video_id(url)` in `domain/value_objects.py` to obtain the VideoID.
- Construct URL as: `f"https://www.youtube.com/watch?v={video_id.value}"` where `video_id` is the VideoID value object.
- Prepend the URL + blank line to the output in `render_lines()` before title/description/transcript sections.
- Ensure clipboard content includes the URL when enabled.
- No new dependencies or domain model changes required.

## Data Model
- No changes to domain entities. VideoID extraction already available.
- URL is computed and rendered at the application/presentation boundary.

## Work Breakdown
1. **CLI argument**: Add `--no-url` flag and update `--no-metadata` help text in `application/cli.py`.
2. **Main entry point**: Compute `show_url` and pass it with `input_url` to use case in `main.py`.
3. **Use case**: Update `FetchTranscriptUseCase.execute()`, `render()`, and `render_lines()` signatures to accept `show_url` and `input_url`; prepend URL in `render_lines()`.
4. **Tests**: Update `tests/test_ytt.py` to verify default URL output, `--no-url` suppression, `--no-metadata` behavior, and Markdown canonicalization.
5. **Documentation**: Update README with usage note; add 0.7.0 CHANGELOG entry.
6. **Version**: Bump `pyproject.toml` to 0.7.0.

## Files to Modify
- `src/ytt/application/cli.py`: Add `--no-url` argument and update help.
- `src/ytt/main.py`: Wire `show_url` and `input_url`.
- `src/ytt/application/fetch_service.py`: Update `execute()`, `render()`, `render_lines()` to accept and handle `show_url` and `input_url`.
- `tests/test_ytt.py`: Add/update test cases for URL output and flags.
- `README.md`: Document the URL line and `--no-url` flag.
- `pyproject.toml`: Bump version to 0.7.0.
- `CHANGELOG.md`: Add 0.7.0 entry.

## Test Strategy
- **Default behavior**: Verify first line is canonical URL.
- **`--no-url`**: URL absent; title/description/transcript present.
- **`--no-metadata`**: URL/title/description absent; only transcript.
- **Canonicalization**: Markdown link, youtu.be, /v, embed, Shorts all resolve to standard watch URL.
- **Clipboard**: URL included when enabled, mirroring stdout.
- **Edge case**: Missing `input_url` → skip URL line, continue normally.

## Definition of Done
- [x] All tests passing locally and in CI.
- [x] Default output includes canonical URL as first line.
- [x] `--no-url` and `--no-metadata` work as specified.
- [x] README and CHANGELOG updated; version bumped to 0.7.0.
- [x] PR references PRD/Spec/Plan.

## Risks & Mitigations
- **Output parsing regression**: Users or scripts expecting specific first line format.
  - **Mitigation**: Provide `--no-url` to opt out; document feature in release notes; ensure `--no-metadata` also disables URL.
- **Edge case URL handling**: Missing or unparseable `input_url`.
  - **Mitigation**: Defensive guard; skip URL line but continue processing.

## Sequencing & Dependencies
1. Create/finalize PRD/Spec/Plan (this document).
2. Create feature branch `feat/003-prepend-video-url`.
3. Implement CLI, main, use case changes.
4. Update tests to cover new behavior.
5. Update version, README, CHANGELOG.
6. Run full test suite locally; ensure CI is green.
7. Open PR with references to PRD/Spec/Plan.
