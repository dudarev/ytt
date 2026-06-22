# Plan: P2 test quality

## Goal
Improve confidence in the most brittle behavior: YouTube metadata extraction, CLI output, package execution, and cache behavior.

## Task Breakdown
- [ ] Add saved HTML fixtures for representative YouTube metadata pages.
- [ ] Add fixture-based tests for title extraction.
- [ ] Add fixture-based tests for description extraction.
- [ ] Add tests for generic YouTube boilerplate descriptions.
- [ ] Add CLI golden-output tests for common fetch rendering combinations.
- [ ] Add CLI tests for clipboard fallback and fetch flags at the command boundary.
- [ ] Add package execution/import tests, including installed-package behavior.
- [ ] Add cache read/write tests that cover current and legacy payload shapes.
- [ ] Add coverage reporting in CI without enforcing a strict threshold initially.
- [ ] Split fast unit tests from slower integration-style tests.

## Sequencing
1. Add fixture directory and metadata fixture tests.
2. Add CLI golden-output tests around existing rendering behavior.
3. Add package/import checks after P0 resolves the stale package issue.
4. Expand cache-format regression tests.
5. Add coverage reporting once the test suite shape is stable.

## Dependencies
- P0 package smoke checks and import cleanup.
- P1 Makefile/CI guardrails for running separate test groups.
- Stable fixture naming and storage convention under `tests/`.

## Risks & Mitigations
- Risk: YouTube fixture HTML becomes large or noisy.
  - Mitigation: store minimized representative snippets rather than full pages unless full pages are required.
- Risk: golden-output tests become brittle.
  - Mitigation: reserve golden tests for user-facing CLI contracts and keep unit assertions for internals.
- Risk: coverage thresholds create busywork.
  - Mitigation: report coverage first, then decide on thresholds later.

## Definition of Done
- Metadata extraction has fixture coverage for realistic page structures.
- CLI output contracts have focused regression tests.
- Package/import behavior is tested in a way that catches local shadowing.
- CI reports coverage without blocking useful work on arbitrary thresholds.
