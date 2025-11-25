# ADR 003: Test suite organization

## Status

Accepted

## Context

Tests currently live in a single file, which makes it hard to scale coverage,
mirror the growing module layout, and tell unit checks from integration
scenarios as the codebase grows.

## Decision

- Create top-level directories under `tests/` for `unit/` and `integration/`.
- Mirror the production package layout inside `tests/unit/` so each module gains a
  matching unit test module when needed.
- Name unit test modules using the pattern `test_<module>[_detail]` to link each
  test file to its subject, optionally adding the specific function or scenario.
- Focus unit tests on the most important business logic; avoid covering every helper
  or adapter by default.
- Migrate broad, cross-module checks into `tests/integration/`, evolving the
  existing combined test file into focused integration scenarios.
- Use integration suites for scenarios where multiple components or external
  boundaries collaborate.

Example layout:

```
tests/
├── integration/
│   └── test_orders_flow.py
└── unit/
    ├── package_a/
    │   ├── test_module_x.py
    │   └── test_module_x_process_order.py
    └── package_b/
        ├── test_service.py
        └── test_service_create_order.py
```

## Consequences

- Contributors share a clear map for new tests that matches the source tree.
- Moving existing tests will take some effort but yields better focus and
  discoverability.
- Unit tests stay centered on core rules, while integration suites capture
  collaborations without duplicating unit checks.
- Future categories such as functional or contract tests can live under the same
  hierarchy.
