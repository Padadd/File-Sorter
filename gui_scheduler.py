#!/usr/bin/env python3
"""GUI to configure file sorter target folders and schedule runs.

Features:
- Choose target directory and create category folders.
- Schedule a Windows Task Scheduler job to run `file_sorter.py` daily or weekly.

Notes:
- Scheduling uses `schtasks` and therefore works on Windows. The GUI still works cross-platform
  but the scheduling button will show a message if `schtasks` is unavailable.
"""
from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Dict

SETTINGS_FILE = "scheduler_settings.json"


def save_settings(data: Dict) -> None:
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_settings() -> Dict:
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def create_category_folders(path: str) -> None:
    # Mirror the categories from file_sorter.TYPE_MAP
    categories = [
        "Images",
        "Documents",
        "Audio",
        "Video",
        "Archives",
        "Code",
        "Text",
    ]
    for c in categories:
        try:
            os.makedirs(os.path.join(path, c), exist_ok=True)
        except Exception:
            pass


def schtasks_available() -> bool:
    try:
        subprocess.run(["schtasks"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def register_schtask(python_exe: str, script_path: str, target_dir: str, when: str, mode: str, days: str) -> subprocess.CompletedProcess:
    # Build the command for schtasks
    # Example: schtasks /Create /SC DAILY /TN "FileSorter" /TR "python C:\path\file_sorter.py C:\target" /ST 14:00 /F
    name = f"FileSorter_{os.path.basename(target_dir)}"
    tr = f'"{shlex.quote(python_exe)}" "{script_path}" "{target_dir}"'
    cmd = [
        "schtasks",
        "/Create",
        "/SC",
        mode.upper(),
        "/TN",
        name,
        "/TR",
        tr,
        "/ST",
        when,
        "/F",
    ]
    if mode.upper() == "WEEKLY" and days:
        cmd.extend(["/D", days])
    return subprocess.run(cmd, capture_output=True, text=True)


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("File Sorter Scheduler")

        self.settings = load_settings()

        tk.Label(root, text="Target directory:").grid(row=0, column=0, sticky="w")
        self.path_var = tk.StringVar(value=self.settings.get("path", ""))
        tk.Entry(root, textvariable=self.path_var, width=60).grid(row=0, column=1)
        tk.Button(root, text="Browse", command=self.browse).grid(row=0, column=2)

        tk.Button(root, text="Create category folders", command=self.create_folders).grid(row=1, column=1, sticky="w")

        tk.Label(root, text="Schedule:").grid(row=2, column=0, sticky="w")
        self.mode_var = tk.StringVar(value=self.settings.get("mode", "DAILY"))
        tk.OptionMenu(root, self.mode_var, "DAILY", "WEEKLY").grid(row=2, column=1, sticky="w")

        tk.Label(root, text="Time (HH:MM, 24h):").grid(row=3, column=0, sticky="w")
        self.time_var = tk.StringVar(value=self.settings.get("time", "09:00"))
        tk.Entry(root, textvariable=self.time_var, width=10).grid(row=3, column=1, sticky="w")

        tk.Label(root, text="Weekdays (MON,TUE,... for weekly):").grid(row=4, column=0, sticky="w")
        self.days_var = tk.StringVar(value=self.settings.get("days", "MON"))
        tk.Entry(root, textvariable=self.days_var, width=20).grid(row=4, column=1, sticky="w")

        tk.Button(root, text="Save settings", command=self.save).grid(row=5, column=0)
        tk.Button(root, text="Create scheduled task", command=self.schedule).grid(row=5, column=1)

    def browse(self):
        d = filedialog.askdirectory(initialdir=os.getcwd())
        if d:
            self.path_var.set(d)

    def create_folders(self):
        p = self.path_var.get().strip() or os.getcwd()
        try:
            create_category_folders(p)
            messagebox.showinfo("Done", f"Category folders created in {p}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save(self):
        data = {"path": self.path_var.get(), "mode": self.mode_var.get(), "time": self.time_var.get(), "days": self.days_var.get()}
        save_settings(data)
        messagebox.showinfo("Saved", f"Settings saved to {SETTINGS_FILE}")

    def schedule(self):
        p = self.path_var.get().strip() or os.getcwd()
        when = self.time_var.get().strip()
        mode = self.mode_var.get().strip()
        days = self.days_var.get().strip()
        # Validate time
        if not when or len(when) != 5 or when[2] != ":":
            messagebox.showerror("Invalid time", "Time must be in HH:MM format")
            return

        if os.name != "nt":
            messagebox.showerror("Unsupported", "Scheduling via Task Scheduler is only supported on Windows (schtasks)")
            return

        if not schtasks_available():
            messagebox.showerror("Missing", "`schtasks` not found on this system")
            return

        python_exe = sys.executable or "python"
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "file_sorter.py"))

        res = register_schtask(python_exe, script_path, p, when, mode, days if mode == "WEEKLY" else "")
        if res.returncode == 0:
            messagebox.showinfo("Scheduled", "Task created successfully")
        else:
            messagebox.showerror("Failed", f"schtasks failed:\n{res.stdout}\n{res.stderr}")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
