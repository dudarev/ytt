# Plan 005: Refresh fetch results by bypassing cache

- PRD: `docs/prds/005-refresh.md`
- Spec: `docs/specs/005-refresh.md`

## Task Breakdown
- [ ] Add `--refresh` argument to fetch CLI parser.
- [ ] Thread `refresh` through main/use case/domain service/repository interfaces.
- [ ] Implement repository logic to skip cache read when refresh is enabled while preserving cache writes.
- [ ] Add/adjust tests for CLI wiring and repository behavior.
- [ ] Update README and CHANGELOG.

## Sequencing
1. Add interface and repository support for refresh.
2. Wire CLI argument through execution path.
3. Update tests.
4. Update docs and release notes.

## Dependencies
- Existing YouTube transcript and metadata gateways.

## Risks & Mitigations
- Risk: behavior drift in default mode.
  - Mitigation: explicit tests for default cache usage path.

## Definition of Done
- `--refresh` works end-to-end.
- Default cache-first behavior unchanged.
- Tests passing locally.
- Documentation updated.
