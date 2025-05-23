import unittest
from unittest.mock import patch, MagicMock
import io # For capturing stderr/stdout
import sys
from pathlib import Path

# Add project root to sys.path to allow importing ytt
project_root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(project_root))

import ytt

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
    @patch('ytt.get_transcript') # Mock fetching the transcript
    @patch('sys.stdout', new_callable=io.StringIO) # Capture stdout
    @patch('ytt.load_config') # Mock loading config
    @patch('ytt.extract_video_id') # Mock extracting video ID
    def test_copy_successful(self, mock_extract_video_id, mock_load_config, mock_stdout, mock_get_transcript, mock_pyperclip_copy):
        mock_extract_video_id.return_value = "test_video_id" # Dummy video ID
        mock_get_transcript.return_value = self.sample_transcript_data
        mock_load_config.return_value = {'preferred_languages': ['en']} # Mock config

        # Simulate command line arguments for a fetch command
        test_args = ['ytt.py', 'fetch', 'some_url']
        with patch.object(sys, 'argv', test_args):
            try:
                ytt.main()
            except SystemExit as e: # Catch sys.exit calls
                self.assertEqual(e.code, None) # Or check for specific exit codes if expected

        mock_pyperclip_copy.assert_called_once_with(self.expected_transcript_string)
        self.assertIn(self.expected_transcript_string, mock_stdout.getvalue().replace('\\n', '\n'))


    @patch('ytt.pyperclip.copy')
    @patch('ytt.get_transcript')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('ytt.load_config')
    @patch('ytt.extract_video_id')
    def test_no_copy_flag(self, mock_extract_video_id, mock_load_config, mock_stdout, mock_get_transcript, mock_pyperclip_copy):
        mock_extract_video_id.return_value = "test_video_id"
        mock_get_transcript.return_value = self.sample_transcript_data
        mock_load_config.return_value = {'preferred_languages': ['en']}

        test_args = ['ytt.py', 'fetch', 'some_url', '--no-copy']
        with patch.object(sys, 'argv', test_args):
            try:
                ytt.main()
            except SystemExit as e:
                self.assertEqual(e.code, None)

        mock_pyperclip_copy.assert_not_called()
        self.assertIn(self.expected_transcript_string, mock_stdout.getvalue().replace('\\n', '\n'))

    @patch('ytt.pyperclip.copy', side_effect=pyperclip.PyperclipException("Mock clipboard error"))
    @patch('ytt.get_transcript')
    @patch('sys.stderr', new_callable=io.StringIO) # Capture stderr
    @patch('sys.stdout', new_callable=io.StringIO) # Capture stdout
    @patch('ytt.load_config')
    @patch('ytt.extract_video_id')
    def test_copy_fails_gracefully(self, mock_extract_video_id, mock_load_config, mock_stdout, mock_stderr, mock_get_transcript, mock_pyperclip_copy_fails):
        mock_extract_video_id.return_value = "test_video_id"
        mock_get_transcript.return_value = self.sample_transcript_data
        mock_load_config.return_value = {'preferred_languages': ['en']}

        test_args = ['ytt.py', 'fetch', 'some_url']
        with patch.object(sys, 'argv', test_args):
            try:
                ytt.main()
            except SystemExit as e:
                self.assertEqual(e.code, None)
        
        mock_pyperclip_copy_fails.assert_called_once()
        # The error message in ytt.py was updated to be more specific
        self.assertIn("Warning: Could not copy to clipboard: Mock clipboard error", mock_stderr.getvalue())
        self.assertIn(self.expected_transcript_string, mock_stdout.getvalue().replace('\\n', '\n'))

if __name__ == '__main__':
    # Create tests directory if it doesn't exist
    if not Path('tests').exists():
        Path('tests').mkdir()
    unittest.main()
