# ADR 002: Domain-driven package structure

## Status

Accepted

## Context

The `main.py` file originally contained configuration management, YouTube API
integration, caching, clipboard utilities, and the command line entrypoint.
Having all concerns combined into a single module made the code harder to
understand, test, and extend. Upcoming work is expected to include features for
retrieving additional video metadata such as titles and descriptions, so we need
an approach that keeps the domain model isolated and ready for new
infrastructure integrations.

## Decision

We refactored the project into layers that follow domain-driven design (DDD)
principles:

- `ytt.domain` contains the core model and business services. It defines
  immutable value objects, transcript entities, and the `TranscriptRepository`
  port used by the rest of the application. The domain layer has no dependencies
  on other project modules.
- `ytt.infrastructure` implements the domain ports. It provides repositories for
  configuration, clipboard integration, caching, and communication with the
  YouTube Transcript API.
- `ytt.application` coordinates user-facing use cases. It wires domain services
  with infrastructure implementations and exposes CLI handlers to the
  presentation layer.
- `ytt.main` now only orchestrates dependency wiring and command execution.

This structure makes the domain layer the heart of the codebase, with
application and infrastructure layers depending on it while remaining adaptable
for future features such as fetching video titles or descriptions.

## Consequences

- Responsibilities are clearly separated, lowering coupling between unrelated
  functionality.
- New delivery mechanisms (e.g., web UI or API) can re-use the domain and
  application layers without reimplementing infrastructure details.
- Additional metadata providers can be added alongside transcripts by expanding
  domain ports and infrastructure adapters without modifying existing business
  logic.
- Some modules now perform only orchestration work, which slightly increases the
  number of files but yields better maintainability.
