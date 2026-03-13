from __future__ import annotations

import os
from pathlib import Path


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

TRIGGER_MODE = "dummy"
TRIGGER_PORT = ""
DEFAULT_TRIGGER_WIDTH_MS = 10
DEFAULT_SESSION_ID = "001"
REST_EYES_OPEN_SECONDS = 180
REST_EYES_CLOSED_SECONDS = 180
REST_CYCLE_COUNT = 1
REST_FULLSCREEN = os.environ.get("REST_FULLSCREEN", "0") == "1"
REST_ALLOW_GUI = os.environ.get("REST_ALLOW_GUI", "1") != "0"
REST_WINDOW_SIZE = (1280, 800)
REST_BACKGROUND_COLOR = "black"
REST_TEXT_COLOR = "white"
REST_FONT = "Arial"
PSYCHOPY_MIN_VERSION = "2025.1.1"
PSYCHOPY_AUDIO_LIB = os.environ.get("PSYCHOPY_AUDIO_LIB", "ptb")
WM_PRETEST_KEYBOARD_BACKEND = os.environ.get("WM_PRETEST_KEYBOARD_BACKEND", "event")
WM_PRETEST_FRAME_RATE_FALLBACK = float(
    os.environ.get("WM_PRETEST_FRAME_RATE_FALLBACK", "60")
)
WM_PRETEST_MACOS_WINDOWED = os.environ.get("WM_PRETEST_MACOS_WINDOWED", "1") != "0"
WM_PRETEST_FORCE_MOUSE_VISIBLE = (
    os.environ.get("WM_PRETEST_FORCE_MOUSE_VISIBLE", "1") != "0"
)
MENTAL_ARITHMETIC_FULLSCREEN = (
    os.environ.get("MENTAL_ARITHMETIC_FULLSCREEN", "0") == "1"
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
MENTAL_ARITHMETIC_FONT = "Arial"
MENTAL_ARITHMETIC_FIXATION_SECONDS = 1.0
MENTAL_ARITHMETIC_INTER_TRIAL_SECONDS = 0.5
MENTAL_ARITHMETIC_RESPONSE_TIMEOUT_SECONDS = 15.0
MENTAL_ARITHMETIC_RANDOM_SEED = None
MENTAL_ARITHMETIC_TRIALS_PER_LEVEL = {
    "QE": 6,
    "QM": 6,
    "QH": 6,
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
LEARNING_CYCLE_QUESTIONNAIRE_DIR = QUESTIONNAIRE_DIR
LEARNING_CYCLE_FULLSCREEN = os.environ.get("LEARNING_CYCLE_FULLSCREEN", "0") == "1"
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
