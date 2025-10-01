import unittest
from unittest.mock import patch, MagicMock
import io # For capturing stderr/stdout
import sys
from pathlib import Path

# Add project root to sys.path to allow importing ytt
project_root = Path(__file__).parent.parent.resolve()
src_root = project_root / "src"
sys.path.insert(0, str(src_root))
sys.path.insert(1, str(project_root))

import ytt
from ytt.domain import VideoID

import pyperclip

class TestYttClipboard(unittest.TestCase):

    def setUp(self):
        # Example transcript data
        # Create mock objects that have a 'text' attribute
        mock_line1 = MagicMock()
        mock_line1.text = 'Hello world'
        mock_line2 = MagicMock()
        mock_line2.text = 'This is a test'
        self.sample_transcript_data = [mock_line1, mock_line2]
        self.expected_transcript_string = "Hello world\nThis is a test"

    @patch('ytt.pyperclip.copy')
    @patch('ytt.domain.services.TranscriptService.fetch') # Mock fetching the transcript
    @patch('sys.stdout', new_callable=io.StringIO) # Capture stdout
    @patch('ytt.application.config_service.ConfigService.get_preferred_languages') # Mock loading config
    @patch('ytt.application.fetch_service.extract_video_id') # Mock extracting video ID
    def test_copy_successful(self, mock_extract_video_id, mock_get_languages, mock_stdout, mock_fetch_transcript, mock_pyperclip_copy):
        mock_extract_video_id.return_value = VideoID("test_video_id")
        mock_fetch_transcript.return_value = self.sample_transcript_data
        mock_get_languages.return_value = ['en']

        # Simulate command line arguments for a fetch command
        test_args = ['ytt.py', 'fetch', 'some_url']
        with patch.object(sys, 'argv', test_args):
            try:
                ytt.main()
            except SystemExit as e: # Catch sys.exit calls
                self.assertEqual(e.code, None) # Or check for specific exit codes if expected

        mock_fetch_transcript.assert_called_once()
        mock_pyperclip_copy.assert_called_once_with(self.expected_transcript_string)
        self.assertIn(self.expected_transcript_string, mock_stdout.getvalue().replace('\\n', '\n'))


    @patch('ytt.pyperclip.copy')
    @patch('ytt.domain.services.TranscriptService.fetch')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('ytt.application.config_service.ConfigService.get_preferred_languages')
    @patch('ytt.application.fetch_service.extract_video_id')
    def test_no_copy_flag(self, mock_extract_video_id, mock_get_languages, mock_stdout, mock_fetch_transcript, mock_pyperclip_copy):
        mock_extract_video_id.return_value = VideoID("test_video_id")
        mock_fetch_transcript.return_value = self.sample_transcript_data
        mock_get_languages.return_value = ['en']

        test_args = ['ytt.py', 'fetch', 'some_url', '--no-copy']
        with patch.object(sys, 'argv', test_args):
            try:
                ytt.main()
            except SystemExit as e:
                self.assertEqual(e.code, None)

        mock_fetch_transcript.assert_called_once()
        mock_pyperclip_copy.assert_not_called()
        self.assertIn(self.expected_transcript_string, mock_stdout.getvalue().replace('\\n', '\n'))

    @patch('ytt.pyperclip.copy', side_effect=pyperclip.PyperclipException("Mock clipboard error"))
    @patch('ytt.domain.services.TranscriptService.fetch')
    @patch('sys.stderr', new_callable=io.StringIO) # Capture stderr
    @patch('sys.stdout', new_callable=io.StringIO) # Capture stdout
    @patch('ytt.application.config_service.ConfigService.get_preferred_languages')
    @patch('ytt.application.fetch_service.extract_video_id')
    def test_copy_fails_gracefully(self, mock_extract_video_id, mock_get_languages, mock_stdout, mock_stderr, mock_fetch_transcript, mock_pyperclip_copy_fails):
        mock_extract_video_id.return_value = VideoID("test_video_id")
        mock_fetch_transcript.return_value = self.sample_transcript_data
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
        self.assertIn(self.expected_transcript_string, mock_stdout.getvalue().replace('\\n', '\n'))

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
