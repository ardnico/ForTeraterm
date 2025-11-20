"""Profile creation dialog for the launcher."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from ..credential_store import CredentialStore
from ..storage import CommandSet, DataStore, Profile
from .credential_dialog import CredentialDialog


class ProfileDialog(ctk.CTkToplevel):
    def __init__(self, master: ctk.CTk, storage: DataStore, cred_store: CredentialStore) -> None:
        super().__init__(master)
        self.title("New Profile")
        self.resizable(False, False)
        self.grab_set()
        self.storage = storage
        self.cred_store = cred_store
        self.created_profile: Profile | None = None
        self.created_command_set: CommandSet | None = None

        self._build_form()

    def _build_form(self) -> None:
        body = ctk.CTkFrame(self)
        body.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        self.name_entry = self._add_entry(body, "Profile Name", 0)
        self.host_entry = self._add_entry(body, "Host", 1)
        self.port_entry = self._add_entry(body, "Port", 2, default="22")
        self.user_entry = self._add_entry(body, "User", 3)
        self.auth_type = tk.StringVar(value="password")
        ctk.CTkLabel(body, text="Auth Type").grid(row=4, column=0, sticky=tk.W, padx=4, pady=4)
        ctk.CTkOptionMenu(body, variable=self.auth_type, values=["password", "publickey", "keyboard-interactive"]).grid(
            row=4, column=1, sticky=tk.EW, padx=4, pady=4
        )

        # Command set fields
        self.command_label_entry = self._add_entry(body, "Command Set Label", 5, default="Default Commands")
        ctk.CTkLabel(body, text="Commands (one per line)").grid(row=6, column=0, sticky=tk.W, padx=4, pady=(12, 4))
        self.command_text = tk.Text(body, height=5, width=40)
        self.command_text.grid(row=7, column=0, columnspan=2, sticky=tk.EW, padx=4, pady=4)

        # Credential fields
        ctk.CTkLabel(body, text="Credential Reference").grid(row=8, column=0, sticky=tk.W, padx=4, pady=(12, 4))
        self.cred_var = tk.StringVar(value="(none)")
        self.cred_options = ["(none)"] + self.storage.list_credential_refs()
        self.cred_menu = ctk.CTkOptionMenu(body, variable=self.cred_var, values=self.cred_options, state="normal")
        self.cred_menu.grid(row=8, column=1, sticky=tk.EW, padx=4, pady=(12, 4))
        ctk.CTkButton(body, text="New Credential", command=self._new_credential).grid(
            row=9, column=0, columnspan=2, sticky=tk.EW, padx=4, pady=4
        )

        if self.cred_store.restricted:
            self.cred_menu.configure(state="disabled")
            ctk.CTkLabel(body, text="Credential storage disabled; password will be requested at connect time.").grid(
                row=10, column=0, columnspan=2, sticky=tk.W, padx=4, pady=(4, 12)
            )
        else:
            ctk.CTkLabel(body, text="Credentials are stored securely via keyring").grid(
                row=10, column=0, columnspan=2, sticky=tk.W, padx=4, pady=(4, 12)
            )

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill=tk.X, padx=12, pady=(0, 12))
        save_btn = ctk.CTkButton(button_frame, text="Save", command=self._on_save)
        save_btn.pack(side=tk.RIGHT, padx=4)
        cancel_btn = ctk.CTkButton(button_frame, text="Cancel", command=self.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=4)

        for i in range(2):
            body.grid_columnconfigure(i, weight=1)

    def _new_credential(self) -> None:
        if self.cred_store.restricted:
            messagebox.showwarning("Restricted", "Credential storage is disabled in this environment")
            return
        dialog = CredentialDialog(self, cred_store=self.cred_store)
        self.wait_window(dialog)
        if dialog.cred_ref:
            if dialog.cred_ref not in self.cred_options:
                self.cred_options.append(dialog.cred_ref)
                self.cred_menu.configure(values=self.cred_options)
            self.cred_var.set(dialog.cred_ref)

    def _add_entry(self, frame: ctk.CTkFrame, label: str, row: int, default: str | None = None) -> ctk.CTkEntry:
        ctk.CTkLabel(frame, text=label).grid(row=row, column=0, sticky=tk.W, padx=4, pady=4)
        entry = ctk.CTkEntry(frame)
        if default is not None:
            entry.insert(0, default)
        entry.grid(row=row, column=1, sticky=tk.EW, padx=4, pady=4)
        return entry

    def _on_save(self) -> None:
        name = self.name_entry.get().strip()
        host = self.host_entry.get().strip()
        port_str = self.port_entry.get().strip()
        user = self.user_entry.get().strip()
        auth_type = self.auth_type.get()
        if not name or not host or not port_str or not user:
            messagebox.showerror("Error", "Name, host, port, and user are required")
            return
        try:
            port = int(port_str)
        except ValueError:
            messagebox.showerror("Error", "Port must be a number")
            return
        commands = [line.strip() for line in self.command_text.get("1.0", tk.END).splitlines() if line.strip()]
        if not commands:
            messagebox.showerror("Error", "At least one command is required")
            return

        cred_ref: str | None = None
        if not self.cred_store.restricted and self.cred_var.get() != "(none)":
            cred_ref = self.cred_var.get()

        command_set = CommandSet(
            id=None,
            ref_id=f"cmd:{name.lower().replace(' ', '-')}",
            label=self.command_label_entry.get().strip() or "Commands",
            description="",
            commands=commands,
        )
        command_set_id = self.storage.upsert_command_set(command_set)
        command_set.id = command_set_id

        profile = Profile(
            id=None,
            name=name,
            host=host,
            port=port,
            user=user,
            auth_type=auth_type,
            cred_ref=cred_ref,
            ttl_template_version="v1-basic",
            command_set_id=command_set_id,
        )
        profile_id = self.storage.upsert_profile(profile)
        profile.id = profile_id
        self.created_profile = profile
        self.created_command_set = command_set
        self.destroy()


__all__ = ["ProfileDialog"]
