from __future__ import annotations

import sys
from pathlib import Path
from time import sleep

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.settings import DEFAULT_TRIGGER_WIDTH_MS, TRIGGER_MODE, TRIGGER_PORT
from config.settings import (
    EYELINK_BACKEND,
    EYELINK_CALIBRATION_TYPE,
    EYELINK_DUMMY_MODE,
    EYELINK_ENABLED,
    EYELINK_HOST_IP,
    EYELINK_INITIALIZE_CONTEXT,
    EYELINK_MESSAGE_PREFIX,
    EYELINK_PYLINK_PATH,
    EYELINK_RELAY_HOST,
    EYELINK_RELAY_PORT,
    EYELINK_RELAY_TIMEOUT_SECONDS,
    EYELINK_SCREEN_HEIGHT,
    EYELINK_SCREEN_WIDTH,
    TRIGGER_BAUDRATE,
    TRIGGER_RESET_CODE,
    TRIGGER_SERIAL_ENCODING,
    TRIGGER_SERIAL_TERMINATOR,
    TRIGGER_TIMEOUT_SECONDS,
    TRIGGER_WRITE_TIMEOUT_SECONDS,
)
from eeg.trigger import (
    EyeLinkRelaySettings,
    EyeLinkTriggerSettings,
    SerialTriggerSettings,
    get_trigger,
)


def main() -> None:
    trigger = get_trigger(
        TRIGGER_MODE,
        port=TRIGGER_PORT,
        serial_settings=SerialTriggerSettings(
            baudrate=TRIGGER_BAUDRATE,
            timeout_seconds=TRIGGER_TIMEOUT_SECONDS,
            write_timeout_seconds=TRIGGER_WRITE_TIMEOUT_SECONDS,
            reset_code=TRIGGER_RESET_CODE,
            encoding=TRIGGER_SERIAL_ENCODING,
            terminator=TRIGGER_SERIAL_TERMINATOR,
        ),
        eyelink_settings=(
            None
            if not EYELINK_ENABLED
            else (
                EyeLinkRelaySettings(
                    host=EYELINK_RELAY_HOST,
                    port=EYELINK_RELAY_PORT,
                    timeout_seconds=EYELINK_RELAY_TIMEOUT_SECONDS,
                    message_prefix=EYELINK_MESSAGE_PREFIX,
                )
                if EYELINK_BACKEND == "relay"
                else EyeLinkTriggerSettings(
                    host_ip=EYELINK_HOST_IP,
                    dummy_mode=EYELINK_DUMMY_MODE,
                    pylink_path=EYELINK_PYLINK_PATH,
                    screen_width=EYELINK_SCREEN_WIDTH,
                    screen_height=EYELINK_SCREEN_HEIGHT,
                    initialize_context=EYELINK_INITIALIZE_CONTEXT,
                    calibration_type=EYELINK_CALIBRATION_TYPE,
                    message_prefix=EYELINK_MESSAGE_PREFIX,
                )
            )
        ),
    )
    for code in (1, 2, 3):
        trigger.pulse(code, width_ms=DEFAULT_TRIGGER_WIDTH_MS)
        sleep(0.5)
    trigger.close()


if __name__ == "__main__":
    main()
