"""Entry point for launching the ForTeraterm application."""

from ForTeraterm.main_menu import Mainmenu


def main() -> None:
    """Instantiate and run the main application window."""

    app = Mainmenu()
    app.run()


if __name__ == "__main__":
    main()
