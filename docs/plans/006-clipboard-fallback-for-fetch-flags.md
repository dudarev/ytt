# Plan 006: Clipboard fallback for URL-less fetch flag invocations

- PRD: `docs/prds/006-clipboard-fallback-for-fetch-flags.md`
- Spec: `docs/specs/006-clipboard-fallback-for-fetch-flags.md`

## Task Breakdown
- [x] Make `fetch` URL positional optional in parser.
- [x] Extend `_prepare_args` to infer fetch from top-level fetch flags.
- [x] Reuse one clipboard fallback path for bare `ytt` and URL-less fetch invocations.
- [x] Add `_prepare_args` tests for success/failure and global/unknown flag behavior.
- [x] Add CLI flow tests for `ytt fetch --refresh` and `ytt --refresh`.
- [x] Update README examples and changelog.
- [x] Bump version to `0.9.1`.

## Sequencing
1. Parser + `_prepare_args` implementation.
2. Unit and CLI test updates.
3. Docs and release metadata updates.
4. Full test run.

## Dependencies
- Existing clipboard gateway behavior.
- Existing URL extraction (`extract_video_id`).

## Risks & Mitigations
- Risk: introducing inference collisions with global flags.
  - Mitigation: explicitly exclude global flags from fetch inference.
- Risk: unknown flags silently mapped to fetch.
  - Mitigation: infer only when all args are recognized fetch flags.

## Definition of Done
- Feature commands work as specified.
- Existing command behavior remains stable.
- Tests pass locally.
- PRD/Spec/Plan + README + changelog + version are updated.
