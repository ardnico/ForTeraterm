"""Main application window for the ForTeraterm toolkit."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, List, Optional, Sequence, Tuple
from os import fspath
import webbrowser

import customtkinter
from tkinter import filedialog

from .CTkMenuBar import CTkMenuBar, CustomDropdownMenu
from .Language.apptext import AppText
from .WindowAction.editmacro import EditMacro
from .WindowAction.serveraccess import ServerAccess
from .WindowAction.serverregist import ServerRegist
from .WindowSettings.conf import appconf
from .WindowSettings.edit import Edit
from .WindowSettings.theme import ThemeFrame1, ThemeManager
from .util import messsagebox

FrameFactory = Callable[[customtkinter.CTkFrame], customtkinter.CTkFrame]


class Mainmenu(customtkinter.CTk):
    """Main application window.

    The original implementation mixed window construction and main-loop
    management.  This refactored version separates responsibilities to make the
    class easier to reason about and extend.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.apptxt = AppText(appconf.get_data("lang"))
        self._theme = ThemeManager()
        self._content_frame: ThemeFrame1 | None = None
        self._current_frame: customtkinter.CTkFrame | None = None

        self._configure_window()
        self._build_menu_bar()
        self._build_content_frame()

        # Show the default view.
        self.action_serveraccess()

    def run(self) -> None:
        """Start the Tk main loop."""

        self.mainloop()

    def _configure_window(self) -> None:
        """Configure geometry, title and theme information."""

        width = appconf.get_data("width")
        height = appconf.get_data("height")
        self.geometry(f"{width}x{height}")
        self.title(self.apptxt.translate("TeratermAccessTool"))

        customtkinter.set_appearance_mode(self._theme.mode)

    def _build_menu_bar(self) -> None:
        """Construct the top-level menu bar and configure dropdowns."""

        menu_bar = CTkMenuBar(self)

        action_button = menu_bar.add_cascade(self.apptxt.translate("Action"))
        settings_button = menu_bar.add_cascade(self.apptxt.translate("Settings"))
        about_button = menu_bar.add_cascade(self.apptxt.translate("About"))

        self._create_dropdown(
            action_button,
            (
                ("ServerAccess", self.action_serveraccess),
                ("EditMacro", self.action_editmacro),
                ("ServerRegist", self.action_serverregist),
            ),
        )

        self._create_dropdown(
            settings_button,
            (
                ("Edit", self.settings_edit),
            ),
        )

        about_options: Tuple[tuple[str, Callable[[], None]], ...] = (
            ("Readme", self.about_readme),
            ("Version", self.about_version),
        )

        if appconf.get_data("dev_mode") == 1:
            about_options += (("Test", self.test),)

        self._create_dropdown(about_button, about_options)

    def _build_content_frame(self) -> None:
        """Create the frame that hosts the different feature panels."""

        width = appconf.get_data("width")
        height = appconf.get_data("height")
        self._content_frame = ThemeFrame1(
            master=self,
            fg_color=self._theme.back1,
            width=width,
            height=height,
        )
        self._content_frame.pack(fill="both", expand=True)

    def _create_dropdown(
        self,
        widget: customtkinter.CTkButton,
        options: Sequence[tuple[str, Callable[[], None]]],
    ) -> CustomDropdownMenu:
        """Create a drop-down menu attached to *widget* with translated labels."""

        dropdown = CustomDropdownMenu(
            widget=widget,
            border_color=self._theme.back2,
            font=self._theme.setfont,
            bg_color="transparent",
            hover_color=[self._theme.back1, self._theme.highlight],
        )

        for label_key, command in options:
            dropdown.add_option(
                option=self.apptxt.translate(label_key),
                command=command,
            )

        return dropdown

    def _show_frame(self, factory: FrameFactory) -> None:
        """Display a new frame returned by *factory* in the content area."""

        if self._content_frame is None:
            raise RuntimeError("Content frame has not been initialised.")

        self.reset_frame()
        frame = factory(self._content_frame)
        self._current_frame = frame

    @appconf.log_exception
    def action_serveraccess(self) -> None:
        self._show_frame(ServerAccess)

    @appconf.log_exception
    def action_editmacro(self) -> None:
        self._show_frame(EditMacro)

    @appconf.log_exception
    def action_serverregist(self) -> None:
        self._show_frame(ServerRegist)

    @appconf.log_exception
    def settings_edit(self) -> None:
        self._show_frame(Edit)

    def reset_frame(self) -> None:
        """Clear existing frames from the content area."""

        if self._current_frame is not None:
            self._current_frame.destroy()
            self._current_frame = None

    @appconf.log_exception
    def about_readme(self) -> None:
        readme_path = Path(__file__).resolve().parent.parent / "README.pdf"
        if readme_path.exists():
            webbrowser.open(readme_path.as_uri())
        else:
            messsagebox.show_warning(
                title="Missing documentation",
                message=f"README file not found at {readme_path}",
            )

    @appconf.log_exception
    def about_version(self) -> None:
        version_txt = (
            f"AppName:    {appconf.__name__}\n"
            f"Version:    {appconf.__version__}\n"
            f"License:    {appconf.__license__}"
        )
        messsagebox.show_info(
            title="Version Information",
            message=version_txt,
        )

    @appconf.log_exception
    def restart(self) -> None:
        self.destroy()

    @appconf.log_exception
    def test(self) -> None:
        messsagebox.show_info(
            title="Development Mode",
            message="Test action is not implemented.",
        )

    @staticmethod
    def open_file_dialog(
        filetypes: Sequence[tuple[str, str]] | None,
        initialdir: str | Path | None,
    ) -> Optional[str]:
        """Open a file selection dialog.

        Args:
            filetypes: File type filters passed directly to
                :func:`tkinter.filedialog.askopenfilename`.
            initialdir: Starting directory for the dialog.  Accepts ``str`` or
                :class:`pathlib.Path` objects as well as ``None``; any
                :class:`pathlib.Path` values are converted to strings before
                invoking the dialog.

        Returns:
            The selected file path or ``None`` if the dialog is cancelled.
        """

        if initialdir is not None:
            initialdir = fspath(initialdir)
        file_path = filedialog.askopenfilename(
            filetypes=filetypes,
            initialdir=initialdir,
        )
        return file_path or None
