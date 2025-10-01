# YouTube Transcript Tool (ytt)

A simple command-line interface (CLI) tool to fetch and display the transcript of a YouTube video using pre-configured preferred languages.

This tool wraps the [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) Python library, simplifying the process of fetching YouTube video transcripts.


## Features
- Automatically extracts video ID from multiple YouTube URL formats
- Prioritizes manually created transcripts based on preferred languages
- Falls back to automatically generated transcripts if no manual ones are available
- Caches previously fetched transcripts to speed up repeated requests


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

Once languages are configured, run the tool providing the URL of the YouTube video:

```bash
ytt <youtube_url>
```
*(This implicitly uses the `fetch` command)*

**Example:**

```bash
ytt "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

The tool prioritizes manually created transcripts and will attempt your preferred languages in the given order.
If successful, it will print only the transcript text to standard output. Errors will be printed to standard error.

**Redirecting Output:**

You can save the transcript directly to a file:

```bash
ytt "<youtube_url>" > transcript.txt
```

or to the clipboard:

```bash
ytt "<youtube_url>" | pbcopy
```

## Supported URL Formats

The tool attempts to extract the video ID from common YouTube URL formats, including:

*   `https://www.youtube.com/watch?v=VIDEO_ID`
*   `https://youtu.be/VIDEO_ID`
*   `https://www.youtube.com/embed/VIDEO_ID`
*   `https://www.youtube.com/v/VIDEO_ID`

## License

[MIT License](LICENSE)
