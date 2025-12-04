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
        self.search_var = tk.StringVar()
        self.teraterm_var = tk.StringVar(value=current.teraterm_path)
        self.use_stub_var = tk.BooleanVar(value=current.use_stub)
        self._settings_rows: list[tuple[ctk.CTkLabel, tk.Widget, str]] = []

        self._build_form()

    def _build_form(self) -> None:
        body = ctk.CTkFrame(self)
        body.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        search_frame = ctk.CTkFrame(body)
        search_frame.grid(row=0, column=0, columnspan=2, sticky=tk.EW, padx=4, pady=(0, 8))
        ctk.CTkLabel(search_frame, text="Search", font=self.preview_font).pack(side=tk.LEFT, padx=4)
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, font=self.preview_font)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
        search_entry.bind("<KeyRelease>", lambda _event: self._filter_settings())

        self.appearance_var = tk.StringVar(value=self.current.appearance_mode)
        appearance_menu = ctk.CTkOptionMenu(body, variable=self.appearance_var, values=self.appearance_modes, font=self.preview_font)
        self._add_row(body, 1, "Appearance", appearance_menu, keywords="appearance theme mode")

        self.theme_var = tk.StringVar(value=self.current.color_theme)
        theme_menu = ctk.CTkOptionMenu(body, variable=self.theme_var, values=self.color_themes, font=self.preview_font)
        self._add_row(body, 2, "Color Theme", theme_menu, keywords="theme color")

        self.font_family_var = tk.StringVar(value=self.current.font_family)
        font_menu = ctk.CTkOptionMenu(body, variable=self.font_family_var, values=self.font_families, font=self.preview_font)
        self._add_row(body, 3, "Font Family", font_menu, keywords="font family typeface")

        self.font_size_var = tk.StringVar(value=str(self.current.font_size))
        self.font_size_entry = ctk.CTkEntry(body, textvariable=self.font_size_var, width=120, font=self.preview_font)
        self._add_row(body, 4, "Font Size", self.font_size_entry, keywords="font size")

        teraterm_entry = ctk.CTkEntry(body, textvariable=self.teraterm_var, font=self.preview_font)
        self._add_row(body, 5, "Tera Term Path", teraterm_entry, keywords="teraterm path executable client")

        stub_checkbox = ctk.CTkCheckBox(body, text="Use stub mode (no real Tera Term)", variable=self.use_stub_var, font=self.preview_font)
        self._add_row(body, 6, "Stub Mode", stub_checkbox, keywords="stub simulate")

        self._filter_settings()

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill=tk.X, padx=12, pady=(0, 12))
        ctk.CTkButton(button_frame, text="Save", command=self._on_save, font=self.preview_font).pack(side=tk.RIGHT, padx=4)
        ctk.CTkButton(button_frame, text="Cancel", command=self.destroy, font=self.preview_font).pack(side=tk.RIGHT, padx=4)

        for i in range(2):
            body.grid_columnconfigure(i, weight=1)

    def _add_row(
        self,
        frame: ctk.CTkFrame,
        row: int,
        label: str,
        widget: tk.Widget,
        *,
        keywords: str,
    ) -> None:
        lbl = ctk.CTkLabel(frame, text=label, font=self.preview_font)
        lbl.grid(row=row, column=0, sticky=tk.W, padx=4, pady=4)
        widget.grid(row=row, column=1, sticky=tk.EW, padx=4, pady=4)
        self._settings_rows.append((lbl, widget, keywords.lower()))

    def _filter_settings(self) -> None:
        term = (self.search_var.get() or "").lower()
        for label, widget, keywords in self._settings_rows:
            match = not term or term in keywords or term in label.cget("text").lower()
            if match:
                label.grid()
                widget.grid()
            else:
                label.grid_remove()
                widget.grid_remove()

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
            teraterm_path=self.teraterm_var.get().strip(),
            use_stub=bool(self.use_stub_var.get()),
        )
        self.destroy()


__all__ = ["SettingsDialog"]
