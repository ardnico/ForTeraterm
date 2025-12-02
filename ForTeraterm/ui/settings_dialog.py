"""Dialog for adjusting launcher appearance and font settings."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from ..storage import AppSettings


class SettingsDialog(ctk.CTkToplevel):
    def __init__(
        self,
        master: ctk.CTk,
        current: AppSettings,
        appearance_modes: list[str],
        color_themes: list[str],
        font_families: list[str],
    ) -> None:
        super().__init__(master)
        self.title("Settings")
        self.resizable(False, False)
        self.grab_set()
        self.result: AppSettings | None = None
        self.current = current
        self.appearance_modes = appearance_modes
        self.color_themes = color_themes
        self.font_families = font_families
        self.preview_font = ctk.CTkFont(family=current.font_family, size=current.font_size)

        self._build_form()

    def _build_form(self) -> None:
        body = ctk.CTkFrame(self)
        body.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        ctk.CTkLabel(body, text="Appearance", font=self.preview_font).grid(row=0, column=0, sticky=tk.W, padx=4, pady=4)
        self.appearance_var = tk.StringVar(value=self.current.appearance_mode)
        ctk.CTkOptionMenu(body, variable=self.appearance_var, values=self.appearance_modes, font=self.preview_font).grid(
            row=0, column=1, sticky=tk.EW, padx=4, pady=4
        )

        ctk.CTkLabel(body, text="Color Theme", font=self.preview_font).grid(row=1, column=0, sticky=tk.W, padx=4, pady=4)
        self.theme_var = tk.StringVar(value=self.current.color_theme)
        ctk.CTkOptionMenu(body, variable=self.theme_var, values=self.color_themes, font=self.preview_font).grid(
            row=1, column=1, sticky=tk.EW, padx=4, pady=4
        )

        ctk.CTkLabel(body, text="Font Family", font=self.preview_font).grid(row=2, column=0, sticky=tk.W, padx=4, pady=4)
        self.font_family_var = tk.StringVar(value=self.current.font_family)
        ctk.CTkOptionMenu(body, variable=self.font_family_var, values=self.font_families, font=self.preview_font).grid(
            row=2, column=1, sticky=tk.EW, padx=4, pady=4
        )

        ctk.CTkLabel(body, text="Font Size", font=self.preview_font).grid(row=3, column=0, sticky=tk.W, padx=4, pady=4)
        self.font_size_var = tk.StringVar(value=str(self.current.font_size))
        self.font_size_entry = ctk.CTkEntry(body, textvariable=self.font_size_var, width=80, font=self.preview_font)
        self.font_size_entry.grid(row=3, column=1, sticky=tk.EW, padx=4, pady=4)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill=tk.X, padx=12, pady=(0, 12))
        ctk.CTkButton(button_frame, text="Save", command=self._on_save, font=self.preview_font).pack(side=tk.RIGHT, padx=4)
        ctk.CTkButton(button_frame, text="Cancel", command=self.destroy, font=self.preview_font).pack(side=tk.RIGHT, padx=4)

        for i in range(2):
            body.grid_columnconfigure(i, weight=1)

    def _on_save(self) -> None:
        size_text = self.font_size_var.get().strip()
        try:
            size = int(size_text)
        except ValueError:
            messagebox.showerror("Invalid size", "Font size must be a number")
            return
        if size <= 6:
            messagebox.showerror("Invalid size", "Font size must be greater than 6")
            return

        self.result = AppSettings(
            appearance_mode=self.appearance_var.get(),
            color_theme=self.theme_var.get(),
            font_family=self.font_family_var.get(),
            font_size=size,
        )
        self.destroy()


__all__ = ["SettingsDialog"]
