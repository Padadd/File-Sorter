# File Sorter

Simple utility to organize files in a directory into subfolders by file type.

Usage:

```
python file_sorter.py
```

When prompted, enter the directory path to organize or leave empty to use the current directory.

The script creates folders like `Images`, `Documents`, `Text`, etc., and moves files accordingly.

GUI and scheduling
- Run `gui_scheduler.py` to open a simple GUI to choose a target directory, create the target folders, and schedule automatic runs.
- On Windows the GUI can create a Task Scheduler job (uses `schtasks`) to run `file_sorter.py` daily or weekly at a chosen time.
- The GUI saves settings to `scheduler_settings.json` in the repository.

See `file_sorter.py` and `gui_scheduler.py` for implementation details.