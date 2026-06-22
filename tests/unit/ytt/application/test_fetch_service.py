import pytest

from ytt.application.fetch_service import FetchTranscriptUseCase
from ytt.domain import VideoID
from ytt.domain.entities import TranscriptLine, VideoMetadata, VideoTranscriptBundle


class StubTranscriptService:
    def __init__(self, bundle):
        self.bundle = bundle
        self.last_languages = None

    def fetch(self, video_id, preferred_languages, *, refresh=False):
        self.last_languages = list(preferred_languages)
        return self.bundle


class StubConfigService:
    def __init__(self, languages):
        self.languages = languages

    def get_preferred_languages(self):
        return list(self.languages)


class StubClipboard:
    def copy(self, lines):
        return True

    def read(self):
        return ""


def _bundle():
    return VideoTranscriptBundle(
        transcript=[TranscriptLine(text="line", start=0.0, duration=1.0)],
        metadata=VideoMetadata(title="title", description="desc"),
    )


def test_execute_uses_explicit_language_before_configured_languages():
    service = StubTranscriptService(_bundle())
    use_case = FetchTranscriptUseCase(
        service,
        StubConfigService(["en", "de"]),
        StubClipboard(),
        extractor=lambda _: VideoID("aaaaaaaaaaa"),
    )

    use_case.execute(
        "https://www.youtube.com/watch?v=aaaaaaaaaaa",
        copy_to_clipboard=False,
        preferred_language="de-AT",
    )

    assert service.last_languages == ["de-AT", "en", "de"]


def test_execute_with_explicit_language_no_config_still_fetches():
    service = StubTranscriptService(_bundle())
    use_case = FetchTranscriptUseCase(
        service,
        StubConfigService([]),
        StubClipboard(),
        extractor=lambda _: VideoID("aaaaaaaaaaa"),
    )

    use_case.execute(
        "https://www.youtube.com/watch?v=aaaaaaaaaaa",
        copy_to_clipboard=False,
        preferred_language="de-AT",
    )

    assert service.last_languages == ["de-AT"]


def test_execute_without_any_languages_exits():
    service = StubTranscriptService(_bundle())
    use_case = FetchTranscriptUseCase(
        service,
        StubConfigService([]),
        StubClipboard(),
        extractor=lambda _: VideoID("aaaaaaaaaaa"),
    )

    with pytest.raises(SystemExit) as exc:
        use_case.execute(
            "https://www.youtube.com/watch?v=aaaaaaaaaaa",
            copy_to_clipboard=False,
        )

    assert exc.value.code == 1
