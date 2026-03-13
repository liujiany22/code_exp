from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from config.settings import (
    DEFAULT_SESSION_ID,
    RAW_BEH_DIR,
    TRIGGER_MODE,
    TRIGGER_PORT,
)
from eeg.trigger import TriggerClient, get_trigger


@dataclass
class ExperimentContext:
    participant_id: str
    session_id: str
    run_id: str
    output_dir: Path
    trigger: TriggerClient


def build_context(
    participant_id: str = "pilot",
    session_id: str = DEFAULT_SESSION_ID,
) -> ExperimentContext:
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = RAW_BEH_DIR / participant_id / session_id / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    return ExperimentContext(
        participant_id=participant_id,
        session_id=session_id,
        run_id=run_id,
        output_dir=output_dir,
        trigger=get_trigger(TRIGGER_MODE, port=TRIGGER_PORT),
    )
