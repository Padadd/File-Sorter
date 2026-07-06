#!/usr/bin/env python3
"""Simple file sorter: moves files into subfolders by type.

Prompts for a directory (defaults to current directory), scans files,
creates folders for types, moves files, and prints a summary.
"""
from __future__ import annotations

import os
import shutil
from collections import defaultdict
from typing import Dict, Set

TYPE_MAP: Dict[str, Set[str]] = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"},
    "Documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"},
    "Video": {".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm"},
    "Archives": {".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"},
    "Code": {".py", ".js", ".ts", ".java", ".c", ".cpp", ".cs", ".go", ".rb", ".php", ".html", ".css"},
    "Text": {".txt", ".md", ".rtf", ".log"},
}


def get_category(ext: str) -> str:
    ext = ext.lower()
    for category, exts in TYPE_MAP.items():
        if ext in exts:
            return category
    if ext:
        return ext.lstrip(".").upper()
    return "No_Extension"


def organize_directory(path: str) -> Dict[str, int]:
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        raise NotADirectoryError(f"Not a directory: {path}")

    moved_counts: Dict[str, int] = defaultdict(int)
    total_files = 0
    errors = []

    try:
        script_path = os.path.abspath(__file__)
    except NameError:
        script_path = ""

    for entry in os.listdir(path):
        src = os.path.join(path, entry)
        if not os.path.isfile(src):
            continue
        # don't move the running script
        try:
            if script_path and os.path.abspath(src) == script_path:
                continue
        except Exception:
            pass

        total_files += 1
        _, ext = os.path.splitext(entry)
        category = get_category(ext)
        dest_dir = os.path.join(path, category)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, entry)
        try:
            shutil.move(src, dest)
            moved_counts[category] += 1
        except Exception as e:
            errors.append((entry, str(e)))

    moved_counts["_total_scanned"] = total_files
    moved_counts["_errors"] = len(errors)
    return dict(moved_counts)


def main():
    print("File Sorter — organize files into folders by type")
    path = input("Enter directory path to organize (leave empty for current dir): ").strip() or "."
    path = os.path.expanduser(path)
    try:
        summary = organize_directory(path)
    except Exception as e:
        print(f"Error: {e}")
        return

    total = summary.pop("_total_scanned", 0)
    errs = summary.pop("_errors", 0)
    print(f"Scanned {total} files in: {os.path.abspath(path)}")
    if summary:
        print("Moved files:")
        for cat, count in sorted(summary.items(), key=lambda x: (-x[1], x[0])):
            print(f" - {cat}: {count}")
    if errs:
        print(f"Completed with {errs} errors (some files may not have been moved).")
    else:
        print("Completed without errors.")


if __name__ == "__main__":
    main()
