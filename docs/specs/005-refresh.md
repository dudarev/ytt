# Spec 005: Refresh fetch results by bypassing cache

- PRD: `docs/prds/005-refresh.md`
- Plan: `docs/plans/005-refresh.md`

## Overview
Introduce `--refresh` for `ytt fetch` so a run can skip cache reads and fetch transcript/metadata from upstream sources.

## Architecture & Data Flow
- CLI (`src/ytt/application/cli.py`) adds `--refresh` as a boolean flag on `fetch`.
- Entry layer (`src/ytt/main.py`) passes this flag to `FetchTranscriptUseCase.execute(...)`.
- Use case forwards `refresh` to `TranscriptService.fetch(...)`.
- Domain service forwards `refresh` to repository `retrieve(...)`.
- Repository (`src/ytt/infrastructure/transcript_repository.py`) bypasses cache load when `refresh=True`, fetches from API, and saves updated bundle to cache.

## CLI/UX Behavior
- Default:
  - `ytt "<url>"` and `ytt fetch "<url>"` remain cache-first.
- Refresh:
  - `ytt fetch "<url>" --refresh` ignores local cached bundle for that run.

## Error Handling
- Preserve existing API/network error reporting.
- Do not silently fall back to cached bundle in refresh mode.

## Test Strategy
- Add repository unit tests to verify:
  - cache is used by default,
  - cache is skipped with `refresh=True`.
- Add CLI flow test to verify `--refresh` reaches service call kwargs.
