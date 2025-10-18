import sys
import unittest
from pathlib import Path

project_root = Path(__file__).resolve().parents[4]
src_root = project_root / "src"
sys.path.insert(0, str(src_root))
sys.path.insert(1, str(project_root))

from ytt.domain.value_objects import VideoID, extract_video_id


class TestExtractVideoID(unittest.TestCase):
    def test_markdown_watch_url(self):
        link = "[Video](https://www.youtube.com/watch?v=BsWxPI9UM4c&t=2s)"
        video_id = extract_video_id(link)
        self.assertIsInstance(video_id, VideoID)
        self.assertEqual(video_id.value, "BsWxPI9UM4c")

    def test_markdown_short_url(self):
        link = "[Short](https://youtu.be/BsWxPI9UM4c?si=abc)"
        video_id = extract_video_id(link)
        self.assertIsInstance(video_id, VideoID)
        self.assertEqual(video_id.value, "BsWxPI9UM4c")

    def test_markdown_embed_url(self):
        link = "[Embed](https://www.youtube.com/embed/BsWxPI9UM4c?autoplay=1)"
        video_id = extract_video_id(link)
        self.assertIsInstance(video_id, VideoID)
        self.assertEqual(video_id.value, "BsWxPI9UM4c")

    def test_malformed_markdown_falls_back(self):
        link = "[Broken](https://www.youtube.com/watch?v=BsWxPI9UM4c"
        self.assertIsNone(extract_video_id(link))

    def test_plain_text_with_markdown_inside_sentence(self):
        link = "See [context](https://www.youtube.com/watch?v=BsWxPI9UM4c) for details."
        video_id = extract_video_id(link)
        self.assertIsInstance(video_id, VideoID)
        self.assertEqual(video_id.value, "BsWxPI9UM4c")

    def test_non_markdown_string_returns_none(self):
        self.assertIsNone(extract_video_id("not a url at all"))


if __name__ == "__main__":
    unittest.main()
