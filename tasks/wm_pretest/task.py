from __future__ import annotations

import csv
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from common.data_io import ExperimentContext
from common.external_task import ExternalTaskSpec, load_module_from_path
from common.ui import show_message, wait_for_continue
from config.event_codes import WM_PRETEST
from config.settings import (
    CORSI_BLOCKS_SCRIPT,
    DEFAULT_TRIGGER_WIDTH_MS,
    DIGIT_SPAN_SCRIPT,
    PSYCHOPY_AUDIO_LIB,
    PSYCHOPY_MIN_VERSION,
    WM_PRETEST_FRAME_RATE_FALLBACK,
    WM_PRETEST_FORCE_MOUSE_VISIBLE,
    WM_PRETEST_KEYBOARD_BACKEND,
    WM_PRETEST_MACOS_WINDOWED,
)


@dataclass(frozen=True)
class WMPretestConfig:
    auto_advance: bool = False


TASK_SPECS = [
    ExternalTaskSpec(
        name="digit_span",
        script_path=DIGIT_SPAN_SCRIPT,
        task_code_start=WM_PRETEST["digit_span_start"],
        task_code_end=WM_PRETEST["digit_span_end"],
    ),
    ExternalTaskSpec(
        name="corsi_blocks",
        script_path=CORSI_BLOCKS_SCRIPT,
        task_code_start=WM_PRETEST["corsi_start"],
        task_code_end=WM_PRETEST["corsi_end"],
    ),
]


def _check_environment() -> tuple[str, str]:
    try:
        import psychopy  # type: ignore
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "PsychoPy is not installed in the Python interpreter running this task. "
            f"Current interpreter: {sys.executable} | Python {sys.version.split()[0]}. "
            "Install with `python -m pip install psychopy` using this same interpreter, "
            "or run the task with the PsychoPy bundled Python."
        ) from exc

    version = getattr(psychopy, "__version__", "unknown")
    return version, sys.executable


def _prepare_exp_info(module: object, context: ExperimentContext) -> dict[str, str]:
    exp_info = dict(getattr(module, "expInfo", {}))
    exp_info["participant"] = context.participant_id
    exp_info["session"] = context.session_id
    return exp_info


def _emit_boundary(context: ExperimentContext, event_name: str, event_code: int) -> None:
    context.trigger.emit(
        name=f"wm_pretest.{event_name}",
        code=event_code,
        width_ms=DEFAULT_TRIGGER_WIDTH_MS,
    )


def _install_keyboard_compatibility(module: object) -> None:
    """
    Replace the generated ioHub device setup with a lightweight keyboard setup.

    The exported reference tasks only need standard keyboard access. On some
    macOS environments ioHub fails to start, so we pre-create the devices with
    a simpler backend and leave `deviceManager.ioServer` as `None`.
    """
    device_manager = getattr(module, "deviceManager")

    def setup_devices_without_iohub(expInfo, thisExp, win):
        device_manager.ioServer = None

        if device_manager.getDevice("defaultKeyboard") is None:
            device_manager.addDevice(
                deviceClass="keyboard",
                deviceName="defaultKeyboard",
                backend=WM_PRETEST_KEYBOARD_BACKEND,
            )

        if hasattr(module, "expName") and getattr(module, "expName") == "corsi_blocks":
            if device_manager.getDevice("key_resp") is None:
                device_manager.addDevice(
                    deviceClass="keyboard",
                    deviceName="key_resp",
                    backend=WM_PRETEST_KEYBOARD_BACKEND,
                )

        return True

    module.setupDevices = setup_devices_without_iohub


def _configure_macos_runtime() -> None:
    if sys.platform != "darwin":
        return

    try:
        import pyglet  # type: ignore
    except ModuleNotFoundError:
        return

    # Pyglet documents an alternative event loop for macOS because the
    # standard loop can randomly break or crash, especially on ARM Macs.
    pyglet.options["osx_alt_loop"] = True


def _install_window_compatibility(module: object) -> None:
    original_setup_window = module.setupWindow
    original_get_frame_rate = getattr(module.visual.Window, "getActualFrameRate", None)

    def force_mouse_visible(created_window) -> None:
        if not WM_PRETEST_FORCE_MOUSE_VISIBLE:
            return

        try:
            created_window.mouseVisible = True
        except Exception:
            pass

        win_handle = getattr(created_window, "winHandle", None)
        if win_handle is None:
            return

        for method_name in ("set_mouse_visible", "setMouseVisible"):
            method = getattr(win_handle, method_name, None)
            if callable(method):
                try:
                    method(True)
                except Exception:
                    pass

        exclusive_mouse = getattr(win_handle, "set_exclusive_mouse", None)
        if callable(exclusive_mouse):
            try:
                exclusive_mouse(False)
            except Exception:
                pass

    def safe_get_frame_rate(self, *args, **kwargs):
        return WM_PRETEST_FRAME_RATE_FALLBACK

    def setup_window_with_defaults(expInfo=None, win=None):
        if sys.platform == "darwin" and win is None and WM_PRETEST_MACOS_WINDOWED:
            module._fullScr = False

        created_window = original_setup_window(expInfo=expInfo, win=win)
        force_mouse_visible(created_window)

        if sys.platform == "darwin":
            created_window._monitorFrameRate = WM_PRETEST_FRAME_RATE_FALLBACK

            # Some macOS environments raise Objective-C bridge errors when PsychoPy
            # tries to activate the window explicitly.
            try:
                created_window.winHandle.activate = lambda *args, **kwargs: None
            except Exception:
                pass

        return created_window

    if sys.platform == "darwin" and original_get_frame_rate is not None:
        module.visual.Window.getActualFrameRate = safe_get_frame_rate

    module.setupWindow = setup_window_with_defaults


def _write_manifest(output_path: Path, rows: list[dict[str, str]]) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["task_name", "status", "script_path", "output_dir"],
        )
        writer.writeheader()
        writer.writerows(rows)


def _run_external_psychopy_task(
    context: ExperimentContext,
    spec: ExternalTaskSpec,
) -> dict[str, str]:
    module_name = f"wm_pretest_{spec.name}"
    task_output_dir = context.output_dir / "wm_pretest" / spec.name
    task_output_dir.mkdir(parents=True, exist_ok=True)

    _emit_boundary(context, f"{spec.name}_start", spec.task_code_start)
    _configure_macos_runtime()
    module = load_module_from_path(module_name=module_name, script_path=spec.script_path)
    _install_keyboard_compatibility(module)
    _install_window_compatibility(module)
    exp_info = _prepare_exp_info(module, context)

    # Match the generated scripts' expectation for the PTB audio backend when present.
    os.environ.setdefault("PSYCHOPY_AUDIO_LIB", PSYCHOPY_AUDIO_LIB)

    this_exp = None
    win = None
    status = "completed"

    try:
        # The exported PsychoPy scripts concatenate `dataDir + os.sep + filename`,
        # so pass a plain string for compatibility with those generated files.
        this_exp = module.setupData(expInfo=exp_info, dataDir=os.fspath(task_output_dir))
        module.setupLogging(filename=this_exp.dataFileName)
        win = module.setupWindow(expInfo=exp_info)
        module.setupDevices(expInfo=exp_info, thisExp=this_exp, win=win)
        module.run(
            expInfo=exp_info,
            thisExp=this_exp,
            win=win,
            globalClock="float",
        )
    except BaseException:
        status = "failed"
        raise
    finally:
        if this_exp is not None:
            module.saveData(thisExp=this_exp)
            if hasattr(module, "endExperiment"):
                module.endExperiment(thisExp=this_exp, win=win)
            this_exp.abort()
        if win is not None:
            win.close()
        _emit_boundary(context, f"{spec.name}_end", spec.task_code_end)

    return {
        "task_name": spec.name,
        "status": status,
        "script_path": str(spec.script_path),
        "output_dir": str(task_output_dir),
    }


def run(
    context: ExperimentContext,
    config: WMPretestConfig | None = None,
) -> Path:
    config = config or WMPretestConfig()
    psychopy_version, interpreter_path = _check_environment()

    show_message("Working Memory Pretest")
    show_message(
        f"PsychoPy version: {psychopy_version} "
        f"(recommended: {PSYCHOPY_MIN_VERSION})"
    )
    show_message(f"Python interpreter: {interpreter_path}")
    wait_for_continue(
        "The task will run digit span first, then Corsi blocks.",
        auto_advance=config.auto_advance,
    )

    _emit_boundary(context, "task_start", WM_PRETEST["task_start"])
    manifest_rows: list[dict[str, str]] = []

    try:
        for spec in TASK_SPECS:
            show_message(f"Launching {spec.name} interface...")
            manifest_rows.append(_run_external_psychopy_task(context, spec))
    finally:
        _emit_boundary(context, "task_end", WM_PRETEST["task_end"])

    manifest_path = context.output_dir / "wm_pretest_manifest.csv"
    _write_manifest(manifest_path, manifest_rows)
    show_message(f"Working memory pretest manifest saved to: {manifest_path}")
    return manifest_path
