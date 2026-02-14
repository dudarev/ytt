from ytt.infrastructure.metadata import YouTubeMetadataGateway


def test_extract_description_skips_known_youtube_boilerplate():
    gateway = YouTubeMetadataGateway()
    player_response = {
        "videoDetails": {
            "shortDescription": (
                "Enjoy the videos and music you love, upload original content, "
                "and share it all with friends, family, and the world on YouTube."
            )
        }
    }

    assert gateway._extract_description(player_response, None, "") is None


def test_extract_description_skips_boilerplate_with_whitespace_and_case_variants():
    gateway = YouTubeMetadataGateway()
    player_response = {
        "videoDetails": {
            "shortDescription": (
                "  ENJOY the videos and music you love,\nupload original content,\n"
                "and share it all with friends, family, and the world on YouTube!  "
            )
        }
    }

    assert gateway._extract_description(player_response, None, "") is None


def test_extract_description_keeps_non_boilerplate_text():
    gateway = YouTubeMetadataGateway()
    player_response = {
        "videoDetails": {
            "shortDescription": "Quick walkthrough of the top 3 keyboard shortcuts."
        }
    }

    assert gateway._extract_description(player_response, None, "") == (
        "Quick walkthrough of the top 3 keyboard shortcuts."
    )
