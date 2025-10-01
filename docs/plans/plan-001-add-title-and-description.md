---
title: plan-001-add-title-and-description
status: accepted
owner: gpt-5-codex
last-updated: 2025-10-01
links: { prd: docs/prds/001-add-title-and-description.md, spec: docs/specs/spec-001-add-title-and-description.md, tasks: null, adrs: [] }
---

## Goal
- Deliver the functionality described in the add-title-and-description spec so that CLI users receive video metadata ahead of transcripts while retaining opt-out controls and cache reuse.

## Architecture Choices
- **Presentation boundary:** Extend `FetchTranscriptUseCase.render` to emit title and description before transcript lines while respecting new CLI flags.
- **Application layer:** Introduce a new orchestrator (e.g., `VideoMetadataService`) that coordinates transcript retrieval and metadata extraction so CLI commands depend on a single use case returning both transcript and metadata.
- **Domain entities:** Expand the domain to include a `VideoMetadata` value object and update transcript aggregates (e.g., a new `VideoTranscriptBundle`) to carry metadata alongside transcript lines.
- **Infrastructure boundaries:** Add a metadata gateway that encapsulates HTML/JSON parsing. The gateway should first target the structured JSON shapes identified in research (`description.simpleText`, `attributedDescription.content`, `videoDetails.title`) before falling back to Open Graph tags or `<title>` text. This isolates YouTube-specific scraping logic, enables future provider swaps, and relies on the existing dependency footprint (`youtube-transcript-api` plus its bundled `requests` and `defusedxml` transitives, `appdirs`, `pyperclip`) for HTTP ergonomics and safe HTML parsing without introducing new top-level packages.
- **Caching contract:** Extend the existing cache repository to persist metadata together with transcript data in a backward-compatible structure (e.g., versioned pickle payload).

## Implementation Notes
- Reuse the JSON-extraction approach prototyped in `research/2025-05-27-get-description/get_description_request.py`, including the balanced-brace parser for `description`/`attributedDescription` blocks. Prefer `simpleText` values from `description`, then `content` from `attributedDescription` / `attributedDescriptionBodyText`, and finally fall back to OG meta tags when JSON extraction fails.
- Derive titles in the same gateway using the three sources from `research/2025-05-28-get-title/get_title_research.py`: prioritize `videoDetails.title` within the `ytInitialPlayerResponse` JSON, backstop with `og:title`, and use `<title>` (stripping the " - YouTube" suffix) as a last resort.
- Adopt `requests` (already provided transitively by `youtube-transcript-api`) for metadata retrieval with explicit timeouts, retry/backoff policy, and a desktop User-Agent header that mirrors the research scripts. Reuse a shared session to prepare for future batching and to centralize proxy/header configuration. If we later need to drop `requests`, retain a thin abstraction so the gateway can swap to `urllib.request` without affecting callers.
- Parse HTML fallbacks with `defusedxml.ElementTree` to extract `<meta property="og:description">`, `<meta property="og:title">`, and `<title>` values. Keep parsing logic scoped to the gateway so the rest of the application remains agnostic of DOM parsing concerns, and document the security posture benefits of defused parsing versus generic HTML libraries.
- Hide network and parsing details behind an interface in `domain.services` so unit tests can inject fake metadata sources without relying on real HTTP responses.
- Keep `pyproject.toml` unchanged because the necessary libraries arrive via existing dependencies; document this decision in the plan and ADR if questions surface about transitive usage.
- Update CLI argument parsing in `application.cli` to support `--no-title`, `--no-description`, and `--no-metadata` while ensuring combined flag precedence.
- Ensure observability by surfacing warnings when metadata could not be resolved, but avoid failing the command unless transcripts also fail. Keep logging/CLI output within current capabilities so no observability dependency changes are required, and capture HTTP status plus parsing failure reasons (including whether JSON, Open Graph, or defused XML parsing failed) to aid triage.
- Maintain compatibility with existing transcript cache files by detecting legacy entries and populating metadata lazily on first successful fetch.

## Data Model
- Add `VideoMetadata` dataclass with `title: str | None` and `description: str | None`.
- Extend cached bundle schema to store `{ "version": 2, "transcript": [...], "metadata": { "title": ..., "description": ... } }`, with loader handling both version 1 (transcript-only) and version 2 payloads.
- Persist metadata in memory as part of a new `VideoTranscriptBundle` entity returned by repositories and use cases.

Because the tool does not yet have active users, no separate migration or staged rollout activities are required beyond ensuring the default experience works as expected once metadata support lands.

## Test Strategy
- **Unit tests:** Cover metadata parsing fallbacks, cache upgrades, and flag-driven rendering logic in isolation with mocked gateways, including `requests` timeout/error propagation and defused XML parsing edge cases.
- **Integration tests:** Exercise the CLI end-to-end against recorded fixtures (e.g., VCR cassettes) to validate combined transcript and metadata output.
- **Regression tests:** Verify legacy cache files remain readable and produce identical transcript output when metadata is unavailable.
- **Manual QA:** Run CLI against sample videos with/without metadata availability to confirm behavior of each flag.

## Work Breakdown
1. Define domain entities and interfaces for metadata and transcript bundles.
2. Implement metadata infrastructure adapter, starting with the JSON parsing pathway validated in research and layering OG/`<title>` fallbacks using `requests` and `defusedxml` without altering top-level dependencies.
3. Update cache repository to persist metadata with migration support.
4. Expand application services and CLI rendering to surface metadata and new flags.
5. Add automated tests (unit fixtures for JSON, OG, and `<title>` fallbacks) and documentation updates (README usage, changelog entry upon release).
