from __future__ import annotations

import sys
import types
from typing import Callable

customtkinter_stub = types.ModuleType("customtkinter")


class _CTk:
    def __init__(self, *args, **kwargs) -> None:  # pragma: no cover - stub
        _ = (args, kwargs)


class _CTkFrame:
    def __init__(self, *args, **kwargs) -> None:  # pragma: no cover - stub
        _ = (args, kwargs)

    def destroy(self) -> None:  # pragma: no cover - stub
        pass


class _CTkButton(_CTkFrame):
    def __init__(self, *args, **kwargs) -> None:  # pragma: no cover - stub
        super().__init__(*args, **kwargs)


def _set_appearance_mode(mode: str) -> None:  # pragma: no cover - stub
    _ = mode


customtkinter_stub.CTk = _CTk
customtkinter_stub.CTkFrame = _CTkFrame
customtkinter_stub.CTkButton = _CTkButton
customtkinter_stub.set_appearance_mode = _set_appearance_mode

sys.modules.setdefault("customtkinter", customtkinter_stub)


ctk_menu_bar_stub = types.ModuleType("ForTeraterm.CTkMenuBar")


class _CascadeButton:
    def __init__(self) -> None:
        self.label: str | None = None


class _CTkMenuBar:
    def __init__(self, master) -> None:  # pragma: no cover - stub
        self.master = master

    def add_cascade(self, label: str) -> _CascadeButton:  # pragma: no cover - stub
        button = _CascadeButton()
        button.label = label
        return button


class _CustomDropdownMenu:
    def __init__(self, widget, **kwargs) -> None:  # pragma: no cover - stub
        self.widget = widget
        self.options: list[tuple[str, Callable[[], None]]] = []
        _ = kwargs

    def add_option(self, option: str, command: Callable[[], None]) -> None:  # pragma: no cover - stub
        self.options.append((option, command))


ctk_menu_bar_stub.CTkMenuBar = _CTkMenuBar
ctk_menu_bar_stub.CustomDropdownMenu = _CustomDropdownMenu

sys.modules.setdefault("ForTeraterm.CTkMenuBar", ctk_menu_bar_stub)


language_stub = types.ModuleType("ForTeraterm.Language.apptext")


class _AppText:
    def __init__(self, lang: str) -> None:  # pragma: no cover - stub
        self.lang = lang

    def translate(self, key: str) -> str:  # pragma: no cover - stub
        return key


language_stub.AppText = _AppText
sys.modules.setdefault("ForTeraterm.Language.apptext", language_stub)


window_theme_stub = types.ModuleType("ForTeraterm.WindowSettings.theme")


class _ThemeFrame1(_CTkFrame):
    pass


class _ThemeManager:
    def __init__(self) -> None:  # pragma: no cover - stub
        self.mode = "Light"
        self.back1 = "#fff"
        self.back2 = "#000"
        self.setfont = ("Arial", 12)
        self.highlight = "#f00"


window_theme_stub.ThemeFrame1 = _ThemeFrame1
window_theme_stub.ThemeManager = _ThemeManager
sys.modules.setdefault("ForTeraterm.WindowSettings.theme", window_theme_stub)


window_conf_stub = types.ModuleType("ForTeraterm.WindowSettings.conf")


class _AppConf:
    __name__ = "appconf"
    __version__ = "0"
    __license__ = "MIT"

    def get_data(self, key: str) -> int | str:
        defaults: dict[str, int | str] = {
            "lang": "en",
            "width": 800,
            "height": 600,
            "dev_mode": 0,
        }
        return defaults[key]

    def log_exception(self, func: Callable) -> Callable:
        return func


window_conf_stub.appconf = _AppConf()
sys.modules.setdefault("ForTeraterm.WindowSettings.conf", window_conf_stub)


window_edit_stub = types.ModuleType("ForTeraterm.WindowSettings.edit")


class _Edit(_ThemeFrame1):
    def __init__(self, master) -> None:  # pragma: no cover - stub
        super().__init__(master)


window_edit_stub.Edit = _Edit
sys.modules.setdefault("ForTeraterm.WindowSettings.edit", window_edit_stub)


window_action_stub = types.ModuleType("ForTeraterm.WindowAction.serveraccess")


class _ServerAccess(_ThemeFrame1):
    def __init__(self, master) -> None:  # pragma: no cover - stub
        super().__init__(master)


window_action_stub.ServerAccess = _ServerAccess
sys.modules.setdefault("ForTeraterm.WindowAction.serveraccess", window_action_stub)


server_regist_stub = types.ModuleType("ForTeraterm.WindowAction.serverregist")


class _ServerRegist(_ThemeFrame1):
    def __init__(self, master) -> None:  # pragma: no cover - stub
        super().__init__(master)


server_regist_stub.ServerRegist = _ServerRegist
sys.modules.setdefault("ForTeraterm.WindowAction.serverregist", server_regist_stub)


edit_macro_stub = types.ModuleType("ForTeraterm.WindowAction.editmacro")


class _EditMacro(_ThemeFrame1):
    def __init__(self, master) -> None:  # pragma: no cover - stub
        super().__init__(master)


edit_macro_stub.EditMacro = _EditMacro
sys.modules.setdefault("ForTeraterm.WindowAction.editmacro", edit_macro_stub)


messsagebox_stub = types.ModuleType("ForTeraterm.util.messsagebox")


def _show_info(*args, **kwargs) -> None:  # pragma: no cover - stub
    _ = (args, kwargs)


def _show_warning(*args, **kwargs) -> None:  # pragma: no cover - stub
    _ = (args, kwargs)


messsagebox_stub.show_info = _show_info
messsagebox_stub.show_warning = _show_warning
sys.modules.setdefault("ForTeraterm.util.messsagebox", messsagebox_stub)


from ForTeraterm.main_menu import Mainmenu


class DummyFrame:
    def __init__(self) -> None:
        self.destroy_calls = 0

    def destroy(self) -> None:
        self.destroy_calls += 1


def test_reset_frame_destroys_current_frame_once() -> None:
    menu = Mainmenu.__new__(Mainmenu)
    dummy = DummyFrame()
    menu._current_frame = dummy  # type: ignore[attr-defined]

    Mainmenu.reset_frame(menu)
    assert menu._current_frame is None  # type: ignore[attr-defined]
    assert dummy.destroy_calls == 1

    Mainmenu.reset_frame(menu)
    assert dummy.destroy_calls == 1
