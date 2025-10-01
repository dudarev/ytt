# PRD 0001: Add Video Title and Description Extraction

## Description
- Expand the YouTube Transcript Tool (YTT) to automatically capture both the video title and full description alongside the transcript.
- Surface the extracted title and description in the default Markdown output ahead of the transcript content.
- Ensure the title leverages the most reliable source among Open Graph metadata, the `<title>` element, or structured JSON (e.g., `ytInitialPlayerResponse.videoDetails.title`).
- Ensure the description comes from the structured JSON payload (e.g., `description.simpleText`) with graceful fallbacks when unavailable.
- Provide CLI and library-level configuration flags to disable adding the title and/or description when consumers prefer transcript-only output.
- Maintain compatibility with existing transcript retrieval flows and error handling paths.
- Cache the resolved title and description alongside the transcript so repeat requests for the same video reuse previously fetc
hed metadata without additional network calls.

### Success Metrics
- Title and description appear for at least 95% of sampled public YouTube videos where the transcript is available.
- CLI users can opt out of adding the title or description without needing code changes.
- No regressions in transcript extraction success rate or runtime performance over baseline measurements.

### Non-Goals
- Fetching additional metadata (e.g., view counts, channel info) beyond title and description.
- Persisting metadata in databases or external storage.

## Transcript
- **Title research (May 28, 2025):** Confirmed reliable extraction paths through Open Graph tags, `<title>` elements, and `ytInitialPlayerResponse` JSON, favoring canonical values without the " - YouTube" suffix.【F:research/2025-05-28-get-title/README.md†L1-L44】
- **Description research (May 27, 2025):** Developed robust JSON parsing around the `description.simpleText` structure, including brace-aware extraction and fallback strategies when keys are missing.【F:research/2025-05-27-get-description/README.md†L1-L79】
- Reuse the JSON parsing utilities created during description research as the primary implementation path for both metadata fields, supplementing with Open Graph or HTML fallbacks as needed.
- Design flags such as `--no-title` and `--no-description` (and corresponding library options) to disable metadata injection without impacting transcript retrieval.
