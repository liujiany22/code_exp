from __future__ import annotations

# Edit this file on the acquisition machine if you do not want to set
# environment variables in the terminal every time. Environment variables
# still take priority over these values when both are present.

# EEG trigger settings
TRIGGER_MODE = "dummy"
TRIGGER_PORT = ""
TRIGGER_BAUDRATE = 115200
TRIGGER_TIMEOUT_SECONDS = 1.0
TRIGGER_WRITE_TIMEOUT_SECONDS = 1.0
TRIGGER_RESET_CODE = 0
TRIGGER_SERIAL_ENCODING = "byte"
TRIGGER_SERIAL_TERMINATOR = b""

# EyeLink message-only settings
EYELINK_ENABLED = True
EYELINK_HOST_IP = "100.1.1.1"
EYELINK_DUMMY_MODE = False
EYELINK_PYLINK_PATH = ""
EYELINK_SCREEN_WIDTH = 1920
EYELINK_SCREEN_HEIGHT = 1080
EYELINK_INITIALIZE_CONTEXT = False
EYELINK_CALIBRATION_TYPE = "HV9"
EYELINK_MESSAGE_PREFIX = "TRIGGER"
