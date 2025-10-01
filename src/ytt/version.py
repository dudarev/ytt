"""Utilities for retrieving the ytt package version."""

from __future__ import annotations

from importlib import metadata
from pathlib import Path

import tomllib


def get_version() -> str:
    """Return the installed version of ytt.

    Attempts to read the version from package metadata first. If the package
    metadata is unavailable (for example when running from a source checkout
    without installation), it falls back to reading the local ``pyproject.toml``
    file. If both strategies fail, ``"unknown"`` is returned.
    """

    try:
        return metadata.version("ytt")
    except metadata.PackageNotFoundError:
        pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"
        if pyproject_path.is_file():
            with pyproject_path.open("rb") as pyproject:
                data = tomllib.load(pyproject)
            version = data.get("project", {}).get("version")
            if isinstance(version, str):
                return version
    return "unknown"


__all__ = ["get_version"]
