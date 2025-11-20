"""Main application window for the launcher."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from pathlib import Path

import customtkinter as ctk

from ..credential_store import CredentialStore
from ..launcher import Launcher
from ..storage import CommandSet, DataStore, Profile
from ..ttl_renderer import TTLRenderer
from .password_dialog import PasswordDialog
from .profile_dialog import ProfileDialog


class MainWindow(ctk.CTk):
    def __init__(self, db_path: Path, template_root: Path) -> None:
        super().__init__()
        self.title("TeraTerm Connection Launcher v3")
        self.geometry("820x520")
        self.storage = DataStore(db_path)
        self.cred_store = CredentialStore()
        self.renderer = TTLRenderer(template_root)
        self.launcher = Launcher(self.renderer, self.storage, stub_mode=True)
        self.selected_profile: Profile | None = None
        self.command_set_cache: dict[int, CommandSet] = {}
        self.history_records = []

        self._build_ui()
        self._load_profiles()

    def _build_ui(self) -> None:
        self.status_bar = ctk.CTkLabel(self, text=self._status_text())
        self.status_bar.pack(fill=tk.X, pady=(8, 4), padx=8)

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Profile list
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        ctk.CTkLabel(left_frame, text="Profiles").pack(anchor=tk.W, padx=6, pady=4)
        self.profile_list = tk.Listbox(left_frame, exportselection=False)
        self.profile_list.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        self.profile_list.bind("<<ListboxSelect>>", lambda event: self._on_select())

        btn_frame = ctk.CTkFrame(left_frame)
        btn_frame.pack(fill=tk.X, padx=6, pady=(0, 6))
        ctk.CTkButton(btn_frame, text="New Profile", command=self._new_profile).pack(side=tk.LEFT, padx=4)
        ctk.CTkButton(btn_frame, text="Connect", command=self._connect).pack(side=tk.RIGHT, padx=4)

        # History
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        ctk.CTkLabel(right_frame, text="Recent History").pack(anchor=tk.W, padx=6, pady=4)
        filter_frame = ctk.CTkFrame(right_frame)
        filter_frame.pack(fill=tk.X, padx=6, pady=(0, 6))
        ctk.CTkLabel(filter_frame, text="Result").pack(side=tk.LEFT, padx=4)
        self.result_filter = tk.StringVar(value="all")
        ctk.CTkOptionMenu(filter_frame, variable=self.result_filter, values=["all", "success", "failed", "unknown"], command=lambda _=None: self._load_history()).pack(side=tk.LEFT, padx=4)
        ctk.CTkLabel(filter_frame, text="Command Set").pack(side=tk.LEFT, padx=4)
        self.command_filter = tk.StringVar(value="all")
        self.command_menu = ctk.CTkOptionMenu(filter_frame, variable=self.command_filter, values=["all"], command=lambda _=None: self._load_history())
        self.command_menu.pack(side=tk.LEFT, padx=4)

        self.history_list = tk.Listbox(right_frame, exportselection=False)
        self.history_list.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        self.history_list.bind("<Double-Button-1>", lambda event: self._relaunch_history())

    def _status_text(self) -> str:
        if self.cred_store.restricted:
            return "Credential Storage: Disabled (restricted mode)"
        return "Credential Storage: Enabled (Windows Credential Manager / keyring)"

    def _load_profiles(self) -> None:
        self.profile_list.delete(0, tk.END)
        for profile in self.storage.list_profiles():
            display = f"{profile.name} ({profile.user}@{profile.host}:{profile.port})"
            self.profile_list.insert(tk.END, display)
        if self.storage.list_profiles():
            self.profile_list.selection_set(0)
            self._on_select()

    def _get_selected_profile(self) -> Profile | None:
        selection = self.profile_list.curselection()
        if not selection:
            return None
        index = selection[0]
        profiles = self.storage.list_profiles()
        if index >= len(profiles):
            return None
        return profiles[index]

    def _on_select(self) -> None:
        profile = self._get_selected_profile()
        self.selected_profile = profile
        self._update_command_filter()
        self._load_history()

    def _new_profile(self) -> None:
        dialog = ProfileDialog(self, storage=self.storage, cred_store=self.cred_store)
        self.wait_window(dialog)
        if dialog.created_profile:
            self._load_profiles()

    def _get_command_set(self, command_set_id: int) -> CommandSet:
        if command_set_id not in self.command_set_cache:
            self.command_set_cache[command_set_id] = self.storage.get_command_set(command_set_id)
        return self.command_set_cache[command_set_id]

    def _update_command_filter(self) -> None:
        if not self.selected_profile:
            self.command_menu.configure(values=["all"])
            self.command_filter.set("all")
            return
        cs = self._get_command_set(self.selected_profile.command_set_id)
        values = ["all", cs.label]
        self.command_menu.configure(values=values)
        self.command_filter.set("all")

    def _connect(self) -> None:
        profile = self._get_selected_profile()
        if profile is None:
            messagebox.showwarning("No profile", "Select a profile first")
            return
        command_set = self._get_command_set(profile.command_set_id)
        credential = None
        password_fallback = None
        if profile.cred_ref and not self.cred_store.restricted:
            credential = self.cred_store.get(profile.cred_ref)
            if credential is None:
                if not messagebox.askyesno(
                    "Credential missing",
                    "Stored credential not found. Do you want to enter a one-time password?",
                ):
                    return
        if credential is None:
            dialog = PasswordDialog(self, title="Enter password for this session")
            self.wait_window(dialog)
            password_fallback = dialog.password
            if password_fallback is None:
                return
        try:
            result = self.launcher.launch(profile, command_set, credential, password_fallback)
        except Exception as exc:
            messagebox.showerror("Launch failed", str(exc))
            return
        if result.result == "success":
            messagebox.showinfo("Success", "Connection flow completed (stub mode)")
        else:
            messagebox.showwarning("Failed", f"Connection failed: {result.error_code}")
        self._load_history()

    def _relaunch_history(self) -> None:
        if not self.history_records:
            return
        selection = self.history_list.curselection()
        if not selection:
            return
        record = self.history_records[selection[0]]
        profile = self._get_selected_profile()
        if profile is None:
            return
        try:
            command_set = self._get_command_set(record.command_set_id or profile.command_set_id)
        except Exception:
            messagebox.showerror("Error", "Command set missing for this history entry")
            return
        credential = None
        password_fallback = None
        if profile.cred_ref and not self.cred_store.restricted:
            credential = self.cred_store.get(profile.cred_ref)
        if credential is None:
            dialog = PasswordDialog(self, title="Enter password for this session")
            self.wait_window(dialog)
            password_fallback = dialog.password
            if password_fallback is None:
                return
        try:
            result = self.launcher.launch(profile, command_set, credential, password_fallback)
        except Exception as exc:
            messagebox.showerror("Launch failed", str(exc))
            return
        if result.result == "success":
            messagebox.showinfo("Success", "Re-run completed (stub mode)")
        else:
            messagebox.showwarning("Failed", f"Connection failed: {result.error_code}")
        self._load_history()

    def _load_history(self) -> None:
        self.history_list.delete(0, tk.END)
        self.history_records = []
        if not self.selected_profile:
            return
        cs_filter = None
        if self.command_filter.get() != "all":
            cs_filter = self.selected_profile.command_set_id
        history = self.storage.list_history_for_profile(
            self.selected_profile.id or 0,
            limit=50,
            result_filter=self.result_filter.get(),
            command_set_id=cs_filter,
        )
        self.history_records = history
        for record in history:
            summary = f"{record.connected_at} | {record.result}"
            if record.error_code:
                summary += f" ({record.error_code})"
            if record.command_set_id:
                try:
                    cs = self._get_command_set(record.command_set_id)
                    summary += f" | {cs.label}"
                except Exception:
                    summary += " | unknown commands"
            self.history_list.insert(tk.END, summary)
        if not history:
            self.history_list.insert(tk.END, "No history yet")


__all__ = ["MainWindow"]
