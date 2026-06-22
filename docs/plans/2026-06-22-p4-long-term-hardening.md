# Plan: P4 long-term hardening

- PRD: Deferred until implementation.
- Spec: Deferred until implementation.

## Goal
Reduce hidden compatibility risks and clarify long-term maintenance boundaries for cache data, public APIs, and execution modes.

## Task Breakdown
- [ ] Decide whether pickle should remain the cache format.
- [ ] If replacing pickle, design a JSON or other stable cache payload.
- [ ] Define cache versioning and invalidation behavior.
- [ ] Add cache migration or safe fallback behavior for older cache files.
- [ ] Decide whether `python -m ytt` is supported.
- [ ] Add `ytt.__main__` if module execution is supported.
- [ ] Review the public package API exported from `ytt.__init__`.
- [ ] Document supported public API functions and compatibility expectations.
- [ ] Add ADRs for notable decisions: cache format, module execution, public API stance.

## Sequencing
1. Audit current cache payloads and public exports.
2. Decide supported compatibility boundaries.
3. Write ADRs for cache format and public API stance.
4. Implement cache-format or module-execution changes in separate follow-up work.
5. Add migration and regression tests before changing cache behavior.

## Dependencies
- P2 cache tests should exist before changing cache format.
- Public API decisions should account for README usage and any known external users.
- Version and changelog updates are required for public-interface or cache behavior changes.

## Risks & Mitigations
- Risk: cache migration breaks existing users' local caches.
  - Mitigation: keep backward-compatible reads or fail open by refetching.
- Risk: public API cleanup breaks undocumented but real usage.
  - Mitigation: deprecate first when reasonable and document supported entrypoints.
- Risk: `python -m ytt` support creates another path to maintain.
  - Mitigation: keep `ytt.__main__` as a thin call to the existing CLI entrypoint.

## Definition of Done
- Cache compatibility policy is documented.
- Public API support boundaries are explicit.
- Module execution support is either implemented or intentionally out of scope.
- ADRs capture the structural decisions.
