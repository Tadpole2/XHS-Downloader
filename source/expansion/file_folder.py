from contextlib import suppress
from pathlib import Path
import os


def file_switch(path: Path) -> None:
    if path.exists():
        path.unlink()
    else:
        path.touch()


def remove_empty_directories(path: Path) -> None:
    # Using os.sep makes the exclude patterns cross-platform.
    # This will match path components like "/.git" or "\__pycache__".
    sep = os.sep
    exclude = {
        f"{sep}.",
        f"{sep}_",
    }
    # The argument is 'topdown', not 'top_down'.
    # We walk from the bottom up to delete empty subdirectories before their parents.
    for dir_path_str, dir_names, file_names in os.walk(path, topdown=False):
        if any(ex in dir_path_str for ex in exclude):
            continue
        if not dir_names and not file_names:
            with suppress(OSError):
                # os.walk yields strings, so we convert back to Path to use rmdir()
                Path(dir_path_str).rmdir()
