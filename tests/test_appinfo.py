from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from ForTeraterm.util.appinfo import format_version_text, locate_documentation


def test_locate_documentation_prefers_pdf(tmp_path: Path) -> None:
    pdf_path = tmp_path / "README.pdf"
    pdf_path.write_text("pdf", encoding="utf-8")
    md_path = tmp_path / "README.md"
    md_path.write_text("md", encoding="utf-8")

    discovered = locate_documentation(tmp_path)
    assert discovered == pdf_path


def test_locate_documentation_falls_back_to_md(tmp_path: Path) -> None:
    md_path = tmp_path / "README.md"
    md_path.write_text("md", encoding="utf-8")

    discovered = locate_documentation(tmp_path)
    assert discovered == md_path


def test_locate_documentation_handles_missing(tmp_path: Path) -> None:
    assert locate_documentation(tmp_path) is None


def test_format_version_text_includes_metadata() -> None:
    metadata = SimpleNamespace(
        __name__="appconf",
        __version__="1.2.3",
        __license__="MIT",
    )

    text = format_version_text(metadata)
    assert "appconf" in text
    assert "1.2.3" in text
    assert "MIT" in text


def test_format_version_text_with_missing_attributes() -> None:
    metadata = SimpleNamespace()

    text = format_version_text(metadata)
    assert "unknown" in text
