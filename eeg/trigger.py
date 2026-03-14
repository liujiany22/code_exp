from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import socket
import sys
from time import monotonic, sleep
from typing import Optional


class BaseTriggerBackend:
    def connect(self) -> None:
        pass

    def send_code(self, code: int, name: str | None = None) -> None:
        raise NotImplementedError

    def reset(self) -> None:
        pass

    def close(self) -> None:
        pass


@dataclass
class DummyTriggerBackend(BaseTriggerBackend):
    label: str = "dummy"

    def connect(self) -> None:
        print(f"[{self.label}] trigger backend connected")

    def send_code(self, code: int, name: str | None = None) -> None:
        suffix = "" if not name else f" name={name}"
        print(f"[{self.label}] trigger_code={code}{suffix}")

    def reset(self) -> None:
        print(f"[{self.label}] trigger_reset")


@dataclass(frozen=True)
class SerialTriggerSettings:
    baudrate: int = 115200
    timeout_seconds: float = 1.0
    write_timeout_seconds: float = 1.0
    reset_code: int | None = 0
    encoding: str = "byte"
    terminator: bytes = b""
    label: str = "serial"


class SerialTriggerBackend(BaseTriggerBackend):
    def __init__(
        self,
        port: str,
        settings: SerialTriggerSettings | None = None,
    ) -> None:
        self.port = port
        self.settings = settings or SerialTriggerSettings()
        self._serial = None

    def connect(self) -> None:
        if not self.port:
            raise RuntimeError(
                "TRIGGER_PORT is empty. Set the serial port before using "
                "TRIGGER_MODE='serial'."
            )

        try:
            import serial  # type: ignore
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "pyserial is required for serial trigger mode. "
                "Install it with `python -m pip install pyserial`."
            ) from exc

        self._serial = serial.Serial(
            port=self.port,
            baudrate=self.settings.baudrate,
            timeout=self.settings.timeout_seconds,
            write_timeout=self.settings.write_timeout_seconds,
        )
        self._reset_buffers()
        print(
            f"[{self.settings.label}] trigger backend connected "
            f"port={self.port} baudrate={self.settings.baudrate} "
            f"encoding={self.settings.encoding}"
        )

    def send_code(self, code: int, name: str | None = None) -> None:
        payload = self._encode_code(code)
        self._write_payload(payload)

    def reset(self) -> None:
        if self.settings.reset_code is None:
            return
        payload = self._encode_code(self.settings.reset_code)
        self._write_payload(payload)

    def close(self) -> None:
        if self._serial is None:
            return
        if getattr(self._serial, "is_open", False):
            self._serial.close()
        self._serial = None

    def _reset_buffers(self) -> None:
        if self._serial is None:
            return
        reset_input = getattr(self._serial, "reset_input_buffer", None)
        reset_output = getattr(self._serial, "reset_output_buffer", None)
        if callable(reset_input):
            reset_input()
        if callable(reset_output):
            reset_output()

    def _write_payload(self, payload: bytes) -> None:
        serial_handle = self._require_connected()
        serial_handle.write(payload)
        flush = getattr(serial_handle, "flush", None)
        if callable(flush):
            flush()

    def _require_connected(self):
        if self._serial is None:
            raise RuntimeError("Serial trigger backend is not connected.")
        return self._serial

    def _encode_code(self, code: int) -> bytes:
        if not isinstance(code, int):
            raise TypeError(f"Trigger code must be int, got {type(code).__name__}.")
        if not 0 <= code <= 255:
            raise ValueError(f"Trigger code must be in 0..255, got {code}.")

        if self.settings.encoding == "byte":
            return bytes([code]) + self.settings.terminator
        if self.settings.encoding == "ascii":
            return f"{code}".encode("ascii") + self.settings.terminator

        raise ValueError(
            "Unsupported serial trigger encoding: "
            f"{self.settings.encoding}. Expected 'byte' or 'ascii'."
        )


@dataclass(frozen=True)
class EyeLinkTriggerSettings:
    host_ip: str = "100.1.1.1"
    dummy_mode: bool = False
    screen_width: int = 1920
    screen_height: int = 1080
    initialize_context: bool = False
    calibration_type: str | None = "HV9"
    message_prefix: str = "TRIGGER"
    pylink_path: str = ""
    label: str = "eyelink"


@dataclass(frozen=True)
class EyeLinkRelaySettings:
    host: str = "127.0.0.1"
    port: int = 18765
    timeout_seconds: float = 3.0
    message_prefix: str = "TRIGGER"
    label: str = "eyelink-relay"


class EyeLinkTriggerBackend(BaseTriggerBackend):
    def __init__(self, settings: EyeLinkTriggerSettings) -> None:
        self.settings = settings
        self._tracker = None

    def connect(self) -> None:
        try:
            pylink = self._import_pylink()
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "PyLink is required for EyeLink trigger mode. "
                "Install the EyeLink Developers Kit / PyLink on the acquisition machine. "
                f"Current Python: {sys.executable}. "
                "If PyLink is installed outside this Python environment, set "
                "EYELINK_PYLINK_PATH in config/local_settings.py to the folder "
                "containing the pylink module."
            ) from exc

        self._tracker = (
            pylink.EyeLink(None)
            if self.settings.dummy_mode
            else pylink.EyeLink(self.settings.host_ip)
        )

        if self.settings.initialize_context:
            self._initialize_tracker_context()

        mode_text = "dummy" if self.settings.dummy_mode else self.settings.host_ip
        print(
            f"[{self.settings.label}] trigger backend connected "
            f"target={mode_text} mode=message_only"
        )

    def send_code(self, code: int, name: str | None = None) -> None:
        tracker = self._require_connected()
        message = self._format_message(name=name, code=code)
        tracker.sendMessage(message)

    def reset(self) -> None:
        return

    def close(self) -> None:
        tracker = self._tracker
        if tracker is None:
            return

        tracker.close()
        self._tracker = None

    def _require_connected(self):
        if self._tracker is None:
            raise RuntimeError("EyeLink trigger backend is not connected.")
        return self._tracker

    def _initialize_tracker_context(self) -> None:
        tracker = self._require_connected()
        width = self.settings.screen_width
        height = self.settings.screen_height
        if width > 0 and height > 0:
            tracker.sendCommand(f"screen_pixel_coords = 0 0 {width - 1} {height - 1}")
            tracker.sendMessage(f"DISPLAY_COORDS 0 0 {width - 1} {height - 1}")
        if self.settings.calibration_type:
            tracker.sendCommand(f"calibration_type = {self.settings.calibration_type}")

    def _format_message(self, name: str | None, code: int) -> str:
        parts = [self.settings.message_prefix]
        if name:
            parts.append(name)
        parts.append(f"code={code}")
        return " ".join(parts)

    def _import_pylink(self):
        for path in self._iter_pylink_paths():
            path_str = str(path)
            if path_str not in sys.path:
                sys.path.insert(0, path_str)
        import pylink  # type: ignore

        return pylink

    def _iter_pylink_paths(self) -> list[Path]:
        raw = self.settings.pylink_path.strip()
        if not raw:
            return []

        candidates: list[Path] = []
        for chunk in raw.split(os.pathsep):
            value = chunk.strip().strip('"')
            if not value:
                continue
            candidates.append(Path(value))
        return candidates


class EyeLinkRelayTriggerBackend(BaseTriggerBackend):
    def __init__(self, settings: EyeLinkRelaySettings) -> None:
        self.settings = settings
        self._socket: socket.socket | None = None
        self._reader = None
        self._writer = None

    def connect(self) -> None:
        self._socket = socket.create_connection(
            (self.settings.host, self.settings.port),
            timeout=self.settings.timeout_seconds,
        )
        self._reader = self._socket.makefile("r", encoding="utf-8", newline="\n")
        self._writer = self._socket.makefile("w", encoding="utf-8", newline="\n")
        response = self._request({"command": "ping"})
        if response.get("result") != "pong":
            raise RuntimeError(
                "EyeLink relay did not respond to ping. "
                f"Received: {response!r}"
            )
        print(
            f"[{self.settings.label}] trigger backend connected "
            f"target={self.settings.host}:{self.settings.port} mode=relay"
        )

    def send_code(self, code: int, name: str | None = None) -> None:
        message = self._format_message(name=name, code=code)
        self._request({"command": "message", "message": message})

    def reset(self) -> None:
        return

    def close(self) -> None:
        try:
            if self._writer is not None:
                self._writer.close()
            if self._reader is not None:
                self._reader.close()
        finally:
            if self._socket is not None:
                self._socket.close()
            self._writer = None
            self._reader = None
            self._socket = None

    def _format_message(self, name: str | None, code: int) -> str:
        parts = [self.settings.message_prefix]
        if name:
            parts.append(name)
        parts.append(f"code={code}")
        return " ".join(parts)

    def _request(self, payload: dict[str, object]) -> dict[str, object]:
        writer = self._require_writer()
        reader = self._require_reader()
        writer.write(json.dumps(payload) + "\n")
        writer.flush()
        response_line = reader.readline()
        if not response_line:
            raise RuntimeError("EyeLink relay connection closed unexpectedly.")
        response = json.loads(response_line)
        if not response.get("ok", False):
            raise RuntimeError(
                "EyeLink relay error: "
                f"{response.get('error', 'unknown error')}"
            )
        return response

    def _require_reader(self):
        if self._reader is None:
            raise RuntimeError("EyeLink relay backend is not connected.")
        return self._reader

    def _require_writer(self):
        if self._writer is None:
            raise RuntimeError("EyeLink relay backend is not connected.")
        return self._writer


class BroadcastTriggerBackend(BaseTriggerBackend):
    def __init__(self, backends: list[BaseTriggerBackend]) -> None:
        self.backends = backends

    def connect(self) -> None:
        connected: list[BaseTriggerBackend] = []
        try:
            for backend in self.backends:
                backend.connect()
                connected.append(backend)
        except Exception:
            for backend in reversed(connected):
                backend.close()
            raise

    def send_code(self, code: int, name: str | None = None) -> None:
        for backend in self.backends:
            backend.send_code(code, name=name)

    def reset(self) -> None:
        for backend in self.backends:
            backend.reset()

    def close(self) -> None:
        for backend in reversed(self.backends):
            backend.close()


@dataclass(frozen=True)
class TriggerRecord:
    timestamp: float
    name: str
    code: int
    width_ms: int


class TriggerClient:
    def __init__(self, backend: BaseTriggerBackend) -> None:
        self.backend = backend
        self.backend.connect()

    def emit(
        self,
        name: str,
        code: int,
        width_ms: int = 10,
    ) -> TriggerRecord:
        timestamp = monotonic()
        self.backend.send_code(code, name=name)
        sleep(width_ms / 1000.0)
        self.backend.reset()
        return TriggerRecord(
            timestamp=timestamp,
            name=name,
            code=code,
            width_ms=width_ms,
        )

    def pulse(self, code: int, width_ms: int = 10) -> TriggerRecord:
        return self.emit(name=f"code_{code}", code=code, width_ms=width_ms)

    def close(self) -> None:
        self.backend.close()


def get_trigger(
    mode: str = "dummy",
    port: Optional[str] = None,
    serial_settings: SerialTriggerSettings | None = None,
    eyelink_settings: EyeLinkTriggerSettings | EyeLinkRelaySettings | None = None,
) -> TriggerClient:
    backends: list[BaseTriggerBackend] = []

    if mode == "dummy":
        backends.append(DummyTriggerBackend())
    elif mode == "serial":
        backends.append(
            SerialTriggerBackend(
                port=port or "",
                settings=serial_settings,
            )
        )
    else:
        raise ValueError(f"Unsupported trigger mode: {mode}")

    if eyelink_settings is not None:
        if isinstance(eyelink_settings, EyeLinkRelaySettings):
            backends.append(EyeLinkRelayTriggerBackend(eyelink_settings))
        else:
            backends.append(EyeLinkTriggerBackend(eyelink_settings))

    if len(backends) == 1:
        return TriggerClient(backends[0])
    return TriggerClient(BroadcastTriggerBackend(backends))
