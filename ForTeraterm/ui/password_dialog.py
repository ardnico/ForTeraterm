"""Simple password prompt dialog used in restricted mode or lookup failures."""

from __future__ import annotations

import tkinter as tk
import customtkinter as ctk


class PasswordDialog(ctk.CTkToplevel):
    def __init__(self, master: ctk.CTk, title: str = "Enter password") -> None:
        super().__init__(master)
        self.title(title)
        self.resizable(False, False)
        self.grab_set()
        self.password: str | None = None

        self.label = ctk.CTkLabel(self, text=title)
        self.label.pack(padx=12, pady=(12, 6))
        self.entry = ctk.CTkEntry(self, show="*")
        self.entry.pack(padx=12, pady=6)
        self.entry.focus_set()

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill=tk.X, padx=12, pady=(6, 12))
        ok_btn = ctk.CTkButton(btn_frame, text="OK", command=self._on_ok)
        ok_btn.pack(side=tk.LEFT, expand=True, padx=4)
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=self._on_cancel)
        cancel_btn.pack(side=tk.RIGHT, expand=True, padx=4)

        self.bind("<Return>", lambda event: self._on_ok())
        self.bind("<Escape>", lambda event: self._on_cancel())

    def _on_ok(self) -> None:
        self.password = self.entry.get()
        self.destroy()

    def _on_cancel(self) -> None:
        self.password = None
        self.destroy()


__all__ = ["PasswordDialog"]
