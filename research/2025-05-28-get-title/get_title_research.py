"""Research script for extracting YouTube video titles from raw HTML pages.

This script fetches several YouTube video pages and demonstrates three different
strategies for discovering the video title:

1. Open Graph meta tag (`<meta property="og:title" content="...">`).
2. The HTML `<title>` element rendered for browsers.
3. JSON data embedded in `ytInitialPlayerResponse` (specifically the
   `videoDetails.title` field), which tends to match the title used by YouTube's
   internal APIs.

Running this file will iterate over a list of sample videos and print the
results of each strategy so that the differences, if any, can be observed.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Iterable, Optional

import requests
from bs4 import BeautifulSoup


@dataclass
class TitleExtractionResult:
    url: str
    og_title: Optional[str]
    html_title: Optional[str]
    json_title: Optional[str]
    errors: list[str]


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


def fetch_html(url: str) -> str:
    """Return the response text for a YouTube URL using a desktop UA."""

    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return response.text


def extract_og_title(soup: BeautifulSoup) -> Optional[str]:
    meta_tag = soup.find("meta", property="og:title")
    return meta_tag["content"].strip() if meta_tag and meta_tag.has_attr("content") else None


def extract_html_title(soup: BeautifulSoup) -> Optional[str]:
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return None


YT_INITIAL_PLAYER_RESPONSE_PATTERN = re.compile(
    r"ytInitialPlayerResponse\s*=\s*(\{.+?\})\s*;",
    re.DOTALL,
)


def extract_json_title(html: str) -> Optional[str]:
    match = YT_INITIAL_PLAYER_RESPONSE_PATTERN.search(html)
    if not match:
        return None

    raw_json = match.group(1)

    # The embedded JSON occasionally contains sequences that are invalid until
    # we unescape certain characters. The simplest approach is to leverage
    # Python's JSON parser directly – YouTube's markup for this script is valid
    # JSON.
    try:
        player_response = json.loads(raw_json)
    except json.JSONDecodeError:
        return None

    video_details = player_response.get("videoDetails")
    if not isinstance(video_details, dict):
        return None

    title = video_details.get("title")
    return title.strip() if isinstance(title, str) else None


def collect_titles(url: str) -> TitleExtractionResult:
    errors: list[str] = []
    try:
        html = fetch_html(url)
    except requests.RequestException as exc:  # pragma: no cover - research script
        errors.append(f"Network error: {exc}")
        return TitleExtractionResult(url, None, None, None, errors)

    soup = BeautifulSoup(html, "html.parser")

    og_title = extract_og_title(soup)
    if og_title is None:
        errors.append("Open Graph title missing")

    html_title = extract_html_title(soup)
    if html_title is None:
        errors.append("HTML <title> element missing")

    json_title = extract_json_title(html)
    if json_title is None:
        errors.append("ytInitialPlayerResponse title missing")

    return TitleExtractionResult(url, og_title, html_title, json_title, errors)


def format_result(result: TitleExtractionResult) -> str:
    lines = [f"URL: {result.url}"]
    lines.append(f"  og:title           : {result.og_title!r}")
    lines.append(f"  <title>            : {result.html_title!r}")
    lines.append(f"  videoDetails.title : {result.json_title!r}")
    if result.errors:
        lines.append("  Notes:")
        for err in result.errors:
            lines.append(f"    - {err}")
    return "\n".join(lines)


def run(urls: Iterable[str]) -> None:
    for url in urls:
        result = collect_titles(url)
        print(format_result(result))
        print("-" * 80)


SAMPLE_VIDEOS = [
    "https://www.youtube.com/watch?v=SS39yl1UiNA",
    "https://www.youtube.com/watch?v=CYKzGwffWr8",
    "https://www.youtube.com/watch?v=uE0r51pneSA",
]


if __name__ == "__main__":
    run(SAMPLE_VIDEOS)
