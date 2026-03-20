from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from tasks.learning_cycle.task import run as run_learning_cycle
from tasks.mental_arithmetic.task import run as run_mental_arithmetic
from tasks.protocol.task import run as run_protocol
from tasks.resting_state.task import run as run_resting_state
from tasks.wm_pretest.task import run as run_wm_pretest


@dataclass(frozen=True)
class TaskSpec:
    slug: str
    name: str
    runner: Callable


TASK_REGISTRY = [
    TaskSpec(slug="protocol", name="Full Protocol", runner=run_protocol),
    TaskSpec(slug="resting_state", name="Resting State", runner=run_resting_state),
    TaskSpec(slug="wm_pretest", name="Working Memory Pretest", runner=run_wm_pretest),
    TaskSpec(slug="mental_arithmetic", name="Mental Arithmetic", runner=run_mental_arithmetic),
    TaskSpec(slug="learning_cycle", name="Learning Cycle", runner=run_learning_cycle),
]

TASK_MAP = {task.slug: task for task in TASK_REGISTRY}
DEFAULT_TASK_SLUG = "protocol"
