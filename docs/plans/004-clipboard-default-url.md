# Plan 004: Default to clipboard URL when no CLI parameters

- PRD: `docs/prds/004-clipboard-default-url.md`
- Spec: `docs/specs/004-clipboard-default-url.md`

## Task Breakdown
- [ ] Extend clipboard gateway with a read/paste method and wire it through the CLI entry layer.
- [ ] Update CLI argument preparation to fall back to clipboard content when no parameters are provided, including error messaging for failures.
- [ ] Add unit tests under `tests/unit/ytt/main/test_main.py` covering success and failure paths for clipboard-based invocation.
- [ ] Update documentation (README/CHANGELOG) and version number to reflect the new default behavior.

## Sequencing
1. Implement clipboard read capability and CLI fallback logic.
2. Add tests validating the new flow and error cases.
3. Refresh docs and bump version/changelog.

## Dependencies
- `pyperclip` availability for clipboard interactions.

## Definition of Done
- Clipboard fallback works as specified, with clear errors for invalid or unavailable clipboards.
- Tests added/updated and passing locally.
- README/CHANGELOG and version are updated.
