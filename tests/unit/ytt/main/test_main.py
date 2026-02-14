import pyperclip
import pytest

from ytt.main import _prepare_args
from ytt.infrastructure import PyperclipClipboardGateway


class StubClipboard:
    def __init__(self, text: str):
        self.text = text

    def copy(self, lines):
        return True

    def read(self) -> str:
        return self.text


def test_prepare_args_uses_clipboard_when_no_args():
    clipboard = StubClipboard("https://youtu.be/example")

    parser, args = _prepare_args([], clipboard)

    assert args.command == "fetch"
    assert args.youtube_url == "https://youtu.be/example"


def test_prepare_args_fetch_without_url_uses_clipboard():
    clipboard = StubClipboard("https://youtu.be/example")

    parser, args = _prepare_args(["fetch", "--refresh"], clipboard)

    assert args.command == "fetch"
    assert args.youtube_url == "https://youtu.be/example"
    assert args.refresh is True


def test_prepare_args_top_level_refresh_uses_clipboard():
    clipboard = StubClipboard("https://youtu.be/example")

    parser, args = _prepare_args(["--refresh"], clipboard)

    assert args.command == "fetch"
    assert args.youtube_url == "https://youtu.be/example"
    assert args.refresh is True


def test_prepare_args_errors_on_empty_clipboard(capsys):
    clipboard = StubClipboard("   ")

    with pytest.raises(SystemExit) as excinfo:
        _prepare_args([], clipboard)

    assert excinfo.value.code == 1
    stderr = capsys.readouterr().err
    assert "Clipboard is empty" in stderr
    assert "usage: ytt" in stderr


def test_prepare_args_errors_on_invalid_clipboard_value(capsys):
    clipboard = StubClipboard("not a youtube url")

    with pytest.raises(SystemExit) as excinfo:
        _prepare_args([], clipboard)

    assert excinfo.value.code == 1
    stderr = capsys.readouterr().err
    assert "No YouTube URL found in clipboard" in stderr
    assert "usage: ytt" in stderr


def test_prepare_args_fetch_without_url_errors_on_empty_clipboard(capsys):
    clipboard = StubClipboard("   ")

    with pytest.raises(SystemExit) as excinfo:
        _prepare_args(["fetch", "--refresh"], clipboard)

    assert excinfo.value.code == 1
    stderr = capsys.readouterr().err
    assert "Clipboard is empty" in stderr
    assert "usage: ytt" in stderr


def test_prepare_args_top_level_refresh_errors_on_invalid_clipboard(capsys):
    clipboard = StubClipboard("not a youtube url")

    with pytest.raises(SystemExit) as excinfo:
        _prepare_args(["--refresh"], clipboard)

    assert excinfo.value.code == 1
    stderr = capsys.readouterr().err
    assert "No YouTube URL found in clipboard" in stderr
    assert "usage: ytt" in stderr


def test_prepare_args_top_level_help_not_rewritten_to_fetch():
    clipboard = StubClipboard("https://youtu.be/example")

    with pytest.raises(SystemExit) as excinfo:
        _prepare_args(["--help"], clipboard)

    assert excinfo.value.code == 0


def test_prepare_args_unknown_top_level_flag_still_errors():
    clipboard = StubClipboard("https://youtu.be/example")

    with pytest.raises(SystemExit) as excinfo:
        _prepare_args(["--not-a-real-flag"], clipboard)

    assert excinfo.value.code == 2


def test_prepare_args_reports_clipboard_exceptions(capsys, monkeypatch):
    gateway = PyperclipClipboardGateway()

    def raise_clipboard_error():
        raise pyperclip.PyperclipException("Mock read error")

    monkeypatch.setattr(pyperclip, "paste", raise_clipboard_error)

    with pytest.raises(SystemExit) as excinfo:
        _prepare_args([], gateway)

    assert excinfo.value.code == 1
    assert "Warning: Could not read from clipboard: Mock read error" in capsys.readouterr().err
