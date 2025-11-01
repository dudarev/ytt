import unittest
from unittest.mock import patch
import io  # For capturing stderr/stdout
import sys
from pathlib import Path

# Add project root to sys.path to allow importing ytt
project_root = Path(__file__).parent.parent.resolve()
src_root = project_root / "src"
sys.path.insert(0, str(src_root))
sys.path.insert(1, str(project_root))

import ytt
from ytt.domain import VideoID
from ytt.domain.entities import TranscriptLine, VideoMetadata, VideoTranscriptBundle
from ytt.application.fetch_service import FetchTranscriptUseCase

import pyperclip

class TestYttClipboard(unittest.TestCase):

    def setUp(self):
        # Example transcript data
        self.sample_transcript_data = [
            TranscriptLine(text="Hello world", start=0.0, duration=3.5),
            TranscriptLine(text="This is a test", start=3.5, duration=2.1),
        ]
        self.expected_transcript_string = "Hello world\nThis is a test"
        self.sample_metadata = VideoMetadata(
            title="Sample Title",
            description="Sample Description",
        )
        self.sample_bundle = VideoTranscriptBundle(
            transcript=self.sample_transcript_data,
            metadata=self.sample_metadata,
        )
        self.expected_title_header = f"# {self.sample_metadata.title}"
        self.expected_description_header = "## Description"
        self.expected_transcript_header = "## Transcript"
        self.expected_clipboard_full = "\n".join(
            FetchTranscriptUseCase.render_lines(self.sample_bundle)
        )
        self.expected_clipboard_no_title = "\n".join(
            FetchTranscriptUseCase.render_lines(
                self.sample_bundle,
                show_title=False,
                show_url=True,
                input_url="https://www.youtube.com/watch?v=test_video_id",
            )
        )
        self.expected_clipboard_no_description = "\n".join(
            FetchTranscriptUseCase.render_lines(
                self.sample_bundle,
                show_description=False,
                show_url=True,
                input_url="https://www.youtube.com/watch?v=test_video_id",
            )
        )
        self.expected_clipboard_no_metadata = "\n".join(
            FetchTranscriptUseCase.render_lines(
                self.sample_bundle,
                show_title=False,
                show_description=False,
            )
        )
        self.expected_url_line = "https://www.youtube.com/watch?v=test_video_id"
        self.expected_clipboard_with_url = "\n".join(
            FetchTranscriptUseCase.render_lines(
                self.sample_bundle,
                show_url=True,
                input_url="https://www.youtube.com/watch?v=test_video_id",
            )
        )
        self.expected_clipboard_no_url = "\n".join(
            FetchTranscriptUseCase.render_lines(
                self.sample_bundle,
                show_url=False,
                input_url="https://www.youtube.com/watch?v=test_video_id",
            )
        )

    @patch('ytt.pyperclip.copy')
    @patch('ytt.domain.services.TranscriptService.fetch') # Mock fetching the transcript
    @patch('sys.stdout', new_callable=io.StringIO) # Capture stdout
    @patch('ytt.application.config_service.ConfigService.get_preferred_languages') # Mock loading config
    @patch('ytt.application.fetch_service.extract_video_id') # Mock extracting video ID
    def test_copy_successful(self, mock_extract_video_id, mock_get_languages, mock_stdout, mock_fetch_transcript, mock_pyperclip_copy):
        mock_extract_video_id.return_value = VideoID("test_video_id")
        mock_fetch_transcript.return_value = self.sample_bundle
        mock_get_languages.return_value = ['en']

        # Simulate command line arguments for a fetch command
        test_args = ['ytt.py', 'fetch', 'some_url']
        with patch.object(sys, 'argv', test_args):
            try:
                ytt.main()
            except SystemExit as e: # Catch sys.exit calls
                self.assertEqual(e.code, None) # Or check for specific exit codes if expected

        mock_fetch_transcript.assert_called_once()
        mock_pyperclip_copy.assert_called_once_with(self.expected_clipboard_with_url)
        stdout_value = mock_stdout.getvalue().replace('\\n', '\n')
        self.assertIn(self.expected_url_line, stdout_value)
        self.assertIn(self.expected_transcript_header, stdout_value)
        self.assertIn(self.expected_transcript_string, stdout_value)
        self.assertIn(self.expected_title_header, stdout_value)
        self.assertIn(self.expected_description_header, stdout_value)
        self.assertIn(self.sample_metadata.description, stdout_value)


    @patch('ytt.pyperclip.copy')
    @patch('ytt.domain.services.TranscriptService.fetch')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('ytt.application.config_service.ConfigService.get_preferred_languages')
    @patch('ytt.application.fetch_service.extract_video_id')
    def test_no_copy_flag(self, mock_extract_video_id, mock_get_languages, mock_stdout, mock_fetch_transcript, mock_pyperclip_copy):
        mock_extract_video_id.return_value = VideoID("test_video_id")
        mock_fetch_transcript.return_value = self.sample_bundle
        mock_get_languages.return_value = ['en']

        test_args = ['ytt.py', 'fetch', 'some_url', '--no-copy']
        with patch.object(sys, 'argv', test_args):
            try:
                ytt.main()
            except SystemExit as e:
                self.assertEqual(e.code, None)

        mock_fetch_transcript.assert_called_once()
        mock_pyperclip_copy.assert_not_called()
        stdout_value = mock_stdout.getvalue().replace('\\n', '\n')
        self.assertIn(self.expected_transcript_header, stdout_value)
        self.assertIn(self.expected_transcript_string, stdout_value)
        self.assertIn(self.expected_title_header, stdout_value)
        self.assertIn(self.expected_description_header, stdout_value)
        self.assertIn(self.sample_metadata.description, stdout_value)

    @patch('ytt.pyperclip.copy')
    @patch('ytt.domain.services.TranscriptService.fetch')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('ytt.application.config_service.ConfigService.get_preferred_languages')
    @patch('ytt.application.fetch_service.extract_video_id')
    def test_no_title_flag(self, mock_extract_video_id, mock_get_languages, mock_stdout, mock_fetch_transcript, mock_pyperclip_copy):
        mock_extract_video_id.return_value = VideoID("test_video_id")
        mock_fetch_transcript.return_value = self.sample_bundle
        mock_get_languages.return_value = ['en']

        test_args = ['ytt.py', 'fetch', 'some_url', '--no-title']
        with patch.object(sys, 'argv', test_args):
            try:
                ytt.main()
            except SystemExit as exc:
                self.assertIsNone(exc.code)

        mock_fetch_transcript.assert_called_once()
        mock_pyperclip_copy.assert_called_once_with(self.expected_clipboard_no_title)
        stdout_value = mock_stdout.getvalue().replace('\\n', '\n')
        self.assertIn(self.expected_transcript_header, stdout_value)
        self.assertIn(self.expected_transcript_string, stdout_value)
        self.assertIn(self.expected_description_header, stdout_value)
        self.assertIn(self.sample_metadata.description, stdout_value)
        self.assertNotIn(self.expected_title_header, stdout_value)

    @patch('ytt.pyperclip.copy')
    @patch('ytt.domain.services.TranscriptService.fetch')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('ytt.application.config_service.ConfigService.get_preferred_languages')
    @patch('ytt.application.fetch_service.extract_video_id')
    def test_no_description_flag(self, mock_extract_video_id, mock_get_languages, mock_stdout, mock_fetch_transcript, mock_pyperclip_copy):
        mock_extract_video_id.return_value = VideoID("test_video_id")
        mock_fetch_transcript.return_value = self.sample_bundle
        mock_get_languages.return_value = ['en']

        test_args = ['ytt.py', 'fetch', 'some_url', '--no-description']
        with patch.object(sys, 'argv', test_args):
            try:
                ytt.main()
            except SystemExit as exc:
                self.assertIsNone(exc.code)

        mock_fetch_transcript.assert_called_once()
        mock_pyperclip_copy.assert_called_once_with(self.expected_clipboard_no_description)
        stdout_value = mock_stdout.getvalue().replace('\\n', '\n')
        self.assertIn(self.expected_transcript_header, stdout_value)
        self.assertIn(self.expected_transcript_string, stdout_value)
        self.assertIn(self.expected_title_header, stdout_value)
        self.assertNotIn(self.expected_description_header, stdout_value)
        self.assertNotIn(self.sample_metadata.description, stdout_value)

    @patch('ytt.pyperclip.copy')
    @patch('ytt.domain.services.TranscriptService.fetch')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('ytt.application.config_service.ConfigService.get_preferred_languages')
    @patch('ytt.application.fetch_service.extract_video_id')
    def test_no_metadata_flag(self, mock_extract_video_id, mock_get_languages, mock_stdout, mock_fetch_transcript, mock_pyperclip_copy):
        mock_extract_video_id.return_value = VideoID("test_video_id")
        mock_fetch_transcript.return_value = self.sample_bundle
        mock_get_languages.return_value = ['en']

        test_args = ['ytt.py', 'fetch', 'some_url', '--no-metadata']
        with patch.object(sys, 'argv', test_args):
            try:
                ytt.main()
            except SystemExit as exc:
                self.assertIsNone(exc.code)

        mock_fetch_transcript.assert_called_once()
        mock_pyperclip_copy.assert_called_once_with(self.expected_clipboard_no_metadata)
        stdout_value = mock_stdout.getvalue().replace('\\n', '\n')
        self.assertIn(self.expected_transcript_header, stdout_value)
        self.assertIn(self.expected_transcript_string, stdout_value)
        self.assertNotIn(self.expected_title_header, stdout_value)
        self.assertNotIn(self.expected_description_header, stdout_value)
        self.assertNotIn(self.sample_metadata.title, stdout_value)
        self.assertNotIn(self.sample_metadata.description, stdout_value)
        self.assertNotIn(self.expected_url_line, stdout_value)

    @patch('ytt.pyperclip.copy')
    @patch('ytt.domain.services.TranscriptService.fetch')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('ytt.application.config_service.ConfigService.get_preferred_languages')
    @patch('ytt.application.fetch_service.extract_video_id')
    def test_no_url_flag(self, mock_extract_video_id, mock_get_languages, mock_stdout, mock_fetch_transcript, mock_pyperclip_copy):
        mock_extract_video_id.return_value = VideoID("test_video_id")
        mock_fetch_transcript.return_value = self.sample_bundle
        mock_get_languages.return_value = ['en']

        test_args = ['ytt.py', 'fetch', 'some_url', '--no-url']
        with patch.object(sys, 'argv', test_args):
            try:
                ytt.main()
            except SystemExit as exc:
                self.assertIsNone(exc.code)

        mock_fetch_transcript.assert_called_once()
        mock_pyperclip_copy.assert_called_once_with(self.expected_clipboard_no_url)
        stdout_value = mock_stdout.getvalue().replace('\\n', '\n')
        self.assertNotIn(self.expected_url_line, stdout_value)
        self.assertIn(self.expected_transcript_header, stdout_value)
        self.assertIn(self.expected_transcript_string, stdout_value)
        self.assertIn(self.expected_title_header, stdout_value)
        self.assertIn(self.expected_description_header, stdout_value)
        self.assertIn(self.sample_metadata.description, stdout_value)

    @patch('ytt.pyperclip.copy', side_effect=pyperclip.PyperclipException("Mock clipboard error"))
    @patch('ytt.domain.services.TranscriptService.fetch')
    @patch('sys.stderr', new_callable=io.StringIO) # Capture stderr
    @patch('sys.stdout', new_callable=io.StringIO) # Capture stdout
    @patch('ytt.application.config_service.ConfigService.get_preferred_languages')
    @patch('ytt.application.fetch_service.extract_video_id')
    def test_copy_fails_gracefully(self, mock_extract_video_id, mock_get_languages, mock_stdout, mock_stderr, mock_fetch_transcript, mock_pyperclip_copy_fails):
        mock_extract_video_id.return_value = VideoID("test_video_id")
        mock_fetch_transcript.return_value = self.sample_bundle
        mock_get_languages.return_value = ['en']

        test_args = ['ytt.py', 'fetch', 'some_url']
        with patch.object(sys, 'argv', test_args):
            try:
                ytt.main()
            except SystemExit as e:
                self.assertEqual(e.code, None)
        
        mock_fetch_transcript.assert_called_once()
        mock_pyperclip_copy_fails.assert_called_once()
        # The error message in ytt.py was updated to be more specific
        self.assertIn("Warning: Could not copy to clipboard: Mock clipboard error", mock_stderr.getvalue())
        stdout_value = mock_stdout.getvalue().replace('\\n', '\n')
        self.assertIn(self.expected_transcript_header, stdout_value)
        self.assertIn(self.expected_transcript_string, stdout_value)
        self.assertIn(self.expected_title_header, stdout_value)
        self.assertIn(self.expected_description_header, stdout_value)
        self.assertIn(self.sample_metadata.description, stdout_value)

    def test_version_flag_outputs_version(self):
        from ytt.application import build_parser

        parser = build_parser()

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as exit_context:
                parser.parse_args(['--version'])

        self.assertEqual(exit_context.exception.code, 0)
        self.assertIn(ytt.__version__, mock_stdout.getvalue())

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as exit_context:
                with patch.object(sys, 'argv', ['ytt.py', '-V']):
                    ytt.main()

        self.assertEqual(exit_context.exception.code, 0)
        self.assertIn(ytt.__version__, mock_stdout.getvalue())

class TestTranscriptRepository(unittest.TestCase):
    """Test the transcript repository with FetchedTranscriptSnippet objects."""
    
    def test_to_transcript_with_fetched_snippet_objects(self):
        """Test that _to_transcript handles FetchedTranscriptSnippet objects correctly."""
        from ytt.infrastructure.transcript_repository import CachedYouTubeTranscriptRepository
        
        # Mock FetchedTranscriptSnippet objects
        class MockFetchedTranscriptSnippet:
            def __init__(self, text, start, duration):
                self.text = text
                self.start = start
                self.duration = duration
        
        snippets = [
            MockFetchedTranscriptSnippet("Hello world", 0.0, 3.5),
            MockFetchedTranscriptSnippet("This is a test", 3.5, 2.1),
        ]
        
        result = CachedYouTubeTranscriptRepository._to_transcript(snippets)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Hello world")
        self.assertEqual(result[0].start, 0.0)
        self.assertEqual(result[0].duration, 3.5)
        self.assertEqual(result[1].text, "This is a test")
        self.assertEqual(result[1].start, 3.5)
        self.assertEqual(result[1].duration, 2.1)


if __name__ == '__main__':
    # Create tests directory if it doesn't exist
    if not Path('tests').exists():
        Path('tests').mkdir()
    unittest.main()
