# Plan: P1 developer guardrails

## Goal
Give maintainers one reliable local command set for linting, formatting, tests, and packaging checks, then run the same guardrails in CI.

## Task Breakdown
- [x] Add `ruff` as a development/test dependency.
- [x] Configure lint rules in `pyproject.toml`.
- [x] Configure formatting with `ruff format`.
- [x] Add `make lint`.
- [x] Add `make format`.
- [x] Add `make check` to run lint, tests, and package smoke checks.
- [x] Add direct dependencies for modules imported by project code, especially `requests` and `defusedxml`.
- [x] Add CI jobs or steps for linting and packaging checks.
- [x] Start moving broad tests toward the documented `tests/unit` and `tests/integration` split.
- [x] Update README or `CONTRIBUTING.md` with the local verification workflow.

## Sequencing
1. Add ruff dependency and a conservative configuration.
2. Run lint and make the smallest necessary code cleanups.
3. Add Makefile targets around existing commands.
4. Add direct dependency declarations and verify package installation.
5. Wire the new checks into CI.
6. Move or rename tests only after import behavior is stable from P0.

## Dependencies
- P0 package-shadowing fix should happen before larger test reorganization.
- CI from P0 provides the place to enforce new checks.
- Development dependency strategy must stay compatible with current `.[test]` install flow.

## Risks & Mitigations
- Risk: introducing lint creates a large unrelated cleanup diff.
  - Mitigation: start with a conservative rule set and expand later.
- Risk: formatter churn obscures behavior changes.
  - Mitigation: land formatting separately from feature work.
- Risk: direct dependency changes affect installs.
  - Mitigation: verify editable install and package install in CI.

## Definition of Done
- `make check` is the default local verification command.
- CI runs lint, tests, and packaging checks.
- Direct runtime imports are declared as direct dependencies.
- Test layout is closer to the project ADR without hiding packaging issues.
