# YouTube Transcript Tool (ytt)

A simple command-line interface (CLI) tool to fetch and display the transcript of a YouTube video using pre-configured preferred languages.

This tool wraps the [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) Python library, simplifying the process of fetching YouTube video transcripts.


## Features
- Automatically extracts video ID from multiple YouTube URL formats
- Prioritizes manually created transcripts based on preferred languages
- Falls back to automatically generated transcripts if no manual ones are available
- Caches previously fetched transcripts to speed up repeated requests


## Installation Globally 

Consider installing `ytt` as a global command with [pipx](https://github.com/pypa/pipx):

```bash
pipx install git+https://github.com/dudarev/ytt.git
```


## Installation for Development

1.  **Clone the repository (or download the source code):**
    ```bash
    # If you have git installed
    # git clone git@github.com:dudarev/ytt.git
    # cd ytt
    ```

2.  **Install the tool using pip or pipx:**
    Navigate to the project directory (where `pyproject.toml` is located) in your terminal and run:

    ```bash
    pip install -e .
    ```

    This installs the necessary dependencies (like `youtube-transcript-api` and `appdirs`) and makes the `ytt` command available in your current Python environment.


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
