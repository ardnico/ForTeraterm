from __future__ import annotations

from pathlib import Path
import sys
import types

import pytest


if "customtkinter" not in sys.modules:
    class _DummyCustomTkModule(types.ModuleType):
        def __getattr__(self, name: str):  # pragma: no cover - fallback for unneeded attributes
            dummy_type = type(name, (), {"__init__": lambda self, *args, **kwargs: None})
            setattr(self, name, dummy_type)
            return dummy_type

    mock_customtkinter = _DummyCustomTkModule("customtkinter")

    def _dummy_set_appearance_mode(*args, **kwargs) -> None:  # pragma: no cover - trivial stub
        pass

    mock_customtkinter.set_appearance_mode = _dummy_set_appearance_mode
    sys.modules["customtkinter"] = mock_customtkinter


if "ForTeraterm.CTkMessagebox" not in sys.modules:
    messagebox_pkg = types.ModuleType("ForTeraterm.CTkMessagebox")
    sys.modules["ForTeraterm.CTkMessagebox"] = messagebox_pkg

    messagebox_mod = types.ModuleType("ForTeraterm.CTkMessagebox.ctkmessagebox")

    class _DummyCTkMessagebox:
        def __init__(self, *args, **kwargs):
            pass

    messagebox_mod.CTkMessagebox = _DummyCTkMessagebox
    sys.modules["ForTeraterm.CTkMessagebox.ctkmessagebox"] = messagebox_mod
    messagebox_pkg.ctkmessagebox = messagebox_mod


if "PIL" not in sys.modules:
    pil_pkg = types.ModuleType("PIL")
    sys.modules["PIL"] = pil_pkg

    pil_image = types.ModuleType("PIL.Image")

    pil_image.open = lambda *args, **kwargs: RuntimeError("Image.open stub should not be called during tests")
    sys.modules["PIL.Image"] = pil_image
    pil_pkg.Image = pil_image


stub_image_module = types.ModuleType("ForTeraterm.WindowSettings.image")


class _DummyImgInst:
    def __getattr__(self, name):  # pragma: no cover - fallback for unused attributes
        return None


stub_image_module.imginst = _DummyImgInst()
sys.modules["ForTeraterm.WindowSettings.image"] = stub_image_module


if "pyautogui" not in sys.modules:
    sys.modules["pyautogui"] = types.ModuleType("pyautogui")


from ForTeraterm.main_menu import Mainmenu


@pytest.fixture
def fake_askopenfilename(monkeypatch):
    """Capture calls to ``filedialog.askopenfilename`` for assertions."""

    calls: list[dict[str, object]] = []

    def stub(*, filetypes, initialdir):
        calls.append({"filetypes": filetypes, "initialdir": initialdir})
        return "selected-file"

    monkeypatch.setattr("ForTeraterm.main_menu.filedialog.askopenfilename", stub)
    return calls


def test_open_file_dialog_accepts_str_initialdir(fake_askopenfilename):
    filetypes = [("All", "*.*")]
    result = Mainmenu.open_file_dialog(filetypes, "C:/tmp")

    assert result == "selected-file"
    (call,) = fake_askopenfilename
    assert call["filetypes"] is filetypes
    assert call["initialdir"] == "C:/tmp"


def test_open_file_dialog_accepts_path_initialdir(fake_askopenfilename):
    filetypes = [("All", "*.*")]
    initialdir = Path("/path/dir")

    Mainmenu.open_file_dialog(filetypes, initialdir)

    (call,) = fake_askopenfilename
    assert call["initialdir"] == str(initialdir)


def test_open_file_dialog_accepts_none_initialdir(monkeypatch):
    def stub(*, filetypes, initialdir):
        assert initialdir is None
        return ""

    monkeypatch.setattr("ForTeraterm.main_menu.filedialog.askopenfilename", stub)

    result = Mainmenu.open_file_dialog([("All", "*.*")], None)

    assert result is None
