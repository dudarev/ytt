# Agent Instructions

- Whenever you introduce changes that affect project behavior, packaging, or public interfaces, increment the version number in `pyproject.toml` and add a corresponding entry to `CHANGELOG.md` following the Keep a Changelog format.
- When updating metadata that depends on the current date (e.g., `last-updated` fields), run the `date -I` command in the terminal to capture today's value accurately.
- Document structural or architectural decisions in the `docs/adrs/` directory as needed, numbering files with three digits (e.g., `001-new-decision.md`).
- YouTube URL parsing lives in `src/ytt/domain/value_objects.py`; unit tests belong in `tests/unit/ytt/domain/test_value_objects.py`.
- For unit tests, mirror the `src/` directory inside `tests/unit/` and name files `test_<source-file>.py` (add a suffix only when splitting large suites).

## Process Options: Full Flow or Standalone Plan

Use one of two tracks before implementation:

- Full flow: use PRD → Spec → Plan → Deliver for non-trivial features or changes where the extra design context improves implementation.
- Standalone plan: use a dated plan only for roadmap, priority, audit, planning-only, or one-off implementation work where creating matching PRD and spec files would add overhead without improving clarity.

Keep documents short but crisp—optimize for quick iteration by an agent. Do not add PRD/Spec placeholders to standalone dated plans.

### Full Flow: PRD → Spec → Plan → Deliver

1) PRD (what & why)
- Location: `docs/prds/`
- Filename: `NNN-<slug>.md` (example: `002-my-feature.md`)
- Contents: Problem statement, users/jobs-to-be-done, goals and non-goals, success metrics, acceptance criteria, key risks/assumptions.

2) Spec (how)
- Location: `docs/specs/`
- Filename: `NNN-<slug>.md`
- Contents: overview, architecture/diagram, data & API contracts, CLI/UX behavior, error handling, telemetry/perf notes, test strategy.
- Must link back to the PRD; keep reciprocal links updated (PRD ↔ Spec).

3) Plan (steps)
- Location: `docs/plans/`
- Filename: `NNN-<slug>.md`
- Contents: task breakdown (checklist), sequencing/milestones, dependencies, owner(s), risks/mitigations, Definition of Done.
- Must link to both PRD and Spec; keep reciprocal links updated (PRD ↔ Plan, Spec ↔ Plan).

Standalone plans that are not part of a synchronized PRD/Spec/Plan set should also live in `docs/plans/`, but must use a date prefix instead of the numbered `NNN-` prefix: `YYYY-MM-DD-<slug>.md`. When creating dated plan filenames, run `date -I` and use that value.

4) Deliver (implement)
- Create branch: `feat/NNN-<slug>` and implement per plan.
- Update or add tests under `tests/` to cover behavior and edge cases.
- If behavior/packaging/public interface changes: bump version in `pyproject.toml` and add a `CHANGELOG.md` entry.
- Add ADR(s) in `docs/adrs/` when introducing notable structural/architectural decisions.
- For any `last-updated` style metadata, use `date -I`.
- Before finishing an implementation iteration, run the relevant local gates; default to `make fix` followed by `make check` unless the change clearly needs a narrower or broader command.
- Open a PR referencing the PRD/Spec/Plan; ensure CI/tests pass.

Quick checklist
- [ ] PRD drafted and committed (`docs/prds/NNN-<slug>.md`)
- [ ] Spec drafted and cross-linked (PRD ↔ Spec) (`docs/specs/NNN-<slug>.md`)
- [ ] Plan created and cross-linked (PRD ↔ Plan, Spec ↔ Plan) (`docs/plans/NNN-<slug>.md`)
- [ ] Feature branch created (`feat/NNN-<slug>`)
- [ ] Implementation matches plan; docs kept in sync
- [ ] Tests added/updated
- [ ] Local gates run (`make fix` then `make check` by default)
- [ ] Version + changelog updated if required
- [ ] ADR(s) added if needed
- [ ] PR opened with links to PRD/Spec/Plan
