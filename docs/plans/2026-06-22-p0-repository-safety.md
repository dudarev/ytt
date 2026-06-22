# Plan: P0 repository safety and correctness


## Goal
Make the default branch difficult to break, ensure pull requests run the core verification suite, and remove local/package ambiguity that can make development exercise stale code.

## Task Breakdown
- [x] Enable branch protection for `main` after CI lands on the default branch.
- [x] Document required pull requests before merging to `main`.
- [x] Document required CI checks before merging.
- [x] Document disabled force pushes and branch deletion on `main`.
- [x] Add a GitHub Actions workflow for `pull_request` and `push` to `main`.
- [x] Add `tox` so the Python version matrix can run consistently in CI and locally.
- [x] Run tests on Python 3.12 and 3.13.
- [x] Fix the stale top-level `ytt/` package so local test imports resolve to `src/ytt` and installed imports resolve to the installed package.
- [x] Add package-install smoke checks for `ytt --help`, `ytt --version`, and `import ytt`.
- [x] Update version and changelog if packaging or public import behavior changes.

## Sequencing
1. Add `tox` environments for the supported Python versions.
2. Add CI workflow with the current test suite through `tox`.
3. Add package-install smoke checks to expose import or entrypoint drift.
4. Fix the stale top-level package and adjust tests that rely on path mutation.
5. Turn on branch protection once CI is stable on the default branch.
6. Document the final protected-branch policy.

## Dependencies
- GitHub repository admin access for branch protection.
- Current test suite must pass in a clean CI environment.
- Python 3.12 and 3.13 must be available in CI for the `tox` matrix.
- Packaging fix may depend on removing local `sys.path` test workarounds.

## Risks & Mitigations
- Risk: branch protection is enabled before CI is stable and blocks routine work.
  - Mitigation: land CI first, confirm it passes on `main`, then require it.
- Risk: removing the stale package breaks tests that accidentally import it.
  - Mitigation: add install-based smoke checks and update tests to import the packaged code.
- Risk: CI differs from local development.
  - Mitigation: use `tox` as the shared matrix runner and expose it through `make` targets in follow-up P1 work.

## Definition of Done
- PRs into `main` require passing checks once the documented branch protection policy is applied after CI lands.
- `tox` runs `pytest` on Python 3.12 and 3.13 in CI.
- Local test imports resolve to `src/ytt`; installed imports resolve to the installed package built from `src/ytt`.
- Installed CLI smoke checks pass in CI.
- Any packaging/public-interface behavior changes are reflected in version and changelog.
