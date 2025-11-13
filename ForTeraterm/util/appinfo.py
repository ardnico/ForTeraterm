"""Utilities for application metadata and documentation discovery."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

DEFAULT_README_CANDIDATES: Sequence[str] = ("README.pdf", "README.md")


def locate_documentation(
    base_path: Path | None = None,
    candidates: Iterable[str] = DEFAULT_README_CANDIDATES,
) -> Path | None:
    """Return the first existing documentation file within *base_path*.

    Parameters
    ----------
    base_path:
        Directory that contains potential documentation files.  When omitted the
        project root (the directory two levels above this module) is used.
    candidates:
        Filenames to evaluate.  The first existing file is returned.
    """

    if base_path is None:
        base_path = Path(__file__).resolve().parent.parent

    for filename in candidates:
        candidate_path = base_path / filename
        if candidate_path.exists():
            return candidate_path
    return None


def format_version_text(app_module: object) -> str:
    """Format application metadata in a multi-line string.

    The function is resilient to missing metadata by falling back to the string
    ``"unknown"``.  ``app_module`` only needs to expose ``__name__``,
    ``__version__`` and ``__license__`` attributes, mirroring what the
    ``appconf`` module provides in production.
    """

    name = getattr(app_module, "__name__", "unknown")
    version = getattr(app_module, "__version__", "unknown")
    license_name = getattr(app_module, "__license__", "unknown")
    return (
        f"AppName:    {name}\n"
        f"Version:    {version}\n"
        f"License:    {license_name}"
    )


__all__ = ["locate_documentation", "format_version_text", "DEFAULT_README_CANDIDATES"]
