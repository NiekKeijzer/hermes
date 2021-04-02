from typing import Iterable
from pathlib import Path


def ensure_dirs(directories: Iterable[Path]) -> None:
    for directory in directories:
        if not directory.exists() or not directory.is_dir():
            directory.mkdir(0o755, parents=True)