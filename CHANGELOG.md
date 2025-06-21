# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


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
