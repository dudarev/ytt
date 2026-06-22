# Plan 007: Per-fetch transcript language override

- PRD: `docs/prds/007-per-fetch-language-override.md`
- Spec: `docs/specs/007-per-fetch-language-override.md`

## Task Breakdown
- [x] Add `-l` / `--language` to the fetch parser.
- [x] Pass the per-fetch language from `main` to `FetchTranscriptUseCase`.
- [x] Merge explicit and configured languages in priority order with case-insensitive dedupe.
- [x] Allow top-level language invocations to use clipboard fallback.
- [x] Support language flags combined with other fetch flags in any order.
- [x] Match manual transcripts by `language_code`.
- [x] Preserve language priority in cache keys.
- [x] Add unit tests for use case language resolution.
- [x] Add unit tests for top-level argument preparation.
- [x] Add unit tests for transcript repository language matching and cache keys.
- [x] Update README, changelog, and version metadata.

## Sequencing
1. Parser and argument preparation.
2. Use case language-priority resolution.
3. Repository transcript selection and cache-key behavior.
4. Unit tests for behavior and regressions.
5. README, changelog, and release metadata updates.

## Dependencies
- Existing `ConfigService.get_preferred_languages`.
- Existing `TranscriptService.fetch` priority ordering.
- Existing clipboard URL fallback path.
- youtube-transcript-api transcript objects exposing `language`, `language_code`, and `is_generated`.

## Risks & Mitigations
- Risk: top-level inference accepts invalid commands as fetch.
  - Mitigation: restrict inference to known fetch flags, language flag forms, and URL-looking positionals.
- Risk: cache returns transcripts fetched with a different language priority.
  - Mitigation: include ordered, normalized language priority in the cache key.
- Risk: configured languages are bypassed when an override is unavailable.
  - Mitigation: append configured languages after the explicit override.

## Definition of Done
- `-l` / `--language` works for explicit and clipboard-backed fetches.
- Fallback to configured languages is preserved.
- Cache entries respect language priority order.
- README, changelog, PRD, spec, and plan are in sync.
- Full test suite passes locally.
