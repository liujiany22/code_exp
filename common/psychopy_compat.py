from __future__ import annotations

import gc
import sys
import time


def configure_macos_psychopy_runtime() -> None:
    if sys.platform != "darwin":
        return

    try:
        import pyglet  # type: ignore
    except ModuleNotFoundError:
        return

    # Pyglet recommends the alternate event loop on macOS.
    pyglet.options["osx_alt_loop"] = True

    try:
        from pyglet.window.cocoa import CocoaWindow  # type: ignore
    except Exception:
        return

    if getattr(CocoaWindow.dispatch_events, "_code_exp_safe_patch", False):
        return

    original_dispatch_events = CocoaWindow.dispatch_events

    def safe_dispatch_events(self):
        try:
            return original_dispatch_events(self)
        except AttributeError as exc:
            message = str(exc)
            if "__NSSingleObjectArrayI" in message and "attribute b'type'" in message:
                return None
            raise

    safe_dispatch_events._code_exp_safe_patch = True  # type: ignore[attr-defined]
    CocoaWindow.dispatch_events = safe_dispatch_events


def get_primary_screen_size() -> tuple[int, int] | None:
    try:
        import pyglet  # type: ignore
    except ModuleNotFoundError:
        return None

    try:
        if hasattr(pyglet, "display"):
            display = pyglet.display.get_display()
        else:
            from pyglet.canvas import Display  # type: ignore

            display = Display()
        screen = display.get_default_screen()
        return int(screen.width), int(screen.height)
    except Exception:
        return None


def build_window_kwargs(
    *,
    size: tuple[int, int],
    fullscr: bool,
    monitor: str,
    color: str,
    color_space: str,
    units: str,
    allow_gui: bool,
) -> dict[str, object]:
    resolved_size = get_primary_screen_size() if fullscr else size
    if resolved_size is None:
        resolved_size = size

    kwargs: dict[str, object] = {
        "size": resolved_size,
        "fullscr": fullscr,
        "monitor": monitor,
        "color": color,
        "colorSpace": color_space,
        "units": units,
        "allowGUI": allow_gui,
    }
    return kwargs


def create_visual_window(visual, **kwargs):
    attempts = 3 if sys.platform == "darwin" else 1
    last_error = None

    for attempt in range(attempts):
        try:
            return visual.Window(**kwargs)
        except AttributeError as exc:
            if not _is_macos_objc_window_error(exc) or attempt == attempts - 1:
                raise
            last_error = exc
            gc.collect()
            time.sleep(0.1)

    if last_error is not None:
        raise last_error
    raise RuntimeError("Unable to create PsychoPy window.")


def safe_close_window(window) -> None:
    if window is None:
        return

    try:
        window.close()
    except AttributeError as exc:
        if "'NoneType' object has no attribute 'close'" in str(exc):
            return
        raise


def _is_macos_objc_window_error(exc: AttributeError) -> bool:
    if sys.platform != "darwin":
        return False

    message = str(exc)
    return "ObjCInstance" in message and "has no attribute b'" in message
