# Spec 007: Per-fetch transcript language override

- PRD: `docs/prds/007-per-fetch-language-override.md`
- Plan: `docs/plans/007-per-fetch-language-override.md`

## Overview
Add `-l` / `--language` to the fetch command as a one-time transcript language preference. The explicit language is tried first, then configured `preferred_languages` are tried in their configured order.

## Architecture & Data Flow
- CLI parser (`src/ytt/application/cli.py`):
  - Add optional `-l` / `--language` to the `fetch` subcommand.
- Arg preparation (`src/ytt/main.py`):
  - Treat top-level invocations composed of known fetch flags, language flags, and URL-looking positionals as implicit `fetch` calls.
  - Preserve global flag behavior for `--help`, `-h`, `--version`, and `-V`.
  - Reuse clipboard URL fallback when an inferred fetch call omits the URL.
- Fetch use case (`src/ytt/application/fetch_service.py`):
  - Build an ordered language list from explicit language plus configured languages.
  - Deduplicate case-insensitively while preserving first occurrence.
  - Keep the existing missing-language error when both sources are empty.
- Transcript repository (`src/ytt/infrastructure/transcript_repository.py`):
  - Match manual transcripts by `language_code` as well as label.
  - Preserve language priority order in cache keys.

## Data & API Contracts
- New CLI option: `fetch [-l LANGUAGE | --language LANGUAGE] [youtube_url]`.
- `FetchTranscriptUseCase.execute(..., preferred_language: Optional[str] = None)` receives the one-time override.
- `TranscriptService.fetch(video_id, preferred_languages, refresh=False)` continues to receive a sequence ordered by priority.

## CLI/UX Behavior
- Works:
  - `ytt fetch <url> -l de-AT`
  - `ytt fetch -l de-AT`
  - `ytt -l de-AT`
  - `ytt --language=de-AT`
  - `ytt --refresh -l de-AT`
  - `ytt --no-copy --language de-AT`
- If the URL is omitted, the existing clipboard URL fallback is used.
- If the explicit language is unavailable, configured languages remain fallback candidates.
- Unknown top-level flags still produce argparse errors.

## Error Handling
- Empty explicit language values are ignored by the use case and fall back to configured languages.
- When neither an explicit language nor configured languages are available, the existing preferred-language configuration error is shown.
- Missing `-l` / `--language` values are handled by argparse.
- Clipboard read and validation errors use the existing messages.

## Telemetry / Performance Notes
- No telemetry changes.
- Cache key cardinality increases for different language priority orders, which is required to avoid returning transcripts selected under a different preference order.

## Test Strategy
- Unit tests for language resolution in `FetchTranscriptUseCase`.
- Unit tests for top-level `_prepare_args` language invocations, including mixed flag order.
- Unit tests for repository manual transcript selection by `language_code`.
- Unit tests for ordered cache keys.
- Run full test suite with `pytest`.
