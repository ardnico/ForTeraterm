"""Main application window for the launcher."""

from __future__ import annotations

import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox
from pathlib import Path

import customtkinter as ctk

from ..credential_store import CredentialStore
from ..launcher import Launcher
from ..ssh_options import parse_ssh_options
from ..storage import AppSettings, CommandSet, DataStore, Profile
from ..ttl_renderer import TTLRenderer
from .password_dialog import PasswordDialog
from .profile_dialog import ProfileDialog
from .settings_dialog import SettingsDialog
from .terminal_window import TerminalWindow


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
        self.visible_profiles: list[Profile] = []
        self.command_set_cache: dict[int, CommandSet] = {}
        self.history_records = []
        self.open_terminals: list[TerminalWindow] = []

        self.settings = self.storage.load_settings()
        self._apply_theme(self.settings)
        self._init_fonts()

        self._build_ui()
        self._load_profiles()

    def _apply_theme(self, settings: AppSettings) -> None:
        ctk.set_appearance_mode(settings.appearance_mode)
        ctk.set_default_color_theme(settings.color_theme)

    def _init_fonts(self) -> None:
        self.body_font = ctk.CTkFont(family=self.settings.font_family, size=self.settings.font_size)
        self.tk_body_font = tkfont.Font(family=self.settings.font_family, size=self.settings.font_size)

    def _available_fonts(self) -> list[str]:
        preferred = ["Arial", "Helvetica", "Consolas", "Meiryo", "MS Gothic", "Yu Gothic UI", "Courier New"]
        available = set(tkfont.families())
        options = [name for name in preferred if name in available]
        if self.settings.font_family not in options:
            options.append(self.settings.font_family)
        return options or [self.settings.font_family]

    def _build_ui(self) -> None:
        header = ctk.CTkFrame(self)
        header.pack(fill=tk.X, pady=(8, 4), padx=8)
        self.status_bar = ctk.CTkLabel(header, text=self._status_text(), font=self.body_font)
        self.status_bar.pack(side=tk.LEFT, padx=(4, 8))
        ctk.CTkButton(header, text="Settings", command=self._open_settings, font=self.body_font).pack(
            side=tk.RIGHT, padx=4
        )

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Profile list
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        ctk.CTkLabel(left_frame, text="Profiles", font=self.body_font).pack(anchor=tk.W, padx=6, pady=4)
        search_frame = ctk.CTkFrame(left_frame)
        search_frame.pack(fill=tk.X, padx=6, pady=(0, 4))
        ctk.CTkLabel(search_frame, text="Search", font=self.body_font).pack(side=tk.LEFT, padx=(0, 6))
        self.profile_search = tk.StringVar()
        entry = ctk.CTkEntry(search_frame, textvariable=self.profile_search, font=self.body_font)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        entry.bind("<KeyRelease>", lambda _event: self._load_profiles())
        self.profile_list = tk.Listbox(left_frame, exportselection=False, font=self.tk_body_font)
        self.profile_list.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        self.profile_list.bind("<<ListboxSelect>>", lambda event: self._on_select())

        btn_frame = ctk.CTkFrame(left_frame)
        btn_frame.pack(fill=tk.X, padx=6, pady=(0, 6))
        ctk.CTkButton(btn_frame, text="New Profile", command=self._new_profile, font=self.body_font).pack(
            side=tk.LEFT, padx=4
        )
        ctk.CTkButton(btn_frame, text="Edit Profile", command=self._edit_profile, font=self.body_font).pack(
            side=tk.LEFT, padx=4
        )
        ctk.CTkButton(btn_frame, text="Connect", command=self._connect, font=self.body_font).pack(
            side=tk.RIGHT, padx=4
        )

        details_frame = ctk.CTkFrame(left_frame)
        details_frame.pack(fill=tk.BOTH, expand=False, padx=6, pady=(0, 6))
        ctk.CTkLabel(details_frame, text="Server Details", font=self.body_font).pack(anchor=tk.W, padx=4, pady=(4, 0))
        self.details_box = tk.Text(details_frame, height=8, state="disabled", font=self.tk_body_font)
        self.details_box.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # History
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        ctk.CTkLabel(right_frame, text="Recent History", font=self.body_font).pack(anchor=tk.W, padx=6, pady=4)
        filter_frame = ctk.CTkFrame(right_frame)
        filter_frame.pack(fill=tk.X, padx=6, pady=(0, 6))
        ctk.CTkLabel(filter_frame, text="Result", font=self.body_font).pack(side=tk.LEFT, padx=4)
        self.result_filter = tk.StringVar(value="all")
        ctk.CTkOptionMenu(
            filter_frame,
            variable=self.result_filter,
            values=["all", "success", "failed", "unknown"],
            command=lambda _=None: self._load_history(),
            font=self.body_font,
        ).pack(side=tk.LEFT, padx=4)
        ctk.CTkLabel(filter_frame, text="Command Set", font=self.body_font).pack(side=tk.LEFT, padx=4)
        self.command_filter = tk.StringVar(value="all")
        self.command_menu = ctk.CTkOptionMenu(
            filter_frame,
            variable=self.command_filter,
            values=["all"],
            command=lambda _=None: self._load_history(),
            font=self.body_font,
        )
        self.command_menu.pack(side=tk.LEFT, padx=4)

        ctk.CTkButton(filter_frame, text="View Session Log", command=self._view_history_session, font=self.body_font).pack(
            side=tk.RIGHT,
            padx=4,
        )

        self.history_list = tk.Listbox(right_frame, exportselection=False, font=self.tk_body_font)
        self.history_list.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        self.history_list.bind("<Double-Button-1>", lambda event: self._relaunch_history())

    def _status_text(self) -> str:
        if self.cred_store.restricted:
            return "Credential Storage: Disabled (restricted mode)"
        if self.cred_store.mode == "local_encrypted":
            return "Credential Storage: Enabled (encrypted local vault)"
        return "Credential Storage: Enabled (Windows Credential Manager / keyring)"

    def _load_profiles(self) -> None:
        self.profile_list.delete(0, tk.END)
        profiles = self.storage.list_profiles()
        search_term = (self.profile_search.get() or "").strip()
        if search_term:
            profiles = self.storage.search_profiles(search_term)
        self.visible_profiles = profiles
        for profile in self.visible_profiles:
            display = f"{profile.name} ({profile.user}@{profile.host}:{profile.port})"
            self.profile_list.insert(tk.END, display)
        if self.visible_profiles:
            self.profile_list.selection_set(0)
            self._on_select()
        else:
            self.selected_profile = None
            self._update_details()
        
    def _get_selected_profile(self) -> Profile | None:
        selection = self.profile_list.curselection()
        if not selection:
            return None
        index = selection[0]
        if index >= len(self.visible_profiles):
            return None
        return self.visible_profiles[index]

    def _open_settings(self) -> None:
        dialog = SettingsDialog(
            self,
            current=self.settings,
            appearance_modes=["system", "light", "dark"],
            color_themes=["blue", "dark-blue", "green"],
            font_families=self._available_fonts(),
        )
        self.wait_window(dialog)
        if dialog.result is None:
            return
        self.settings = dialog.result
        self.storage.save_settings(self.settings)
        self._apply_theme(self.settings)
        self._init_fonts()
        self._rebuild_ui()

    def _rebuild_ui(self) -> None:
        selected_index = None
        if hasattr(self, "profile_list"):
            selection = self.profile_list.curselection()
            if selection:
                selected_index = selection[0]
        result_filter_value = self.result_filter.get()
        command_filter_value = self.command_filter.get()

        for child in self.winfo_children():
            child.destroy()

        self._build_ui()
        self._load_profiles()

        if selected_index is not None and self.profile_list.size() > selected_index:
            self.profile_list.selection_set(selected_index)
            self._on_select()
        self.result_filter.set(result_filter_value)
        if command_filter_value in self.command_menu.cget("values"):
            self.command_filter.set(command_filter_value)
        self._load_history()

    def _on_select(self) -> None:
        profile = self._get_selected_profile()
        self.selected_profile = profile
        self._update_command_filter()
        self._load_history()
        self._update_details()

    def _new_profile(self) -> None:
        dialog = ProfileDialog(self, storage=self.storage, cred_store=self.cred_store)
        self.wait_window(dialog)
        if dialog.created_profile:
            self.storage.list_profiles(refresh=True)
            self._load_profiles()

    def _edit_profile(self) -> None:
        profile = self._get_selected_profile()
        if profile is None:
            messagebox.showwarning("No profile", "Select a profile to edit")
            return
        command_set = self._get_command_set(profile.command_set_id)
        dialog = ProfileDialog(
            self,
            storage=self.storage,
            cred_store=self.cred_store,
            existing_profile=profile,
            command_set=command_set,
        )
        self.wait_window(dialog)
        if dialog.created_profile:
            self.storage.list_profiles(refresh=True)
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
        credential, password_fallback = self._resolve_credentials(profile)
        if password_fallback is False:
            return
        self._start_session(profile, command_set, credential, password_fallback)

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
        self._start_session(profile, command_set, credential, password_fallback)

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

    def _update_details(self) -> None:
        self.details_box.configure(state="normal")
        self.details_box.delete("1.0", tk.END)
        if not self.selected_profile:
            self.details_box.insert(tk.END, "Select a profile to see details")
        else:
            cs = self._get_command_set(self.selected_profile.command_set_id)
            forwards, extras = parse_ssh_options(self.selected_profile.ssh_options)
            lines = [
                f"Name: {self.selected_profile.name}",
                f"Host: {self.selected_profile.host}:{self.selected_profile.port}",
                f"User: {self.selected_profile.user}",
                f"Auth: {self.selected_profile.auth_type}",
                f"Credential: {self.selected_profile.cred_ref or '(prompted)'}",
            ]
            if forwards:
                lines.append("Port forwards:")
                for fwd in forwards:
                    lines.append(f"  {fwd.local_port} -> {fwd.remote_host}:{fwd.remote_port}")
            if extras:
                lines.append(f"Extra SSH options: {extras}")
            if cs.commands:
                lines.append("Commands:")
                for cmd in cs.commands:
                    lines.append(f"  {cmd}")
            else:
                lines.append("Commands: (none)")
            self.details_box.insert(tk.END, "\n".join(lines))
        self.details_box.configure(state="disabled")

    def _view_history_session(self) -> None:
        if not self.history_records:
            messagebox.showwarning("No history", "No history entries available")
            return
        selection = self.history_list.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Select a history entry")
            return
        record = self.history_records[selection[0]]
        if not record.wlog_path:
            messagebox.showwarning("Unavailable", "No session log recorded for this entry")
            return
        self._show_log_terminal(Path(record.wlog_path), f"History {record.connected_at}")

    def _show_log_terminal(self, wlog_path: Path, title: str) -> TerminalWindow:
        terminal = TerminalWindow(self, self.tk_body_font, wlog_path=wlog_path)
        terminal.title(title)
        self.open_terminals.append(terminal)
        return terminal

    def _show_live_terminal(
        self,
        profile: Profile,
        reconnect_cb,
        cancel_cb,
    ) -> TerminalWindow:
        terminal = TerminalWindow(self, self.tk_body_font, live=True, on_cancel=cancel_cb, on_reconnect=reconnect_cb)
        terminal.title(f"Live session for {profile.name}")
        self.open_terminals.append(terminal)
        return terminal

    def _resolve_credentials(self, profile: Profile) -> tuple[object | None, str | bool | None]:
        credential = None
        password_fallback: str | bool | None = None
        if profile.cred_ref and not self.cred_store.restricted:
            credential = self.cred_store.get(profile.cred_ref)
            if credential is None:
                if not messagebox.askyesno(
                    "Credential missing",
                    "Stored credential not found. Do you want to enter a one-time password?",
                ):
                    return None, False
        if credential is None:
            dialog = PasswordDialog(self, title="Enter password for this session")
            self.wait_window(dialog)
            password_fallback = dialog.password
            if password_fallback is None:
                return None, False
        return credential, password_fallback

    def _start_session(
        self,
        profile: Profile,
        command_set: CommandSet,
        credential,
        password_fallback,
    ) -> None:
        def on_reconnect() -> None:
            self._start_session(profile, command_set, credential, password_fallback)

        session_handle = None

        def cancel() -> None:
            if session_handle:
                session_handle.cancel()

        terminal = self._show_live_terminal(profile, reconnect_cb=on_reconnect, cancel_cb=cancel)
        terminal.set_status("Connecting...")

        def stream_cb(line: str) -> None:
            terminal.after(0, lambda: terminal.append_line(line))

        def complete_cb(result) -> None:
            def finalize() -> None:
                if result.wlog_path:
                    terminal.wlog_path = result.wlog_path
                    terminal.load_from_file()
                status = "Connected" if result.result == "success" else f"Failed: {result.error_code}"
                terminal.set_status(status)
                if result.result == "success":
                    messagebox.showinfo("Success", "Connection flow completed (stub mode)")
                else:
                    messagebox.showwarning("Failed", f"Connection failed: {result.error_code}")
                self._load_history()

            terminal.after(0, finalize)

        session_handle = self.launcher.launch_async(
            profile,
            command_set,
            credential,
            password_fallback,
            on_output=stream_cb,
            on_complete=complete_cb,
            max_retries=1,
        )


__all__ = ["MainWindow"]
