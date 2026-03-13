from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from tasks.learning_cycle.task import run as run_learning_cycle
from tasks.mental_arithmetic.task import run as run_mental_arithmetic
from tasks.resting_state.task import run as run_resting_state
from tasks.wm_pretest.task import run as run_wm_pretest


@dataclass(frozen=True)
class TaskSpec:
    name: str
    runner: Callable


TASK_REGISTRY = [
    TaskSpec(name="Resting State", runner=run_resting_state),
    TaskSpec(name="Working Memory Pretest", runner=run_wm_pretest),
    TaskSpec(name="Mental Arithmetic", runner=run_mental_arithmetic),
    TaskSpec(name="Learning Cycle", runner=run_learning_cycle),
]
