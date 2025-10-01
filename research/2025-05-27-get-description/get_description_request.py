import html
import json  # For parsing JSON
import re  # For regular expressions
from typing import Dict, Optional, Tuple

import requests

# URLs of the YouTube videos to inspect
VIDEO_URLS = [
    "https://www.youtube.com/watch?v=SS39yl1UiNA",
    "https://www.youtube.com/watch?v=CYKzGwffWr8",
    "https://www.youtube.com/watch?v=uE0r51pneSA",
]

# A realistic User-Agent keeps responses consistent with those returned to browsers
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_video_page(url: str) -> Optional[str]:
    """Fetch the raw HTML for a YouTube video page."""

    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:  # pragma: no cover - networking best effort
        print(f"Error fetching '{url}': {exc}")
        return None

    return response.text


def _search_meta_content(page_content: str, property_name: str) -> Optional[str]:
    """Search for a meta tag with ``property=property_name`` and return its content."""

    pattern = re.compile(
        rf'<meta[^>]+property=["\']{re.escape(property_name)}["\'][^>]+content=["\'](.*?)["\']',
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(page_content)
    if not match:
        return None

    return html.unescape(match.group(1)).strip()


def extract_open_graph_description(page_content: str) -> Tuple[Optional[str], Optional[str]]:
    """Return the Open Graph title and description from the page."""

    title = _search_meta_content(page_content, "og:title")
    description = _search_meta_content(page_content, "og:description")

    return title, description


def _extract_balanced_braces(text: str, start_index: int) -> Optional[str]:
    """Return the JSON string starting at ``start_index`` with balanced braces."""

    if start_index >= len(text) or text[start_index] != "{":
        return None

    brace_level = 0
    in_string = False
    escaped = False

    for i in range(start_index, len(text)):
        char = text[i]

        if escaped:
            escaped = False
            continue

        if char == "\\":
            escaped = True
            continue

        if char == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        if char == "{":
            brace_level += 1
        elif char == "}":
            brace_level -= 1
            if brace_level == 0:
                return text[start_index : i + 1]

    return None


def extract_json_object_after_pattern(page_content: str, pattern: str) -> Optional[Dict]:
    """Search ``page_content`` for ``pattern`` and parse the JSON object that follows."""

    match = re.search(pattern, page_content)
    if not match:
        return None

    json_start = page_content.find("{", match.end())
    if json_start == -1:
        return None

    json_string = _extract_balanced_braces(page_content, json_start)
    if not json_string:
        return None

    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        return None


def extract_description_from_description_object(page_content: str) -> Optional[str]:
    """Parse the first ``"description": {...}`` JSON object and return the contained text."""

    pattern = r'("description"\s*:\s*)(?=\{)'
    match = re.search(pattern, page_content)
    if not match:
        return None

    json_start = match.end()
    json_string = _extract_balanced_braces(page_content, json_start)
    if not json_string:
        return None

    try:
        description_obj = json.loads(json_string)
    except json.JSONDecodeError:
        return None

    if isinstance(description_obj, dict):
        if "simpleText" in description_obj and description_obj["simpleText"]:
            return str(description_obj["simpleText"])
        if "runs" in description_obj and isinstance(description_obj["runs"], list):
            return "".join(str(run.get("text", "")) for run in description_obj["runs"])

    return None


def extract_description_from_player_response(page_content: str) -> Optional[str]:
    """Pull the description from ``ytInitialPlayerResponse`` if present."""

    patterns = [
        r"ytInitialPlayerResponse\s*=\s*",
        r'ytInitialPlayerResponse"\s*:\s*',
    ]

    player_data: Optional[Dict] = None
    for pattern in patterns:
        player_data = extract_json_object_after_pattern(page_content, pattern)
        if player_data:
            break

    if not isinstance(player_data, dict):
        return None

    video_details = player_data.get("videoDetails", {})
    if isinstance(video_details, dict):
        description = video_details.get("shortDescription")
        if description:
            return str(description)

    microformat = player_data.get("microformat", {})
    if isinstance(microformat, dict):
        renderer = microformat.get("playerMicroformatRenderer", {})
        if isinstance(renderer, dict):
            description_obj = renderer.get("description")
            if isinstance(description_obj, dict):
                if "simpleText" in description_obj and description_obj["simpleText"]:
                    return str(description_obj["simpleText"])
                if "runs" in description_obj and isinstance(description_obj["runs"], list):
                    return "".join(str(run.get("text", "")) for run in description_obj["runs"])

    return None


def print_description_report(url: str) -> None:
    """Fetch ``url`` once and display the descriptions extracted via each method."""

    print("=" * 80)
    print(f"Video URL: {url}")

    page_content = fetch_video_page(url)
    if page_content is None:
        print("Failed to fetch page content; skipping analysis.\n")
        return

    og_title, og_description = extract_open_graph_description(page_content)
    if og_title:
        print(f"OG Title: {og_title}")
    else:
        print("OG Title: <not found>")

    if og_description:
        print(f"OG Description: {og_description}")
    else:
        print("OG Description: <not found>")

    json_description = extract_description_from_description_object(page_content)
    if json_description:
        print("Description via description JSON: \n" + json_description)
    else:
        print("Description via description JSON: <not found>")

    player_response_description = extract_description_from_player_response(page_content)
    if player_response_description:
        print("Description via ytInitialPlayerResponse: \n" + player_response_description)
    else:
        print("Description via ytInitialPlayerResponse: <not found>")


if __name__ == "__main__":
    for video_url in VIDEO_URLS:
        print_description_report(video_url)
