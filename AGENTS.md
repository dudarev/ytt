# Agent Instructions

- Whenever you introduce changes that affect project behavior, packaging, or public interfaces, increment the version number in `pyproject.toml` and add a corresponding entry to `CHANGELOG.md` following the Keep a Changelog format.
- When updating metadata that depends on the current date (e.g., `last-updated` fields), run the `date -I` command in the terminal to capture today's value accurately.
- Document structural or architectural decisions in the `docs/adrs/` directory as needed, numbering files with three digits (e.g., `001-new-decision.md`).
