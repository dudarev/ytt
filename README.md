# YouTube Transcript Tool (ytt)

A simple command-line interface (CLI) tool to fetch and display the transcript of a YouTube video using pre-configured preferred languages.

This tool wraps the [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) Python library, simplifying the process of fetching YouTube video transcripts.


## Features
- Automatically extracts video ID from multiple YouTube URL formats (including Shorts)
- Outputs video title and description along with the transcript in Markdown format
- Automatically copies the output to the clipboard
- Prioritizes manually created transcripts based on preferred languages
- Falls back to automatically generated transcripts if no manual ones are available
- Caches previously fetched transcripts and metadata to speed up repeated requests


## Installation

### Try it instantly with `uvx`

[`uvx`](https://docs.astral.sh/uv/concepts/tools/#uvx) lets you run tools directly from a repository without installing them permanently:

```bash
uvx --from git+https://github.com/dudarev/ytt.git ytt --help
```

This downloads and executes the latest version of `ytt`. You can swap `--help` for any other command arguments.

### Global installs with `uv`

Install the CLI globally when you want it always available on your PATH:

```bash
uv tool install --force --from git+https://github.com/dudarev/ytt.git ytt
```

The `--force` flag ensures you always get the latest version, even if the tool is already installed.

If you prefer to install from a local checkout (for example, after building release artifacts), run the following from inside the repository directory:

```bash
uv tool install --force --from . ytt
```

You can remove a global installation at any time with:

```bash
uv tool uninstall ytt
```

### Develop from a local checkout

1.  **Clone the repository (or download the source code):**
    ```bash
    git clone https://github.com/dudarev/ytt.git
    cd ytt
    ```

2.  **Install the project along with its optional test dependencies:**

    ```bash
    uv pip install --reinstall -e .[test]
    ```

    The `--reinstall` flag forces `uv` to refresh the editable install so you always develop against the current source. The `[test]` extra pulls in the tools required to run the test suite.

    Alternatively, you can use the provided `Makefile` helpers:

    ```bash
    make            # shows available commands
    make install-local       # installs the package in editable mode with test dependencies (forced reinstall)
    make install-global      # installs the current checkout globally (forced reinstall)
    make uninstall-global    # removes the globally installed ytt tool
    make test                # runs the test suite via pytest
    ```


## Usage

There are two main commands: `config` and `fetch` (which is the default).

### 1. Configure Preferred Languages (Required First Step)

Before fetching any transcripts, you **must** configure your preferred language codes. The tool will try these languages in the order you specify.

Run the `config` command:

```bash
ytt config languages <lang1>,<lang2>,...
```

**Example:** Set English, then Spanish, then French as preferred languages:

```bash
ytt config languages en,es,fr
```

This saves your preferences to a configuration file (e.g., `~/.config/ytt/config.json` on Linux/macOS).

### 2. Fetch Transcript

Once languages are configured, run the tool providing the URL of the YouTube video. If you omit the URL entirely, YTT will try to read a YouTube link from your clipboard:

```bash
ytt <youtube_url>
```
*(This implicitly uses the `fetch` command)*

```bash
ytt  # Uses clipboard contents when no URL is supplied
```

By default, the tool will output the canonical video URL as the first line, followed by the video's title and description, and then the transcript, all formatted in Markdown. The output is also automatically copied to your clipboard.

**Example:**

```bash
ytt "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Output:
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Video Title

## Description
Description text here...

## Transcript
[transcript lines]
```

The tool prioritizes manually created transcripts and will attempt your preferred languages in the given order.
If successful, it will print the URL, title, description and the transcript text to standard output. Errors will be printed to standard error.

**Controlling Output:**

You can control the output with the following flags:

*   `--no-url`: Suppress the video URL line.
*   `--no-title`: Suppress the video title.
*   `--no-description`: Suppress the video description.
*   `--no-metadata`: Suppress the URL, title, and description.
*   `--no-copy`: Do not copy the output to the clipboard.

**Redirecting Output:**

Even though the output is automatically copied to the clipboard, you can still redirect it to a file:

```bash
ytt "<youtube_url>" > transcript.md
```

## Supported URL Formats

The tool attempts to extract the video ID from common YouTube URL formats, including:

*   `https://www.youtube.com/watch?v=VIDEO_ID`
*   `https://youtu.be/VIDEO_ID`
*   `https://www.youtube.com/embed/VIDEO_ID`
*   `https://www.youtube.com/v/VIDEO_ID`
*   `https://www.youtube.com/shorts/VIDEO_ID`

## License

[MIT License](LICENSE.md)
