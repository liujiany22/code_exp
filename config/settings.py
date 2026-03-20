from __future__ import annotations

import os
from pathlib import Path

try:
    from . import local_settings as _local_settings
except ImportError:
    _local_settings = None


def _local_value(name: str, default):
    if _local_settings is None:
        return default
    return getattr(_local_settings, name, default)


def _bool_from_env_or_local(name: str, default: bool) -> bool:
    local_default = _local_value(name, default)
    raw = os.environ.get(name)
    if raw is None:
        return bool(local_default)
    return raw != "0"


def _int_from_env_or_local(name: str, default: int) -> int:
    return int(os.environ.get(name, str(_local_value(name, default))))


def _float_from_env_or_local(name: str, default: float) -> float:
    return float(os.environ.get(name, str(_local_value(name, default))))


def _str_from_env_or_local(name: str, default: str) -> str:
    return os.environ.get(name, str(_local_value(name, default)))


def _bytes_from_env_or_local(name: str, default: bytes) -> bytes:
    raw = os.environ.get(name)
    if raw is not None:
        return raw.encode("ascii")
    local_default = _local_value(name, default)
    if isinstance(local_default, bytes):
        return local_default
    return str(local_default).encode("ascii")


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_BEH_DIR = DATA_DIR / "raw_beh"
LOG_DIR = DATA_DIR / "logs"
STIMULI_DIR = BASE_DIR / "stimuli"
VIDEO_DIR = STIMULI_DIR / "videos"
IMAGE_DIR = STIMULI_DIR / "images"
CONDITION_DIR = STIMULI_DIR / "conditions"
QUESTIONNAIRE_DIR = STIMULI_DIR / "questionnaires"
REFERENCE_DIR = BASE_DIR / "cognitiveabilitytest"
DIGIT_SPAN_DIR = REFERENCE_DIR / "digit_span-master_new"
DIGIT_SPAN_SCRIPT = DIGIT_SPAN_DIR / "digit_span_lastrun.py"
CORSI_BLOCKS_DIR = REFERENCE_DIR / "corsi_blocks-master_new"
CORSI_BLOCKS_SCRIPT = CORSI_BLOCKS_DIR / "corsi_blocks_lastrun.py"

TRIGGER_MODE = _str_from_env_or_local("TRIGGER_MODE", "dummy")
TRIGGER_PORT = _str_from_env_or_local("TRIGGER_PORT", "")
TRIGGER_BAUDRATE = _int_from_env_or_local("TRIGGER_BAUDRATE", 115200)
TRIGGER_TIMEOUT_SECONDS = _float_from_env_or_local("TRIGGER_TIMEOUT_SECONDS", 1.0)
TRIGGER_WRITE_TIMEOUT_SECONDS = _float_from_env_or_local(
    "TRIGGER_WRITE_TIMEOUT_SECONDS",
    1.0,
)
TRIGGER_RESET_CODE = _int_from_env_or_local("TRIGGER_RESET_CODE", 0)
TRIGGER_SERIAL_ENCODING = _str_from_env_or_local("TRIGGER_SERIAL_ENCODING", "byte")
TRIGGER_SERIAL_TERMINATOR = _bytes_from_env_or_local(
    "TRIGGER_SERIAL_TERMINATOR",
    b"",
)
EYELINK_ENABLED = _bool_from_env_or_local("EYELINK_ENABLED", False)
EYELINK_BACKEND = _str_from_env_or_local("EYELINK_BACKEND", "direct")
EYELINK_HOST_IP = _str_from_env_or_local("EYELINK_HOST_IP", "100.1.1.1")
EYELINK_DUMMY_MODE = _bool_from_env_or_local("EYELINK_DUMMY_MODE", False)
EYELINK_PYLINK_PATH = _str_from_env_or_local("EYELINK_PYLINK_PATH", "")
EYELINK_RELAY_HOST = _str_from_env_or_local("EYELINK_RELAY_HOST", "127.0.0.1")
EYELINK_RELAY_PORT = _int_from_env_or_local("EYELINK_RELAY_PORT", 18765)
EYELINK_RELAY_TIMEOUT_SECONDS = _float_from_env_or_local(
    "EYELINK_RELAY_TIMEOUT_SECONDS",
    3.0,
)
EYELINK_SCREEN_WIDTH = _int_from_env_or_local("EYELINK_SCREEN_WIDTH", 1920)
EYELINK_SCREEN_HEIGHT = _int_from_env_or_local("EYELINK_SCREEN_HEIGHT", 1080)
EYELINK_INITIALIZE_CONTEXT = _bool_from_env_or_local(
    "EYELINK_INITIALIZE_CONTEXT",
    False,
)
EYELINK_CALIBRATION_TYPE = _str_from_env_or_local("EYELINK_CALIBRATION_TYPE", "HV9")
EYELINK_MESSAGE_PREFIX = _str_from_env_or_local("EYELINK_MESSAGE_PREFIX", "TRIGGER")
DEFAULT_TRIGGER_WIDTH_MS = 10
DEFAULT_SESSION_ID = "001"
REST_EYES_OPEN_SECONDS = 180
REST_EYES_CLOSED_SECONDS = 180
REST_CYCLE_COUNT = 1
REST_TEST_EYES_OPEN_SECONDS = 3
REST_TEST_EYES_CLOSED_SECONDS = 3
REST_TEST_CYCLE_COUNT = 1
REST_FULLSCREEN = _bool_from_env_or_local("REST_FULLSCREEN", True)
REST_ALLOW_GUI = _bool_from_env_or_local("REST_ALLOW_GUI", True)
REST_WINDOW_SIZE = (1280, 800)
REST_BACKGROUND_COLOR = "black"
REST_TEXT_COLOR = "white"
REST_FONT = "Arial"
PSYCHOPY_MONITOR_NAME = _str_from_env_or_local("PSYCHOPY_MONITOR_NAME", "testMonitor")
PSYCHOPY_MIN_VERSION = "2025.1.1"
PSYCHOPY_AUDIO_LIB = os.environ.get("PSYCHOPY_AUDIO_LIB", "ptb")
WM_PRETEST_KEYBOARD_BACKEND = os.environ.get("WM_PRETEST_KEYBOARD_BACKEND", "event")
WM_PRETEST_FRAME_RATE_FALLBACK = float(
    os.environ.get("WM_PRETEST_FRAME_RATE_FALLBACK", "60")
)
WM_PRETEST_SKIP_FRAME_RATE_CHECK = (
    os.environ.get("WM_PRETEST_SKIP_FRAME_RATE_CHECK", "1") != "0"
)
WM_PRETEST_MACOS_WINDOWED = _bool_from_env_or_local("WM_PRETEST_MACOS_WINDOWED", False)
WM_PRETEST_FORCE_MOUSE_VISIBLE = (
    os.environ.get("WM_PRETEST_FORCE_MOUSE_VISIBLE", "1") != "0"
)
WM_PRETEST_TEST_TASK_TIMEOUT_SECONDS = 20.0
MENTAL_ARITHMETIC_FULLSCREEN = _bool_from_env_or_local(
    "MENTAL_ARITHMETIC_FULLSCREEN",
    True,
)
MENTAL_ARITHMETIC_ALLOW_GUI = (
    os.environ.get("MENTAL_ARITHMETIC_ALLOW_GUI", "1") != "0"
)
MENTAL_ARITHMETIC_FORCE_MOUSE_VISIBLE = (
    os.environ.get("MENTAL_ARITHMETIC_FORCE_MOUSE_VISIBLE", "1") != "0"
)
MENTAL_ARITHMETIC_WINDOW_SIZE = (1280, 800)
MENTAL_ARITHMETIC_BACKGROUND_COLOR = "black"
MENTAL_ARITHMETIC_TEXT_COLOR = "white"
MENTAL_ARITHMETIC_PROBE_COLOR = "blue"
MENTAL_ARITHMETIC_FONT = "Arial"
MENTAL_ARITHMETIC_FIXATION_SECONDS = 6.0
MENTAL_ARITHMETIC_PRE_RESPONSE_BLANK_SECONDS = 1.0
MENTAL_ARITHMETIC_INTER_TRIAL_SECONDS = 1.0
MENTAL_ARITHMETIC_RESPONSE_TIMEOUT_SECONDS = 4.0
MENTAL_ARITHMETIC_BLOCK_COUNT = 3
MENTAL_ARITHMETIC_TRIALS_PER_BLOCK = 25
MENTAL_ARITHMETIC_BLOCK_REST_SECONDS = 30.0
MENTAL_ARITHMETIC_RANDOM_SEED = None
MENTAL_ARITHMETIC_TRIALS_PER_LEVEL = {
    "QE": 25,
    "QM": 25,
    "QH": 25,
}
MENTAL_ARITHMETIC_TEST_FIXATION_SECONDS = 2.0
MENTAL_ARITHMETIC_TEST_PRE_RESPONSE_BLANK_SECONDS = 0.2
MENTAL_ARITHMETIC_TEST_INTER_TRIAL_SECONDS = 0.2
MENTAL_ARITHMETIC_TEST_RESPONSE_TIMEOUT_SECONDS = 3.0
MENTAL_ARITHMETIC_TEST_BLOCK_COUNT = 1
MENTAL_ARITHMETIC_TEST_TRIALS_PER_BLOCK = 3
MENTAL_ARITHMETIC_TEST_BLOCK_REST_SECONDS = 0.0
MENTAL_ARITHMETIC_TEST_TRIALS_PER_LEVEL = {
    "QE": 1,
    "QM": 1,
    "QH": 1,
}
MENTAL_ARITHMETIC_Q_RULES = {
    "QE": {
        "min_q": 0.0,
        "max_q": 2.0,
        "digit_pairs": ((1, 1), (2, 1)),
    },
    "QM": {
        "min_q": 2.0,
        "max_q": 4.0,
        "digit_pairs": ((2, 1), (2, 2), (3, 1)),
    },
    "QH": {
        "min_q": 4.0,
        "max_q": None,
        "digit_pairs": ((2, 2), (3, 2), (3, 3)),
    },
}
LEARNING_CYCLE_TRIALS_FILE = CONDITION_DIR / "learning_cycle_trials.csv"
LEARNING_CYCLE_TEST_TRIALS_FILE = CONDITION_DIR / "learning_cycle_trials_test.csv"
LEARNING_CYCLE_PROTOCOL_TRIALS_FILE = CONDITION_DIR / "learning_cycle_trials_protocol.csv"
LEARNING_CYCLE_PRACTICE_TRIALS_FILE = CONDITION_DIR / "learning_cycle_trials_practice.csv"
LEARNING_CYCLE_QUESTIONNAIRE_DIR = QUESTIONNAIRE_DIR
LEARNING_CYCLE_FULLSCREEN = _bool_from_env_or_local("LEARNING_CYCLE_FULLSCREEN", True)
LEARNING_CYCLE_ALLOW_GUI = os.environ.get("LEARNING_CYCLE_ALLOW_GUI", "1") != "0"
LEARNING_CYCLE_FORCE_MOUSE_VISIBLE = (
    os.environ.get("LEARNING_CYCLE_FORCE_MOUSE_VISIBLE", "1") != "0"
)
LEARNING_CYCLE_WINDOW_SIZE = (1280, 800)
LEARNING_CYCLE_BACKGROUND_COLOR = "black"
LEARNING_CYCLE_TEXT_COLOR = "white"
LEARNING_CYCLE_FONT = "Arial"
LEARNING_CYCLE_EXPECTED_TRIALS = 6
LEARNING_CYCLE_MISSING_VIDEO_SECONDS = 5.0
LEARNING_CYCLE_POST_PHASE_BLANK_SECONDS = 0.3
LEARNING_CYCLE_INTER_TRIAL_REST_SECONDS = 0.0
LEARNING_CYCLE_STATEMENT_SECONDS = 4.0
LEARNING_CYCLE_RESPONSE_SECONDS = 4.0
LEARNING_CYCLE_QUESTION_REST_SECONDS = 1.0
LEARNING_CYCLE_TEST_EXPECTED_TRIALS = 2
LEARNING_CYCLE_TEST_MISSING_VIDEO_SECONDS = 1.0
LEARNING_CYCLE_TEST_POST_PHASE_BLANK_SECONDS = 0.0
LEARNING_CYCLE_TEST_STATEMENT_SECONDS = 0.5
LEARNING_CYCLE_TEST_RESPONSE_SECONDS = 0.5
LEARNING_CYCLE_TEST_QUESTION_REST_SECONDS = 0.1


def ensure_directories() -> None:
    for path in (
        DATA_DIR,
        RAW_BEH_DIR,
        LOG_DIR,
        STIMULI_DIR,
        VIDEO_DIR,
        IMAGE_DIR,
        CONDITION_DIR,
        QUESTIONNAIRE_DIR,
    ):
        path.mkdir(parents=True, exist_ok=True)
