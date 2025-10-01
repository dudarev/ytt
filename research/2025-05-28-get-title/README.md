# Research: Extracting YouTube Video Titles (May 28, 2025)

This note documents a quick investigation into practical ways to obtain a YouTube
video's title directly from its public watch page. It mirrors the description
research performed on May 27th, but focuses on titles instead of descriptions.

## Goal

Create a small script that downloads a handful of YouTube pages and demonstrates
multiple strategies for locating the video title. We specifically tested the
following sample videos:

* https://www.youtube.com/watch?v=SS39yl1UiNA
* https://www.youtube.com/watch?v=CYKzGwffWr8
* https://www.youtube.com/watch?v=uE0r51pneSA

## Findings

Three reliable sources for the title were identified:

1. **Open Graph tag** – `<meta property="og:title" content="…">` contains a
   clean version of the video title and is easy to access via standard HTML
   parsing.
2. **HTML `<title>` element** – mirrors the title seen in the browser tab. It
   often includes "- YouTube" as a suffix but is trivial to parse.
3. **`ytInitialPlayerResponse` JSON** – within the page's inline JavaScript,
   the `videoDetails.title` field provides the canonical title. This source is
   useful if you are already extracting other structured data from the same JSON
   blob.

Across the tested videos all three sources were present and returned identical
strings except for the `" - YouTube"` suffix in the `<title>` element. The JSON
value exactly matched the Open Graph title.

## Script

The script `get_title_research.py` implements the three extraction strategies:

```bash
python research/2025-05-28-get-title/get_title_research.py
```

For each sample URL it prints the title discovered through every method along
with basic notes if a source could not be located. This makes it easy to compare
outputs or extend the experiment with more URLs.

## Next Steps

* If the Open Graph title ever differs from the canonical title, the script can
  be extended to highlight mismatches explicitly.
* Introduce simple caching or rate limiting if the research grows to cover many
  videos to avoid unnecessary repeated downloads.
* Integrate the JSON-based approach into reusable utilities if other metadata
  (views, channel, etc.) is needed for the broader project.
