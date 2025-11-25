# ADR 004: AI-assisted delivery workflow

## Status

Proposed

## Context

Work in this repository is frequently executed by AI agents. Without explicit guardrails, changes can lose traceability, skip testing/versioning, or drift from intended outcomes.

## Decision

- Adopt a lightweight PRD → Spec → Plan → Deliver flow as the default workflow for AI-led, non-trivial changes.
- Keep artifacts in `docs/prds/`, `docs/specs/`, and `docs/plans/` following the `NNN-<slug>.md` pattern and reciprocal linking described in `AGENTS.md`.
- Continue to require tests for behavioral changes and version/changelog updates when public behavior or packaging shifts.

## Scope and Exceptions

- Applies to AI-led or largely automated contributions.
- Trivial changes (e.g., typo fixes, comment tweaks, tiny refactors with no behavior change) may skip the flow; reviewers/maintainers can waive it when appropriate.

## Rationale

- Preserves intent and traceability for AI-generated work.
- Ensures design/implementation alignment and reduces rework.
- Keeps review surface predictable with clear artifacts and cross-links.

## Consequences

- Adds modest ceremony to AI-led changes but improves reliability and auditability.
- Contributors must maintain PRD/Spec/Plan links and keep status fields current.

## References

- `AGENTS.md` — detailed instructions and checklist for PRD/Spec/Plan artifacts.
