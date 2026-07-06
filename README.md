# File Sorter

File Sorter is a small Python utility that organizes files in a directory into type-based subfolders. It also includes a graphical scheduler helper for automatic execution on Windows.

## Project files

- `file_sorter.py` — CLI tool to sort files by extension into folders such as `Images`, `Documents`, `Audio`, `Video`, `Archives`, `Code`, and `Text`.
- `gui_scheduler.py` — Tkinter GUI to select a target folder, create category folders, save preferences, and optionally register a Windows Task Scheduler task.
- `LICENSE` — MIT license for this project.
- `.gitignore` — common Python ignores.

## Requirements

- Python 3.8 or newer
- On Windows: `schtasks` is required for the scheduling feature

## Quick start

### 1) Run the CLI sorter

```powershell
python file_sorter.py
```

Enter the directory path when prompted, or press Enter to sort the current working folder.

### 2) Use the scheduler GUI

```powershell
python gui_scheduler.py
```

The GUI lets you:

- choose a target folder
- create the category folders automatically
- save scheduler settings to `scheduler_settings.json`
- register a Windows scheduled task to run the sorter automatically

## Scheduling options

The GUI provides English scheduling options:

- `Once a day`
- `Every N days`
- `Once a week`
- `Once every 2 weeks`
- `Once a month`

## Features

- Auto-moves files into type-based folders
- Supports common file types for images, documents, audio, video, archives, code, and text
- Simple command line interface
- Graphical interface for Windows scheduling
- Saves scheduler preferences for later reuse

## Notes

- The scheduling feature uses Windows Task Scheduler and only works on Windows systems with `schtasks` available.
- Always test the sorter in a non-critical folder first to confirm the output structure.

## License

This project is licensed under the MIT License. See `LICENSE`.

## Contributions

Contributions are welcome. Suggested improvements:

- add a `--dry-run` preview mode
- add file move logging
- add unit tests for the sorting logic
- support cross-platform scheduling (cron or systemd)
