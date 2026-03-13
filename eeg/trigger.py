from __future__ import annotations

from dataclasses import dataclass
from time import monotonic, sleep
from typing import Optional


class BaseTriggerBackend:
    def connect(self) -> None:
        pass

    def send_code(self, code: int) -> None:
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

    def send_code(self, code: int) -> None:
        print(f"[{self.label}] trigger_code={code}")

    def reset(self) -> None:
        print(f"[{self.label}] trigger_reset")


class SerialTriggerBackend(BaseTriggerBackend):
    def __init__(self, port: str) -> None:
        self.port = port
        raise NotImplementedError(
            "Implement the real NeusenW32 communication backend in this class."
        )

    def send_code(self, code: int) -> None:
        raise NotImplementedError("Serial trigger sending is not implemented yet.")


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
        self.backend.send_code(code)
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


def get_trigger(mode: str = "dummy", port: Optional[str] = None) -> TriggerClient:
    if mode == "dummy":
        return TriggerClient(DummyTriggerBackend())
    if mode == "serial":
        return TriggerClient(SerialTriggerBackend(port=port or ""))
    raise ValueError(f"Unsupported trigger mode: {mode}")
