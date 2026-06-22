# Plan: P3 contribution and release hygiene

## Goal
Make future changes easier to review, keep dependencies current, and make releases repeatable.

## Task Breakdown
- [ ] Add a pull request template with checklist items for tests, docs, changelog, and version bumps.
- [ ] Add `CONTRIBUTING.md` with setup, development, verification, and release guidance.
- [ ] Document when the lightweight PRD/spec/plan workflow is required.
- [ ] Add Dependabot or Renovate for Python dependencies.
- [ ] Add Dependabot or Renovate coverage for GitHub Actions.
- [ ] Fix README drift, including `LICENSE.md` vs `LICENSE`.
- [ ] Add a manual release checklist.
- [ ] Optionally add tag-driven GitHub release automation.
- [ ] Optionally add PyPI publishing automation if the package is meant to be distributed beyond Git installs.

## Sequencing
1. Add PR template and contribution guide.
2. Fix small documentation drift.
3. Add dependency update automation.
4. Add manual release checklist.
5. Add release automation only after manual release steps are clear.

## Dependencies
- P1 `make check` should exist before documenting the local verification loop.
- Release automation depends on deciding whether PyPI publishing is in scope.
- Repository settings may require GitHub admin access.

## Risks & Mitigations
- Risk: PR template becomes noisy for tiny changes.
  - Mitigation: keep checklist short and focused on project-specific rules.
- Risk: dependency automation creates low-value churn.
  - Mitigation: group minor updates and require CI to pass.
- Risk: release automation publishes unintended artifacts.
  - Mitigation: start with manual GitHub releases before adding package publishing.

## Definition of Done
- Contributors can find setup, verification, and release expectations in the repo.
- PRs have a project-specific checklist.
- Dependency updates are surfaced automatically.
- Release steps are documented and repeatable.
