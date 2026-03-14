from __future__ import annotations

import argparse
import json
from pathlib import Path
import socketserver
import sys
from typing import Any, Dict, Optional

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.settings import (  # noqa: E402
    EYELINK_CALIBRATION_TYPE,
    EYELINK_DUMMY_MODE,
    EYELINK_HOST_IP,
    EYELINK_INITIALIZE_CONTEXT,
    EYELINK_PYLINK_PATH,
    EYELINK_RELAY_HOST,
    EYELINK_RELAY_PORT,
    EYELINK_SCREEN_HEIGHT,
    EYELINK_SCREEN_WIDTH,
)


class EyeLinkRelayState:
    def __init__(
        self,
        host_ip: str,
        dummy_mode: bool,
        screen_width: int,
        screen_height: int,
        initialize_context: bool,
        calibration_type: Optional[str],
        pylink_path: str,
    ) -> None:
        self.host_ip = host_ip
        self.dummy_mode = dummy_mode
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.initialize_context = initialize_context
        self.calibration_type = calibration_type
        self.pylink_path = pylink_path
        self.pylink = None
        self.tracker = None

    def connect(self) -> None:
        self.pylink = self._import_pylink()
        self.tracker = (
            self.pylink.EyeLink(None)
            if self.dummy_mode
            else self.pylink.EyeLink(self.host_ip)
        )
        if self.initialize_context:
            self._initialize_tracker_context()
        mode_text = "dummy" if self.dummy_mode else self.host_ip
        print(
            "[eyelink-relay-server] connected "
            "target={target} initialize_context={init}".format(
                target=mode_text,
                init=int(self.initialize_context),
            )
        )

    def send_message(self, message: str) -> None:
        tracker = self._require_tracker()
        tracker.sendMessage(message)

    def close(self) -> None:
        if self.tracker is None:
            return
        self.tracker.close()
        self.tracker = None

    def _require_tracker(self):
        if self.tracker is None:
            raise RuntimeError("EyeLink relay server is not connected.")
        return self.tracker

    def _initialize_tracker_context(self) -> None:
        tracker = self._require_tracker()
        width = self.screen_width
        height = self.screen_height
        if width > 0 and height > 0:
            tracker.sendCommand(
                "screen_pixel_coords = 0 0 {x} {y}".format(
                    x=width - 1,
                    y=height - 1,
                )
            )
            tracker.sendMessage(
                "DISPLAY_COORDS 0 0 {x} {y}".format(
                    x=width - 1,
                    y=height - 1,
                )
            )
        if self.calibration_type:
            tracker.sendCommand(
                "calibration_type = {value}".format(
                    value=self.calibration_type,
                )
            )

    def _import_pylink(self):
        if self.pylink_path:
            for chunk in self.pylink_path.split(";"):
                value = chunk.strip().strip('"')
                if value and value not in sys.path:
                    sys.path.insert(0, value)
        import pylink  # type: ignore

        return pylink


class EyeLinkRelayTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, server_address, handler_class, state: EyeLinkRelayState):
        super().__init__(server_address, handler_class)
        self.state = state


class EyeLinkRelayHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        while True:
            raw = self.rfile.readline()
            if not raw:
                return
            try:
                payload = json.loads(raw.decode("utf-8"))
                response = self.server_dispatch(payload)
            except Exception as exc:
                response = {"ok": False, "error": str(exc)}
            self.wfile.write((json.dumps(response) + "\n").encode("utf-8"))
            self.wfile.flush()

    def server_dispatch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        command = payload.get("command")
        server = self.server
        assert isinstance(server, EyeLinkRelayTCPServer)

        if command == "ping":
            return {"ok": True, "result": "pong"}
        if command == "message":
            message = str(payload.get("message", ""))
            if not message:
                raise RuntimeError("Missing relay message payload.")
            server.state.send_message(message)
            return {"ok": True}

        raise RuntimeError("Unsupported relay command: {cmd}".format(cmd=command))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the EyeLink relay server under Python 3.9.",
    )
    parser.add_argument("--relay-host", default=EYELINK_RELAY_HOST)
    parser.add_argument("--relay-port", type=int, default=EYELINK_RELAY_PORT)
    parser.add_argument("--eyelink-host-ip", default=EYELINK_HOST_IP)
    parser.add_argument(
        "--dummy-mode",
        action="store_true",
        default=EYELINK_DUMMY_MODE,
    )
    parser.add_argument(
        "--initialize-context",
        action="store_true",
        default=EYELINK_INITIALIZE_CONTEXT,
    )
    parser.add_argument("--screen-width", type=int, default=EYELINK_SCREEN_WIDTH)
    parser.add_argument("--screen-height", type=int, default=EYELINK_SCREEN_HEIGHT)
    parser.add_argument(
        "--calibration-type",
        default=EYELINK_CALIBRATION_TYPE,
    )
    parser.add_argument(
        "--pylink-path",
        default=EYELINK_PYLINK_PATH,
        help="Optional folder containing the pylink module.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    state = EyeLinkRelayState(
        host_ip=args.eyelink_host_ip,
        dummy_mode=args.dummy_mode,
        screen_width=args.screen_width,
        screen_height=args.screen_height,
        initialize_context=args.initialize_context,
        calibration_type=args.calibration_type,
        pylink_path=args.pylink_path,
    )
    state.connect()

    server = EyeLinkRelayTCPServer(
        (args.relay_host, args.relay_port),
        EyeLinkRelayHandler,
        state,
    )
    print(
        "[eyelink-relay-server] listening "
        "on {host}:{port}".format(
            host=args.relay_host,
            port=args.relay_port,
        )
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        state.close()


if __name__ == "__main__":
    main()
