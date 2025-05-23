import sys
import re
import argparse
import json
import os
from pathlib import Path
import pickle 
from urllib.parse import urlparse, parse_qs

import pyperclip
from appdirs import user_config_dir
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

CONFIG_DIR_NAME = "ytt"
CONFIG_FILE_NAME = "config.json"
CACHE_DIR_NAME = "cache"
CLIPBOARD_UTILITIES = ["pbcopy", "xclip", "xsel", "wl-copy"]

def get_config_dir():
    """Gets the user-specific config directory for ytt."""
    return Path(user_config_dir(CONFIG_DIR_NAME))

def get_cache_dir():
    """Gets the user-specific cache directory for ytt."""
    config_dir = get_config_dir()
    return config_dir / CACHE_DIR_NAME

def get_config_file_path():
    """Gets the full path to the config file."""
    config_dir = get_config_dir()
    return config_dir / CONFIG_FILE_NAME

def load_config():
    """Loads the configuration from the JSON file."""
    config_path = get_config_file_path()
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not decode config file at {config_path}", file=sys.stderr)
            return {} # Return empty config on error
        except Exception as e:
            print(f"Warning: Error loading config file {config_path}: {e}", file=sys.stderr)
            return {}
    return {} # Return empty config if file doesn't exist

def save_config(config_data):
    """Saves the configuration to the JSON file."""
    config_dir = get_config_dir()
    config_path = get_config_file_path()
    try:
        config_dir.mkdir(parents=True, exist_ok=True) # Ensure directory exists
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=4)
    except Exception as e:
        print(f"Error saving config file {config_path}: {e}", file=sys.stderr)
        sys.exit(1)

def extract_video_id(url):
    """
    Extracts the YouTube video ID from a URL.
    Handles various YouTube URL formats.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Standard watch URL: https://www.youtube.com/watch?v=VIDEO_ID
    if parsed_url.netloc in ('www.youtube.com', 'youtube.com') and \
       parsed_url.path == '/watch' and 'v' in query_params:
        return query_params['v'][0]

    # Shortened URL: https://youtu.be/VIDEO_ID
    if parsed_url.netloc == 'youtu.be' and parsed_url.path:
        return parsed_url.path[1:] # Remove leading '/'

    # Embed URL: https://www.youtube.com/embed/VIDEO_ID
    if parsed_url.path.startswith('/embed/'):
        return parsed_url.path.split('/')[2]

    # /v/ URL: https://www.youtube.com/v/VIDEO_ID
    if parsed_url.path.startswith('/v/'):
        return parsed_url.path.split('/')[2]

    # Shorts URL: https://www.youtube.com/shorts/VIDEO_ID
    if parsed_url.path.startswith('/shorts/'):
        return parsed_url.path.split('/')[2]

    # Add more patterns here if needed

    return None

# --- Helper functions for get_transcript ---

def _get_cache_filepath(video_id, preferred_languages):
    """Constructs the cache filepath for a given video ID and languages."""
    cache_dir = get_cache_dir()
    lang_key = "_".join(sorted([lang.lower() for lang in preferred_languages])) if preferred_languages else "any"
    cache_filename = f"{video_id}_{lang_key}.pkl" # Changed extension to .pkl
    return cache_dir / cache_filename, cache_dir, lang_key

def _load_from_cache(cache_filepath):
    """Loads transcript data from a given cache file path using pickle."""
    try:
        # Use binary read mode 'rb' for pickle
        with open(cache_filepath, 'rb') as f:
            return pickle.load(f)
    except pickle.UnpicklingError:
        print(f"Warning: Could not unpickle cache file {cache_filepath}. Fetching again.", file=sys.stderr)
    except FileNotFoundError:
         # This shouldn't happen if Path.exists() check passes, but good practice
         print(f"Warning: Cache file not found {cache_filepath} despite check. Fetching again.", file=sys.stderr)
    except Exception as e:
        print(f"Warning: Error reading cache file {cache_filepath}: {e}. Fetching again.", file=sys.stderr)
    return None # Return None if loading fails

def _save_to_cache(cache_filepath, cache_dir, transcript_data):
    """Saves transcript data to the cache using pickle."""
    try:
        cache_dir.mkdir(parents=True, exist_ok=True) # Ensure cache directory exists
        # Use binary write mode 'wb' for pickle
        with open(cache_filepath, 'wb') as f:
            pickle.dump(transcript_data, f)
    except Exception as e:
        print(f"Warning: Could not save transcript to cache file {cache_filepath}: {e}", file=sys.stderr)


def _find_transcript_object(transcript_list, preferred_languages):
    """Finds the most suitable transcript object from the list."""
    # List all manually created transcripts
    manual_transcripts = [t for t in transcript_list if not t.is_generated]

    # If there is only one manually created transcript, return it
    if len(manual_transcripts) == 1:
        return manual_transcripts[0]

    # If there are multiple manually created transcripts, prioritize by preferred languages
    if manual_transcripts and preferred_languages:
        for lang in preferred_languages:
            for transcript in manual_transcripts:
                if transcript.language == lang:
                    return transcript

    # If no preferred manual transcript is found, fall back to any generated transcript
    if preferred_languages:
        try:
            return transcript_list.find_generated_transcript(preferred_languages)
        except NoTranscriptFound:
            pass

    # If no preferred or generated transcript is found, try any manual transcript
    if manual_transcripts:
        return manual_transcripts[0]

    # If no manual transcripts are found, try any generated transcript
    generated_transcripts = [t for t in transcript_list if t.is_generated]
    if generated_transcripts:
        return generated_transcripts[0]

    # If no transcripts are found at all, raise NoTranscriptFound
    raise NoTranscriptFound("No suitable transcript found in the list.")


def _fetch_from_api(video_id, preferred_languages):
    """Fetches the transcript from the YouTube API."""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript_object = _find_transcript_object(transcript_list, preferred_languages)
        if transcript_object:
            return transcript_object.fetch()
        else:
            # This case should ideally be covered by _find_transcript_object raising NoTranscriptFound
            print(f"Error: Could not find a suitable transcript object for video ID: {video_id}", file=sys.stderr)
            return None
    except NoTranscriptFound:
        # This catches the NoTranscriptFound raised by _find_transcript_object if absolutely no transcript is found
        print(f"Error: No transcript found for video ID: {video_id} (tried languages: {preferred_languages if preferred_languages else 'any'})", file=sys.stderr)
        return None
    except TranscriptsDisabled:
        print(f"Error: Transcripts are disabled for video ID: {video_id}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred during API fetch: {e}", file=sys.stderr)
        return None

# --- Main get_transcript function ---

def get_transcript(video_id, preferred_languages=None):
    """
    Fetches and returns the transcript for a given video ID.
    Tries preferred languages first if provided.
    Uses caching to avoid redundant API calls.
    """
    if not preferred_languages:
        preferred_languages = [] # Ensure it's a list

    cache_filepath, cache_dir, lang_key = _get_cache_filepath(video_id, preferred_languages)

    # 1. Check cache
    if cache_filepath.exists():
        cached_data = _load_from_cache(cache_filepath)
        if cached_data:
            return cached_data # Return data from cache if loaded successfully

    # 2. Fetch from API if cache miss or load failed
    transcript_data = _fetch_from_api(video_id, preferred_languages)

    # 3. Save to cache if fetched successfully
    if transcript_data:
        _save_to_cache(cache_filepath, cache_dir, transcript_data)

    return transcript_data # Return fetched data (or None if fetch failed)


def print_transcript(transcript_data):
    """
    Prints the transcript data in a simple format.
    """
    if not transcript_data:
        return
    for entry in transcript_data:
        print(entry.text)


def copy_to_clipboard(transcript):
    """
    Copies transcript text to clipboard and handles potential clipboard errors.
    Returns True if successful, False otherwise.
    """
    try:
        transcript_text = "\n".join([line.text for line in transcript])
        pyperclip.copy(transcript_text)
        return True
    except pyperclip.PyperclipException as e:
        # Check if the error message indicates a missing copy/paste mechanism
        if any(utility in str(e).lower() for utility in CLIPBOARD_UTILITIES):
            print(
                "Warning: Could not copy to clipboard. Please install xclip or xsel (for Linux) or pbcopy (for macOS) or wl-copy (for Wayland).",
                file=sys.stderr
            )
        else:
            # Print a generic error message for other PyperclipExceptions
            print(f"Warning: Could not copy to clipboard: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Fetch YouTube video transcripts or manage configuration.',
        usage='ytt <youtube_url> | ytt config <setting> <value>'
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # --- Fetch transcript command ---
    fetch_parser = subparsers.add_parser('fetch', help='Fetch transcript for a given URL (default command if none specified)')
    fetch_parser.add_argument('youtube_url', help='The URL of the YouTube video.')
    fetch_parser.add_argument(
        '--no-copy',
        action='store_true',
        help='Do not copy the transcript to the clipboard.'
    )

    # --- Config command ---
    config_parser = subparsers.add_parser('config', help='Configure ytt settings.')
    config_parser.add_argument('setting', help='The configuration setting to modify (e.g., languages).')
    config_parser.add_argument('value', help='The value to set for the setting (e.g., \'en,es,fr\').')

    # Load existing config
    config = load_config()

    # Handle case where no command is specified (treat as 'fetch')
    args_list = sys.argv[1:]
    if not args_list or args_list[0] not in ['fetch', 'config']:
        # Check if it looks like a URL to default to fetch
        if args_list and ('http://' in args_list[0] or 'https://' in args_list[0]):
             args_list.insert(0, 'fetch')
        else:
             # If no command and not a URL, show help
             parser.print_help(sys.stderr)
             sys.exit(1)

    args = parser.parse_args(args_list)

    if args.command == 'config':
        if args.setting.lower() == 'languages':
            langs = [lang.strip() for lang in args.value.split(',') if lang.strip()]
            config['preferred_languages'] = langs
            save_config(config)
        else:
            print(f"Error: Unknown config setting '{args.setting}'. Only 'languages' is supported.", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'fetch':
        video_id = extract_video_id(args.youtube_url)

        if not video_id:
            print(f"Error: Could not extract video ID from URL: {args.youtube_url}", file=sys.stderr)
            sys.exit(1)

        # Check ONLY the config for preferred languages
        if 'preferred_languages' in config and config['preferred_languages']:
            preferred_langs = config['preferred_languages']
        else:
            # If no languages in config, print error and exit
            print("Error: Preferred languages not set in configuration.", file=sys.stderr)
            print("Please set them using: ytt config languages <lang1>,<lang2>,...", file=sys.stderr)
            print("Example: ytt config languages en,es,fr", file=sys.stderr)
            sys.exit(1)

        transcript = get_transcript(video_id, preferred_languages=preferred_langs)

        if transcript:
            if not args.no_copy:
                copy_to_clipboard(transcript)
            print_transcript(transcript)
        else:
            sys.exit(1)
    else:
         # Should not happen with the logic above, but good practice
         parser.print_help(sys.stderr)
         sys.exit(1)

if __name__ == "__main__":
    main()
