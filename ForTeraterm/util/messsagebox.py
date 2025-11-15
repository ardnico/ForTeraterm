"""Utilities for showing user-facing message boxes.

The project bundles the third-party ``CTkMessagebox`` widget as a Git
submodule.  When the submodule is missing (for example because the repository
was cloned without ``--recursive``) importing the widget raises
``ModuleNotFoundError`` and prevents the application from launching.  The
fallback implementation below emulates the small subset of behaviour required by
the application so the program remains usable even without the optional
dependency.
"""

from __future__ import annotations

from typing import Optional

try:
    from ..CTkMessagebox.ctkmessagebox import CTkMessagebox
except ModuleNotFoundError:  # pragma: no cover - exercised when submodule missing
    import contextlib

    try:  # ``tkinter`` may be unavailable in some environments (e.g. minimal CI)
        import tkinter as tk
        from tkinter import messagebox
    except Exception:  # pragma: no cover - triggered only if tkinter is missing
        tk = None  # type: ignore[assignment]
        messagebox = None  # type: ignore[assignment]

    class CTkMessagebox:  # type: ignore[override]
        """Minimal stand-in for the optional CTkMessagebox dependency."""

        _root: Optional["tk.Tk"] = None

        def __init__(
            self,
            *,
            title: str = "Info",
            message: str = "",
            icon: Optional[str] = None,
            option_1: Optional[str] = "OK",
            option_2: Optional[str] = None,
            option_3: Optional[str] = None,
        ) -> None:
            self._response = option_1

            if tk is None or messagebox is None:
                self._fallback_to_console(title, message)
                return

            try:
                root = self._ensure_root()
                self._response = self._show_message(
                    root, title, message, icon, option_1, option_2, option_3
                )
            except tk.TclError:
                self._fallback_to_console(title, message)

        @classmethod
        def _ensure_root(cls) -> "tk.Tk":
            if cls._root is None:
                root = tk.Tk()
                root.withdraw()
                with contextlib.suppress(AttributeError):
                    root.report_callback_exception = lambda *_, **__: None
                cls._root = root
            return cls._root

        def _show_message(
            self,
            root: "tk.Tk",
            title: str,
            message: str,
            icon: Optional[str],
            option_1: Optional[str],
            option_2: Optional[str],
            option_3: Optional[str],
        ) -> Optional[str]:
            if icon == "warning" and option_2 and option_3 is None:
                retry = messagebox.askretrycancel(title, message, master=root)
                return option_2 if retry else option_1

            if icon == "question":
                result = messagebox.askyesnocancel(title, message, master=root)
                if result is True and option_3 is not None:
                    return option_3
                if result is False and option_2 is not None:
                    return option_2
                return option_1

            if icon in {"cancel", "error"}:
                messagebox.showerror(title, message, master=root)
                return option_1

            messagebox.showinfo(title, message, master=root)
            return option_1

        @staticmethod
        def _fallback_to_console(title: str, message: str) -> None:
            print(f"[{title}] {message}")

        def get(self) -> Optional[str]:
            return self._response

def show_info(title="Info", message="This is a CTkMessagebox!"):
    # Default messagebox for showing some information
    CTkMessagebox(title=title, message=message)

def show_checkmark(message="CTkMessagebox is successfully installed.",option_1="Thanks"):
    # Show some positive message with the checkmark icon
    CTkMessagebox(message=message, icon="check", option_1=option_1)
    
def show_error(title="Error", message="Something went wrong!!!"):
    # Show some error message
    CTkMessagebox(title=title, message=message, icon="cancel")
    
def show_warning(title="Warning Message!", message="Unable to connect!", option_1="Cancel", option_2="Retry"):
    # Show some retry/cancel warnings
    msg = CTkMessagebox(title=title, message=message, icon="warning", option_1=option_1, option_2=option_2)
    return msg.get()
    
def ask_question(title="Exit?", message="Do you want to close the program?", option_1="Cancel", option_2="No", option_3="Yes"):
    # get yes/no answers
    msg = CTkMessagebox(title=title, message=message, icon="question", option_1=option_1, option_2=option_2, option_3=option_3)
    return msg.get()

