# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.4] - 2026-02-14

### Fixed
- Accept schemeless YouTube URLs such as `youtube.com/shorts/<VIDEO_ID>` when extracting video IDs.

## [0.8.3] - 2026-01-02

### Added
- Added `help` command as an alias for `--help` to display usage information.

## [0.8.2] - 2026-01-02

### Changed
- Clarified CLI help/README that YouTube URLs should be wrapped in quotes when passed via a shell.
- Added an error hint to quote URLs when extraction fails (common when `&` gets interpreted by the shell).

## [0.8.1] - 2025-12-13

### Fixed
- Show CLI help after clipboard errors when invoking `ytt` without arguments so users can quickly see how to provide a URL.

## [0.8.0] - 2025-12-13

### Added
- Allow invoking `ytt` with no arguments to read a YouTube URL from the clipboard before fetching transcripts.

### Fixed
- Provide explicit clipboard error messages when clipboard access fails or lacks a usable YouTube URL instead of showing generic help text.

## [0.7.0] - 2025-11-01

### Added
- Print the canonical video URL (`https://www.youtube.com/watch?v=<VIDEO_ID>`) as the first line of output by default, improving traceability for AI summarization workflows.
- Added `--no-url` flag to suppress the URL line when not needed.

### Changed
- `--no-metadata` now disables URL, title, and description output (previously only title and description).

## [0.6.0] - 2025-10-18

### Added
- Allow Markdown-formatted YouTube links to be parsed when extracting video IDs, so CLI commands and library helpers accept pasted Markdown URLs.

### Changed
- Documented the unit-test layout convention and the YouTube URL parsing entrypoint in `AGENTS.md` to speed up future feature work.

## [0.5.4] - 2025-10-18

### Changed
- Expanded the feature-development workflow guidance in `AGENTS.md`, the associated spec, and plan templates to clarify expectations for future contributions.

## [0.5.3] - 2025-10-05

### Changed
- Updated `README.md` to include information about automatic clipboard copying, the `--no-copy` flag, and Markdown formatting.
- Updated `README.md` to include information about displaying video title and description with metadata control flags.

## [0.5.2] - 2025-10-01

### Fixed
- Copy the same Markdown-formatted transcript, title, and description to the clipboard, honoring metadata display flags.

## [0.5.1] - 2025-10-01

### Changed
- Render fetched transcripts in Markdown, including a level-one title, description section header, and transcript section header.

### Fixed
- Allow the `-V`/`--version` flag to work without requiring a subcommand so the CLI prints the version as expected.

## [0.5.0] - 2025-10-01

### Added
- Display the YouTube video title and description ahead of transcripts in the CLI with new opt-out flags for each field and all metadata.
- Cache metadata alongside transcripts to reuse previously fetched titles and descriptions.

### Changed
- Introduced a metadata gateway and transcript bundle domain model so metadata and transcripts are fetched together.

## [0.4.5] - 2025-10-08

### Added
- Added a `--version`/`-V` flag to the CLI to display the installed ytt version.

### Changed
- Ensured the CLI reads the package version when running from a source checkout.

## [0.4.4] - 2025-10-07

### Added
- Introduced a `Makefile` with helpers for installing via `uv` and running the test suite.

### Changed
- Updated the README to recommend `uv` for global and local installations and to document the new helper commands.
- Declared a `[test]` optional dependency group in `pyproject.toml` for installing test tooling with a single flag.

## [0.4.3] - 2025-10-01

### Fixed
- Fixed compatibility with youtube-transcript-api v1.1.0+ which changed return format from dict objects to FetchedTranscriptSnippet objects
- Updated transcript repository to use FetchedTranscriptSnippet objects with .text, .start, and .duration attributes
- Added test to verify FetchedTranscriptSnippet format works correctly

## [0.4.2] - 2025-06-22

### Changed
- Refactored the CLI into domain, application, and infrastructure layers to better align with domain-driven design principles.
- Introduced adapter services for configuration, clipboard, caching, and transcript retrieval to compose dependencies cleanly.
- Added ADR 001 documenting the new layered architecture and package layout.


## [0.4.1] - 2025-06-21

### Fixed
- Updated youtube-transcript-api dependency version constraint to ensure compatibility with latest releases


## [0.4.0] - 2025-06-20

### Fixed
- Fixed ModuleNotFoundError that occurred when installing with `pipx install git+https://github.com/dudarev/ytt.git`
- Resolved packaging issues by restructuring code into proper Python package format

### Changed
- Restructured project to use standard `src/` layout for better packaging practices
- Moved main module from `ytt.py` to `src/ytt/main.py` with proper package structure
- Updated `pyproject.toml` to reflect new package structure and support proper entry points
- Improved package discovery configuration in build system

### Technical Details
- Created `src/ytt/__init__.py` to properly export the main function
- Updated setuptools configuration to find packages in `src/` directory
- Maintained backward compatibility for all CLI commands and functionality


## [0.3.0] - 2025-05-22

### Added
- Automatic copying of fetched transcripts to the system clipboard.
- Added `--no-copy` command-line flag to disable the auto-copy feature.

### Changed
- Refactored code to use `pathlib` instead of `os.path` for improved path handling.


## [0.2.0] - 2025-05-11

### Added
- Support for extracting video IDs from YouTube Shorts URLs (e.g., `https://www.youtube.com/shorts/VIDEO_ID`).
- Started the ADR (Architecture Decision Record) process; the first ADR documents the decision to keep a changelog following the Keep a Changelog format.


## [0.1.0] - 2025-04-24

### Added
- Initial version of the `ytt` script.
- Fetches YouTube video transcripts using the `youtube-transcript-api` library.
- Extracts video IDs from various YouTube URL formats (standard watch, youtu.be, embed, /v/).
- Supports specifying preferred transcript languages via a configuration file.
- Includes a `config` command to set preferred languages (e.g., `ytt config languages en,es`).
- Implements caching of fetched transcripts using `pickle` to reduce redundant API calls. Caches are stored in a user-specific cache directory managed by `appdirs`.
- Configuration is stored in a user-specific config directory managed by `appdirs`.
- Provides a command-line interface using `argparse` for fetching transcripts and managing configuration.
- Handles potential errors like `NoTranscriptFound` and `TranscriptsDisabled`.
- Prints the fetched transcript text directly to standard output.
- `ar.md` file to track ideas.
