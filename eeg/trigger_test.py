from __future__ import annotations

import sys
from pathlib import Path
from time import sleep

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.settings import DEFAULT_TRIGGER_WIDTH_MS, TRIGGER_MODE, TRIGGER_PORT
from eeg.trigger import get_trigger


def main() -> None:
    trigger = get_trigger(TRIGGER_MODE, port=TRIGGER_PORT)
    for code in (1, 2, 3):
        trigger.pulse(code, width_ms=DEFAULT_TRIGGER_WIDTH_MS)
        sleep(0.5)
    trigger.close()


if __name__ == "__main__":
    main()
