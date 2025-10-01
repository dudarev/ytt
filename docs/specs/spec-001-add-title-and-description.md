---
title: spec-001-add-title-and-description
status: draft
owner: gpt-5-codex
last-updated: 2025-10-02
links: { prd: docs/prds/001-add-title-and-description.md, plan: null, tasks: null, adrs: [] }
---

## Overview
- Capture YouTube video title and description alongside transcripts and surface them ahead of transcript content by default while allowing opt-outs.

## Functional Requirements
- FR1: Resolve the video title using structured JSON (`ytInitialPlayerResponse.videoDetails.title` or equivalent) with fallbacks to Open Graph metadata and `<title>` markup.
- FR2: Retrieve the video description from structured JSON (`ytInitialData` or `ytInitialPlayerResponse` fields such as `description.simpleText` or `description.runs`) with fallback to Open Graph metadata.
- FR3: Inject the resolved title and description into the default Markdown output before the transcript section.
- FR4: Provide CLI flags (e.g., `--no-title`, `--no-description`) to disable adding each metadata field.
- FR5: Offer a single CLI flag (e.g., `--no-metadata`) that simultaneously omits both the title and description for convenience.
- FR6: Cache the title and description with the transcript so repeat requests for the same video reuse stored metadata.

## Acceptance Criteria
- AC1: Given a public video with accessible transcript metadata, when a user runs the CLI with default options, then the generated Markdown includes the extracted title and description ahead of the transcript.
- AC2: Given a video where JSON metadata is missing the title or description, when extraction runs, then the system falls back to Open Graph metadata and `<title>` markup without errors and surfaces the metadata if any source succeeds.
- AC3: Given a CLI invocation with `--no-title` or `--no-description`, when the output is generated, then the disabled metadata fields are omitted while the transcript still appears.
- AC4: Given a CLI invocation with `--no-metadata`, when the output is generated, then both the title and description are omitted while the transcript still appears.
- AC5: Given a repeat request for a previously fetched video, when the tool runs again, then the transcript, title, and description are served from cache without performing new network fetches for those fields.

## UX Notes / Flows
- CLI default flow: user runs `ytt fetch <video-id>` and receives Markdown with title, description, then transcript; toggles metadata via `--no-title`, `--no-description`, or the combined `--no-metadata` flag.

## Constraints
- Preserve existing transcript retrieval behavior and error handling paths.
- Avoid additional network calls on cached replays beyond what transcript caching already performs.
- Ensure feature releases with a minor version bump to reflect added functionality.
