# PRD 006: Clipboard fallback for URL-less fetch flag invocations

## Description
- Extend clipboard URL fallback to fetch invocations that omit the URL but include fetch flags.
- Support both explicit and implicit fetch entrypoints.

## Problem Statement
Users can run `ytt fetch --refresh` or `ytt --refresh` expecting the same clipboard fallback behavior as bare `ytt`, but these currently fail because `youtube_url` is required at parse time.

## Users / Jobs to Be Done
- CLI users who run fetch commands quickly with flags and expect URL derivation from clipboard when URL is omitted.

## Goals
- Allow URL-less fetch commands with flags to use clipboard fallback.
- Preserve current clipboard error messaging.
- Preserve existing `--help`/`--version` behavior.

## Non-Goals
- Introducing new flags.
- Changing transcript fetch semantics.
- Auto-fixing unknown flags.

## Success Metrics
- `ytt fetch --refresh` resolves URL from clipboard and executes fetch.
- `ytt --refresh` resolves URL from clipboard and executes fetch.
- Existing bare `ytt` fallback still works.

## Acceptance Criteria
- AC1: `ytt fetch --refresh` uses clipboard URL when URL is omitted.
- AC2: `ytt --refresh` is inferred as fetch and uses clipboard URL.
- AC3: Empty/invalid clipboard in these paths shows current clipboard-specific errors plus help text.
- AC4: Global flags `--help` and `--version` retain current behavior.
- AC5: Unknown top-level flags still raise argparse errors.

## Key Risks & Assumptions
- **Risk**: Over-eager command inference could misinterpret non-fetch commands.
  - **Mitigation**: Infer fetch only when all top-level args are known fetch flags.
- **Assumption**: Fetch flags remain simple boolean switches without additional values.

## References
- Spec: `docs/specs/006-clipboard-fallback-for-fetch-flags.md`
- Plan: `docs/plans/006-clipboard-fallback-for-fetch-flags.md`
