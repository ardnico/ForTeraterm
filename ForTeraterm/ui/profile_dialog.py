from __future__ import annotations

"""Profile creation and editing dialog for the launcher."""

import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from ..credential_store import CredentialStore
from ..ssh_options import PortForward, build_ssh_options, parse_ssh_options
from ..storage import CommandSet, DataStore, Profile
from .credential_dialog import CredentialDialog


class ProfileDialog(ctk.CTkToplevel):
    def __init__(
        self,
        master: ctk.CTk,
        storage: DataStore,
        cred_store: CredentialStore,
        existing_profile: Profile | None = None,
        command_set: CommandSet | None = None,
    ) -> None:
        super().__init__(master)
        self.title("Edit Profile" if existing_profile else "New Profile")
        self.resizable(False, False)
        self.grab_set()
        self.storage = storage
        self.cred_store = cred_store
        self.created_profile: Profile | None = None
        self.created_command_set: CommandSet | None = None
        self.existing_profile = existing_profile
        self.command_set = command_set
        self.forward_rows: list[dict[str, ctk.CTkEntry]] = []

        self._build_form()
        if existing_profile:
            self._populate(existing_profile, command_set)

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

        ctk.CTkLabel(body, text="Port Forwardings").grid(row=5, column=0, sticky=tk.W, padx=4, pady=(12, 4))
        self.forward_frame = ctk.CTkFrame(body)
        self.forward_frame.grid(row=6, column=0, columnspan=2, sticky=tk.EW, padx=4, pady=(0, 4))
        self._add_forward_row()
        ctk.CTkButton(body, text="Add Forward", command=self._add_forward_row).grid(
            row=7, column=0, columnspan=2, sticky=tk.EW, padx=4, pady=(0, 8)
        )

        ctk.CTkLabel(body, text="Additional SSH Options").grid(row=8, column=0, sticky=tk.W, padx=4, pady=(4, 4))
        self.extra_ssh_entry = ctk.CTkEntry(body)
        self.extra_ssh_entry.grid(row=8, column=1, sticky=tk.EW, padx=4, pady=(4, 4))
        ctk.CTkLabel(body, text="(e.g. -v or other flags; /FWD entries are managed above)").grid(
            row=9, column=0, columnspan=2, sticky=tk.W, padx=4, pady=(0, 8)
        )

        self.command_label_entry = self._add_entry(body, "Command Set Label", 10, default="Default Commands")
        ctk.CTkLabel(body, text="Commands (one per line)").grid(row=11, column=0, sticky=tk.W, padx=4, pady=(12, 4))
        self.command_text = tk.Text(body, height=5, width=40)
        self.command_text.grid(row=12, column=0, columnspan=2, sticky=tk.EW, padx=4, pady=4)
        ctk.CTkLabel(body, text="(Optional) Leave blank to skip post-login commands.").grid(
            row=13, column=0, columnspan=2, sticky=tk.W, padx=4, pady=(0, 8)
        )

        ctk.CTkLabel(body, text="Credential Reference").grid(row=14, column=0, sticky=tk.W, padx=4, pady=(12, 4))
        self.cred_var = tk.StringVar(value="(none)")
        self.cred_options = ["(none)"] + self.storage.list_credential_refs()
        self.cred_menu = ctk.CTkOptionMenu(body, variable=self.cred_var, values=self.cred_options, state="normal")
        self.cred_menu.grid(row=14, column=1, sticky=tk.EW, padx=4, pady=(12, 4))
        ctk.CTkButton(body, text="New Credential", command=self._new_credential).grid(
            row=15, column=0, columnspan=2, sticky=tk.EW, padx=4, pady=4
        )

        if self.cred_store.restricted:
            self.cred_menu.configure(state="disabled")
            ctk.CTkLabel(body, text="Credential storage disabled; password will be requested at connect time.").grid(
                row=16, column=0, columnspan=2, sticky=tk.W, padx=4, pady=(4, 12)
            )
        else:
            mode_label = "keyring" if self.cred_store.mode == "standard" else "encrypted local vault"
            ctk.CTkLabel(body, text=f"Credentials stored securely via {mode_label}").grid(
                row=16, column=0, columnspan=2, sticky=tk.W, padx=4, pady=(4, 12)
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

    def _add_forward_row(self, forward: PortForward | None = None) -> None:
        row_idx = len(self.forward_rows)
        frame = ctk.CTkFrame(self.forward_frame)
        frame.grid(row=row_idx, column=0, sticky=tk.EW, pady=2)
        ctk.CTkLabel(frame, text="Local Port").grid(row=0, column=0, padx=2)
        local_entry = ctk.CTkEntry(frame, width=70)
        local_entry.grid(row=1, column=0, padx=2)
        ctk.CTkLabel(frame, text="Remote Host").grid(row=0, column=1, padx=2)
        host_entry = ctk.CTkEntry(frame, width=120)
        host_entry.grid(row=1, column=1, padx=2)
        ctk.CTkLabel(frame, text="Remote Port").grid(row=0, column=2, padx=2)
        remote_entry = ctk.CTkEntry(frame, width=70)
        remote_entry.grid(row=1, column=2, padx=2)
        remove_btn = ctk.CTkButton(frame, text="Remove", command=lambda f=frame: self._remove_forward_row(f), width=70)
        remove_btn.grid(row=1, column=3, padx=4)
        if forward:
            local_entry.insert(0, forward.local_port)
            host_entry.insert(0, forward.remote_host)
            remote_entry.insert(0, forward.remote_port)
        self.forward_rows.append({"frame": frame, "local": local_entry, "host": host_entry, "remote": remote_entry})

    def _remove_forward_row(self, frame: ctk.CTkFrame) -> None:
        for row in list(self.forward_rows):
            if row["frame"] is frame:
                row["frame"].destroy()
                self.forward_rows.remove(row)
        for idx, row in enumerate(self.forward_rows):
            row["frame"].grid(row=idx, column=0, sticky=tk.EW, pady=2)

    def _collect_forwards(self) -> list[PortForward]:
        forwards: list[PortForward] = []
        for row in self.forward_rows:
            local = row["local"].get().strip()
            host = row["host"].get().strip()
            remote = row["remote"].get().strip()
            if local or host or remote:
                forwards.append(PortForward(local_port=local, remote_host=host, remote_port=remote))
        return forwards

    def _populate(self, profile: Profile, command_set: CommandSet | None) -> None:
        self.name_entry.insert(0, profile.name)
        self.host_entry.insert(0, profile.host)
        self.port_entry.delete(0, tk.END)
        self.port_entry.insert(0, str(profile.port))
        self.user_entry.insert(0, profile.user)
        self.auth_type.set(profile.auth_type)
        forwards, extras = parse_ssh_options(profile.ssh_options)
        if forwards:
            for row in list(self.forward_rows):
                self._remove_forward_row(row["frame"])
            for forward in forwards:
                self._add_forward_row(forward)
        self.extra_ssh_entry.insert(0, extras)
        if command_set:
            self.command_label_entry.delete(0, tk.END)
            self.command_label_entry.insert(0, command_set.label)
            self.command_text.insert("1.0", "\n".join(command_set.commands))
            self.command_set = command_set
        if profile.cred_ref:
            if profile.cred_ref not in self.cred_options:
                self.cred_options.append(profile.cred_ref)
                self.cred_menu.configure(values=self.cred_options)
            self.cred_var.set(profile.cred_ref)

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

        cred_ref: str | None = None
        if not self.cred_store.restricted and self.cred_var.get() != "(none)":
            cred_ref = self.cred_var.get()

        forwards = self._collect_forwards()
        extras = self.extra_ssh_entry.get().strip()
        ssh_options = build_ssh_options(forwards, extras)

        cmd_ref = self.command_set.ref_id if self.command_set else f"cmd:{name.lower().replace(' ', '-')}"

        command_set = CommandSet(
            id=self.command_set.id if self.command_set else None,
            ref_id=cmd_ref,
            label=self.command_label_entry.get().strip() or "Commands",
            description="",
            commands=commands,
        )
        command_set_id = self.storage.upsert_command_set(command_set)
        command_set.id = command_set_id

        profile = Profile(
            id=self.existing_profile.id if self.existing_profile else None,
            name=name,
            host=host,
            port=port,
            user=user,
            auth_type=auth_type,
            cred_ref=cred_ref,
            ssh_options=ssh_options,
            ttl_template_version="v1-basic",
            command_set_id=command_set_id,
        )
        profile_id = self.storage.upsert_profile(profile)
        profile.id = profile_id
        self.created_profile = profile
        self.created_command_set = command_set
        self.destroy()


__all__ = ["ProfileDialog"]
