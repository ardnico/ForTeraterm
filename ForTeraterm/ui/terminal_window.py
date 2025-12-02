from __future__ import annotations

import tkinter as tk
import tkinter.font as tkfont
from pathlib import Path

import customtkinter as ctk


class TerminalWindow(ctk.CTkToplevel):
    """Lightweight viewer for Tera Term .wlog files."""

    def __init__(self, master: ctk.CTk, wlog_path: Path, font: tkfont.Font | ctk.CTkFont) -> None:
        super().__init__(master)
        self.wlog_path = Path(wlog_path)
        self.title(f"Terminal: {self.wlog_path.name}")
        self.geometry("700x420")
        self.resizable(True, True)
        self.body_font = font
        self.text = tk.Text(self, state="disabled", font=self.body_font, bg="#111", fg="#e5e5e5")
        self.text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self._after_id: str | None = None
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._refresh()

    def _refresh(self) -> None:
        content = "(wlog not found)" if not self.wlog_path.exists() else self.wlog_path.read_text(encoding="utf-8")
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, content)
        self.text.configure(state="disabled")
        self._after_id = self.after(1000, self._refresh)

    def _on_close(self) -> None:
        if self._after_id:
            self.after_cancel(self._after_id)
        self.destroy()


__all__ = ["TerminalWindow"]
