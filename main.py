"""Entry point for launching the new TeraTerm Connection Launcher v3."""

from __future__ import annotations

from pathlib import Path

from ForTeraterm.ui.main_window import MainWindow


def main() -> None:
    app_dir = Path.home() / ".for_teraterm"
    app_dir.mkdir(exist_ok=True)
    db_path = app_dir / "launcher.db"
    template_root = Path(__file__).parent / "templates"
    app = MainWindow(db_path=db_path, template_root=template_root)
    app.mainloop()


if __name__ == "__main__":
    main()
