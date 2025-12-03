from __future__ import annotations

import tkinter as tk
import tkinter.font as tkfont
from pathlib import Path

import customtkinter as ctk


class TerminalWindow(ctk.CTkToplevel):
    """Viewer for live terminal output or historical wlog files."""

    def __init__(
        self,
        master: ctk.CTk,
        font: tkfont.Font | ctk.CTkFont,
        *,
        wlog_path: Path | None = None,
        on_cancel=None,
        on_reconnect=None,
        live: bool = False,
    ) -> None:
        super().__init__(master)
        self.wlog_path = Path(wlog_path) if wlog_path else None
        self.title("Terminal")
        self.geometry("760x460")
        self.resizable(True, True)

        if isinstance(font, ctk.CTkFont):
            self.body_font = font
            self.tk_font = font
        else:
            actual = font.actual()
            self.body_font = ctk.CTkFont(
                family=actual.get("family"),
                size=int(actual.get("size", 0) or 12),
                weight=actual.get("weight"),
                slant=actual.get("slant"),
                underline=bool(actual.get("underline")),
                overstrike=bool(actual.get("overstrike")),
            )
            self.tk_font = font

        self.on_cancel = on_cancel
        self.on_reconnect = on_reconnect
        self.live = live
        self.text = tk.Text(self, state="disabled", font=self.tk_font, bg="#111", fg="#e5e5e5")
        self.text.pack(fill=tk.BOTH, expand=True, padx=8, pady=(8, 2))
        controls = ctk.CTkFrame(self)
        controls.pack(fill=tk.X, padx=8, pady=(0, 8))
        self.status_label = ctk.CTkLabel(controls, text="", font=self.body_font)
        self.status_label.pack(side=tk.LEFT, padx=4)
        if self.live:
            ctk.CTkButton(controls, text="Cancel", command=self._cancel, font=self.body_font).pack(side=tk.RIGHT, padx=4)
            ctk.CTkButton(controls, text="Reconnect", command=self._reconnect, font=self.body_font).pack(
                side=tk.RIGHT, padx=4
            )
        self._after_id: str | None = None
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        if self.wlog_path:
            self.load_from_file()

    def load_from_file(self) -> None:
        content = "(wlog not found)" if not self.wlog_path or not self.wlog_path.exists() else self.wlog_path.read_text(
            encoding="utf-8"
        )
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, content)
        self.text.configure(state="disabled")

    def append_line(self, line: str) -> None:
        self.text.configure(state="normal")
        self.text.insert(tk.END, f"{line}\n")
        self.text.see(tk.END)
        self.text.configure(state="disabled")

    def set_status(self, status: str) -> None:
        self.status_label.configure(text=status)

    def _cancel(self) -> None:
        if self.on_cancel:
            self.on_cancel()

    def _reconnect(self) -> None:
        if self.on_reconnect:
            self.on_reconnect()

    def _on_close(self) -> None:
        if self._after_id:
            self.after_cancel(self._after_id)
        self.destroy()


__all__ = ["TerminalWindow"]
