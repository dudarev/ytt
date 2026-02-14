from ytt.domain.entities import TranscriptLine, VideoMetadata, VideoTranscriptBundle
from ytt.domain.value_objects import VideoID
from ytt.infrastructure.transcript_repository import CachedYouTubeTranscriptRepository


class StubMetadataGateway:
    def fetch(self, video_id: VideoID) -> VideoMetadata:
        return VideoMetadata(title="fresh", description="fresh description")


class ProbeRepository(CachedYouTubeTranscriptRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_cache_called = False
        self.fetch_from_api_called = False

    def _load_cache(self, cache_path):
        self.load_cache_called = True
        return VideoTranscriptBundle(
            transcript=[TranscriptLine(text="cached", start=0.0, duration=1.0)],
            metadata=VideoMetadata(title="cached", description="cached"),
        )

    def _fetch_from_api(self, video_id, preferred_languages):
        self.fetch_from_api_called = True
        return [TranscriptLine(text="fresh", start=0.0, duration=1.0)]


def test_retrieve_uses_cache_by_default(tmp_path):
    repository = ProbeRepository(tmp_path, StubMetadataGateway())
    video_id = VideoID("aaaaaaaaaaa")
    cache_path = repository._cache_path(video_id, ["en"])
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_bytes(b"placeholder")

    bundle = repository.retrieve(video_id, ["en"])

    assert bundle is not None
    assert repository.load_cache_called is True
    assert repository.fetch_from_api_called is False
    assert bundle.metadata.title == "cached"


def test_retrieve_skips_cache_when_refresh_is_enabled(tmp_path):
    repository = ProbeRepository(tmp_path, StubMetadataGateway())
    video_id = VideoID("bbbbbbbbbbb")
    cache_path = repository._cache_path(video_id, ["en"])
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_bytes(b"placeholder")

    bundle = repository.retrieve(video_id, ["en"], refresh=True)

    assert bundle is not None
    assert repository.load_cache_called is False
    assert repository.fetch_from_api_called is True
    assert bundle.metadata.title == "fresh"
