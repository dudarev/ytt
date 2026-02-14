"""Infrastructure gateway for retrieving YouTube video metadata."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from html import unescape
from typing import Optional

import requests
from defusedxml import ElementTree as ET

from ..domain.entities import VideoMetadata
from ..domain.services import MetadataGateway
from ..domain.value_objects import VideoID


_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36"
)

_KNOWN_YOUTUBE_DESCRIPTION_BOILERPLATE = {
    (
        "enjoy the videos and music you love upload original content and "
        "share it all with friends family and the world on youtube"
    ),
}
_YOUTUBE_DESCRIPTION_CORE_PHRASES = (
    "enjoy the videos and music you love",
    "upload original content",
    "share it all with friends family and the world on youtube",
)


@dataclass
class YouTubeMetadataGateway(MetadataGateway):
    """Fetches video metadata by scraping the YouTube watch page."""

    session: Optional[requests.Session] = None
    timeout: float = 10.0

    def __post_init__(self) -> None:
        if self.session is None:
            self.session = requests.Session()
        self.session.headers.setdefault("User-Agent", _USER_AGENT)
        self.session.headers.setdefault("Accept-Language", "en-US,en;q=0.9")

    def fetch(self, video_id: VideoID) -> VideoMetadata:  # noqa: D401 - interface method
        url = f"https://www.youtube.com/watch?v={video_id.value}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as exc:  # pragma: no cover - network defensive
            print(f"Warning: Could not retrieve metadata for {video_id.value}: {exc}", file=sys.stderr)
            return VideoMetadata(title=None, description=None)

        html = response.text
        player_response = self._extract_json_object(html, "ytInitialPlayerResponse")
        initial_data = self._extract_json_object(html, "ytInitialData")
        title = self._extract_title(player_response, html)
        description = self._extract_description(player_response, initial_data, html)
        return VideoMetadata(title=title, description=description)

    # ------------------------------------------------------------------
    # Extraction helpers
    # ------------------------------------------------------------------
    def _extract_json_object(self, html: str, marker: str) -> Optional[dict]:
        marker_index = html.find(marker)
        if marker_index == -1:
            return None
        brace_index = html.find("{", marker_index)
        if brace_index == -1:
            return None

        depth = 0
        for idx in range(brace_index, len(html)):
            char = html[idx]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    candidate = html[brace_index : idx + 1]
                    try:
                        return json.loads(candidate)
                    except json.JSONDecodeError:
                        return None
        return None

    def _extract_title(self, player_response: Optional[dict], html: str) -> Optional[str]:
        title: Optional[str] = None
        if isinstance(player_response, dict):
            title = (
                player_response.get("videoDetails", {}).get("title")
                or player_response.get("microformat", {})
                .get("playerMicroformatRenderer", {})
                .get("title", {})
                .get("simpleText")
            )
            if title:
                return title.strip() or None

        title = self._extract_open_graph(html, "og:title")
        if title:
            return title

        match = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
        if match:
            value = unescape(match.group(1)).strip()
            if value.lower().endswith("- youtube"):
                value = value[:-9].rstrip()
            return value or None
        return None

    def _extract_description(
        self,
        player_response: Optional[dict],
        initial_data: Optional[dict],
        html: str,
    ) -> Optional[str]:
        description: Optional[str] = None
        if isinstance(player_response, dict):
            video_details = player_response.get("videoDetails", {})
            short_description = video_details.get("shortDescription")
            if short_description:
                description = short_description.strip()
            if not description:
                description = (
                    player_response.get("microformat", {})
                    .get("playerMicroformatRenderer", {})
                    .get("description", {})
                    .get("simpleText")
                )
                if isinstance(description, str):
                    description = description.strip()

        normalized_description = self._normalize_description(description)
        if normalized_description:
            return normalized_description

        normalized_description = self._normalize_description(self._extract_from_initial_data(initial_data))
        if normalized_description:
            return normalized_description

        description = self._extract_open_graph(html, "og:description")
        return self._normalize_description(description)

    def _extract_from_initial_data(self, data: Optional[dict]) -> Optional[str]:
        if not isinstance(data, dict):
            return None

        # Walk a handful of observed locations that contain description runs.
        engagement_panels = data.get("engagementPanels") or []
        for panel in engagement_panels:
            renderer = panel.get("engagementPanelSectionListRenderer")
            if not isinstance(renderer, dict):
                continue
            content = renderer.get("content", {})
            section_list_renderer = content.get("sectionListRenderer", {})
            contents = section_list_renderer.get("contents", [])
            for item in contents:
                item_renderer = item.get("itemSectionRenderer", {})
                for inner in item_renderer.get("contents", []):
                    description_renderer = inner.get("videoDescriptionRenderer")
                    if not isinstance(description_renderer, dict):
                        continue
                    runs = description_renderer.get("description", {}).get("runs", [])
                    text = "".join(run.get("text", "") for run in runs if isinstance(run, dict))
                    if text:
                        return text.strip()
        return None

    def _extract_open_graph(self, html: str, property_name: str) -> Optional[str]:
        head_match = re.search(r"<head.*?</head>", html, flags=re.IGNORECASE | re.DOTALL)
        head_html = head_match.group(0) if head_match else html
        fragment = f"<root>{head_html}</root>"
        try:
            root = ET.fromstring(fragment)
        except ET.ParseError:
            root = None

        if root is not None:
            for meta in root.iter("meta"):
                prop = meta.get("property") or meta.get("name")
                if prop and prop.lower() == property_name.lower():
                    content = meta.get("content")
                    if content:
                        return unescape(content.strip()) or None

        pattern = (
            r"<meta[^>]+(?:property|name)=[\"']"
            + re.escape(property_name)
            + r"[\"'][^>]*content=[\"']([^\"']+)[\"']"
        )
        match = re.search(pattern, html, flags=re.IGNORECASE)
        if match:
            return unescape(match.group(1)).strip() or None
        return None

    def _normalize_description(self, description: Optional[str]) -> Optional[str]:
        if not isinstance(description, str):
            return None

        normalized = description.strip()
        if not normalized:
            return None

        if self._is_youtube_boilerplate_description(normalized):
            return None
        return normalized

    def _is_youtube_boilerplate_description(self, description: str) -> bool:
        canonical = self._canonicalize_description(description)
        if canonical in _KNOWN_YOUTUBE_DESCRIPTION_BOILERPLATE:
            return True
        return all(phrase in canonical for phrase in _YOUTUBE_DESCRIPTION_CORE_PHRASES)

    def _canonicalize_description(self, description: str) -> str:
        lowered = description.casefold()
        lowered = re.sub(r"\s+", " ", lowered)
        return re.sub(r"[^a-z0-9 ]", "", lowered).strip()


__all__ = ["YouTubeMetadataGateway"]
