from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ExternalTaskSpec:
    name: str
    script_path: Path
    task_code_start: int
    task_code_end: int


def load_module_from_path(module_name: str, script_path: Path) -> Any:
    if not script_path.exists():
        raise FileNotFoundError(f"Task script not found: {script_path}")

    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module spec from {script_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
