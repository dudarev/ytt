# PRD 005: Refresh fetch results by bypassing cache

## Description
- Add a CLI parameter to bypass local cache and fetch transcript/metadata from YouTube for a specific run.
- Keep default behavior unchanged (cache-first).

## Problem Statement
Users can get stale metadata from cached entries. They need a deterministic way to refresh without manually deleting cache files.

## Users / Jobs to Be Done
- Users who suspect cache staleness and want fresh transcript/metadata immediately.

## Goals
- Add a one-shot fetch mode that skips cache reads.
- Persist newly fetched data back to cache for subsequent default runs.

## Non-Goals
- Global cache invalidation policies.
- Automatic staleness detection.

## Success Metrics
- `ytt fetch <url> --refresh` never uses cached bundle content.
- Existing commands and defaults remain backward-compatible.

## Acceptance Criteria
- AC1: New flag `--refresh` is available on `fetch`.
- AC2: When enabled, repository bypasses cache read and fetches from YouTube.
- AC3: Fresh result is still written to cache.
- AC4: Without the flag, cache-first behavior remains unchanged.

## Key Risks & Assumptions
- **Risk**: Force refresh can fail when network/API is unavailable.
  - **Mitigation**: Preserve existing error behavior and avoid hidden fallback to stale cache.
- **Assumption**: Users explicitly opt in when they need freshness over speed.

## References
- Spec: `docs/specs/005-refresh.md`
- Plan: `docs/plans/005-refresh.md`
