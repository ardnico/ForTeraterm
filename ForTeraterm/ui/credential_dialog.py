"""Dialog for registering or updating credentials via keyring."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from ..credential_store import CredentialStore


class CredentialDialog(ctk.CTkToplevel):
    def __init__(self, master: ctk.CTk, cred_store: CredentialStore) -> None:
        super().__init__(master)
        self.title("New Credential")
        self.resizable(False, False)
        self.grab_set()
        self.cred_store = cred_store
        self.cred_ref: str | None = None
        self._build_form()

    def _build_form(self) -> None:
        body = ctk.CTkFrame(self)
        body.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        ctk.CTkLabel(body, text="Label").grid(row=0, column=0, sticky=tk.W, padx=4, pady=4)
        self.label_entry = ctk.CTkEntry(body)
        self.label_entry.grid(row=0, column=1, sticky=tk.EW, padx=4, pady=4)

        ctk.CTkLabel(body, text="Username (optional)").grid(row=1, column=0, sticky=tk.W, padx=4, pady=4)
        self.user_entry = ctk.CTkEntry(body)
        self.user_entry.grid(row=1, column=1, sticky=tk.EW, padx=4, pady=4)

        ctk.CTkLabel(body, text="Password / Passphrase").grid(row=2, column=0, sticky=tk.W, padx=4, pady=4)
        self.secret_entry = ctk.CTkEntry(body, show="*")
        self.secret_entry.grid(row=2, column=1, sticky=tk.EW, padx=4, pady=4)

        note = "Credentials are stored via OS keyring" if not self.cred_store.restricted else "Credential storage unavailable"
        ctk.CTkLabel(body, text=note).grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=4, pady=(4, 12))

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill=tk.X, padx=12, pady=(0, 12))
        ctk.CTkButton(button_frame, text="Save", command=self._on_save).pack(side=tk.RIGHT, padx=4)
        ctk.CTkButton(button_frame, text="Cancel", command=self.destroy).pack(side=tk.RIGHT, padx=4)

        body.grid_columnconfigure(1, weight=1)

    def _on_save(self) -> None:
        label = self.label_entry.get().strip()
        secret = self.secret_entry.get().strip()
        username = self.user_entry.get().strip() or None
        if not label or not secret:
            messagebox.showerror("Error", "Label and secret are required")
            return
        try:
            self.cred_ref = self.cred_store.register(label, username, secret)
        except Exception as exc:  # pragma: no cover - UI surface
            messagebox.showerror("Error", str(exc))
            return
        self.destroy()


__all__ = ["CredentialDialog"]
