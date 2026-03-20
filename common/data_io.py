from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import shutil
import tempfile

from common.participant_info import ParticipantInfo, write_participant_info
from config.settings import (
    DEFAULT_SESSION_ID,
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
    RAW_BEH_DIR,
    TRIGGER_BAUDRATE,
    TRIGGER_MODE,
    TRIGGER_NEURACLE_DEVICE_ID,
    TRIGGER_NEURACLE_DEVICE_NAME_FUNCTION_ID,
    TRIGGER_NEURACLE_ERROR_FUNCTION_ID,
    TRIGGER_NEURACLE_OUTPUT_FUNCTION_ID,
    TRIGGER_PORT,
    TRIGGER_RESET_CODE,
    TRIGGER_SERIAL_ENCODING,
    TRIGGER_SERIAL_TERMINATOR,
    TRIGGER_TIMEOUT_SECONDS,
    TRIGGER_WRITE_TIMEOUT_SECONDS,
)
from eeg.trigger import (
    EyeLinkRelaySettings,
    EyeLinkTriggerSettings,
    NeuracleSerialTriggerSettings,
    SerialTriggerSettings,
    TriggerClient,
    get_trigger,
)


@dataclass
class ExperimentContext:
    participant_id: str
    session_id: str
    run_id: str
    output_dir: Path
    trigger: TriggerClient
    participant_info: ParticipantInfo
    persist_outputs: bool = True
    temp_root: Path | None = None


def build_context(
    participant_id: str = "pilot",
    session_id: str = DEFAULT_SESSION_ID,
    participant_info: ParticipantInfo | None = None,
    persist_outputs: bool = True,
) -> ExperimentContext:
    if participant_info is None:
        participant_info = ParticipantInfo(
            participant_id=participant_id,
            session_id=session_id,
            name="",
            age="",
        )
    participant_id = participant_info.participant_id
    session_id = participant_info.session_id
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_root = None
    if persist_outputs:
        output_dir = RAW_BEH_DIR / participant_id / session_id / run_id
        output_dir.mkdir(parents=True, exist_ok=True)
        write_participant_info(output_dir, participant_info, run_id)
    else:
        temp_root = Path(
            tempfile.mkdtemp(prefix="code_exp_test_", dir=tempfile.gettempdir())
        )
        output_dir = temp_root / participant_id / session_id / run_id
        output_dir.mkdir(parents=True, exist_ok=True)

    return ExperimentContext(
        participant_id=participant_id,
        session_id=session_id,
        run_id=run_id,
        output_dir=output_dir,
        participant_info=participant_info,
        persist_outputs=persist_outputs,
        temp_root=temp_root,
        trigger=get_trigger(
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
            neuracle_serial_settings=NeuracleSerialTriggerSettings(
                baudrate=TRIGGER_BAUDRATE,
                timeout_seconds=TRIGGER_TIMEOUT_SECONDS,
                write_timeout_seconds=TRIGGER_WRITE_TIMEOUT_SECONDS,
                device_id=TRIGGER_NEURACLE_DEVICE_ID,
                output_function_id=TRIGGER_NEURACLE_OUTPUT_FUNCTION_ID,
                error_function_id=TRIGGER_NEURACLE_ERROR_FUNCTION_ID,
                device_name_function_id=TRIGGER_NEURACLE_DEVICE_NAME_FUNCTION_ID,
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
        ),
    )


def cleanup_context(context: ExperimentContext) -> None:
    if context.temp_root is None:
        return
    shutil.rmtree(context.temp_root, ignore_errors=True)
