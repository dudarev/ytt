"""Clipboard integration."""

from __future__ import annotations

import sys
from typing import Iterable, Protocol

import pyperclip

CLIPBOARD_UTILITIES = ("pbcopy", "xclip", "xsel", "wl-copy")


class ClipboardGateway(Protocol):
    """Abstraction for clipboard behaviour."""

    def copy(self, lines: Iterable[str]) -> bool:
        """Copy the provided lines to the clipboard."""


class PyperclipClipboardGateway:
    """Clipboard gateway implemented using :mod:`pyperclip`."""

    def copy(self, lines: Iterable[str]) -> bool:
        try:
            pyperclip.copy("\n".join(lines))
            return True
        except pyperclip.PyperclipException as exc:  # pragma: no cover - requires clipboard
            message = str(exc).lower()
            if any(utility in message for utility in CLIPBOARD_UTILITIES):
                print(
                    "Warning: Could not copy to clipboard. Please install xclip or xsel (for Linux) or pbcopy (for macOS) or wl-copy (for Wayland).",
                    file=sys.stderr,
                )
            else:
                print(f"Warning: Could not copy to clipboard: {exc}", file=sys.stderr)
            return False
