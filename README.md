# File Sorter

Small Python utilities to organize files by type and optionally schedule automatic runs.

Contents
- `file_sorter.py` — CLI tool that scans a directory, creates subfolders by type (Images, Documents, Audio, Video, Archives, Code, Text), and moves files into them.
- `gui_scheduler.py` — Tkinter-based GUI to choose a target directory, create category folders, save settings, and register a Windows Task Scheduler job using `schtasks`.

Quick start

Requirements: Python 3.8 or newer.

Run the CLI sorter:

```powershell
python file_sorter.py
```

Run the GUI (Windows recommended for scheduling):

```powershell
python gui_scheduler.py
```

Features
- Organizes files into category folders by common file extensions.
- GUI lets you select a target folder, create category folders, and schedule automatic runs.
- Scheduling options (English): "Once a day", "Every N days", "Once a week", "Once every 2 weeks", "Once a month".
- Settings are saved to `scheduler_settings.json` when saved from the GUI.

Notes
- Scheduling integrations use Windows `schtasks` — available only on Windows. The GUI will notify if `schtasks` is not found.
- Test the sorter in a sample folder before running it on important directories.

Contributing
- Suggestions: add a `--dry-run` preview mode, improved logging, unit tests for `organize_directory()`, or cross-platform scheduling (cron/systemd).

License
- No license specified. Add a `LICENSE` file to make this project open-source.
