# PRD 007: Per-fetch transcript language override

## Description
- Add a fetch-scoped language preference so users can request a specific transcript language without changing configured defaults.
- Preserve fallback to configured preferred languages when the override is unavailable.

## Problem Statement
Users sometimes need one transcript in a language different from their normal `preferred_languages`. Today they must change global configuration, fetch the transcript, and then restore their defaults. That is slow and risks leaving the tool configured incorrectly for later fetches.

## Users / Jobs to Be Done
- CLI users who usually fetch transcripts in one language but occasionally need another language for a single video.
- Users who want to try a regional language code, such as `de-AT`, while retaining normal fallback behavior.

## Goals
- Add `-l` / `--language` to fetch commands.
- Try the per-fetch language before configured languages.
- Allow URL-less top-level language invocations to use clipboard fallback.
- Keep transcript cache entries separated by language priority.
- Document the new CLI behavior.

## Non-Goals
- Changing the persisted configuration format.
- Supporting multiple per-fetch language override flags.
- Adding automatic translation or transcript generation.

## Success Metrics
- `ytt fetch <url> -l de-AT` tries `de-AT` before configured languages.
- `ytt -l de-AT` resolves the URL from clipboard.
- `ytt --refresh -l de-AT` works the same as `ytt fetch --refresh -l de-AT`.
- Fetches with different language priority order do not share the same cache entry.

## Acceptance Criteria
- AC1: The parser accepts `-l` and `--language` on `fetch`.
- AC2: An explicit language is prepended to configured languages and duplicate configured entries are skipped case-insensitively.
- AC3: A per-fetch language works even when no languages are configured.
- AC4: Missing configured languages still produce the existing error when no per-fetch language is provided.
- AC5: Top-level fetch inference handles language flags combined with other fetch flags in any order.
- AC6: Cache keys preserve preferred-language priority order.
- AC7: README, changelog, and tests cover the new behavior.

## Key Risks & Assumptions
- **Risk**: Reusing a cache key for a different language priority could return the wrong transcript.
  - **Mitigation**: Preserve ordered, deduplicated language priority in cache keys.
- **Risk**: Top-level command inference could become too broad.
  - **Mitigation**: Infer fetch only for recognized fetch flags, recognized language flag forms, and URL-looking positionals.
- **Assumption**: Language values use youtube-transcript-api language codes or labels accepted by the transcript list.

## References
- Spec: `docs/specs/007-per-fetch-language-override.md`
- Plan: `docs/plans/007-per-fetch-language-override.md`
