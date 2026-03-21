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


def get_window_aspect_ratio(window, fallback: float = 1.6) -> float:
    try:
        width, height = getattr(window, "size", (0, 0))
        width = float(width)
        height = float(height)
    except Exception:
        return fallback

    if width <= 0 or height <= 0:
        return fallback
    return width / height


def get_adaptive_text_height(
    window,
    base_height: float,
    *,
    reference_aspect: float = 1.6,
    min_scale: float = 0.78,
) -> float:
    aspect = get_window_aspect_ratio(window, fallback=reference_aspect)
    scale = aspect / reference_aspect
    scale = min(1.0, max(min_scale, scale))
    return base_height * scale


def get_adaptive_wrap_width(
    window,
    base_wrap_width: float,
    *,
    horizontal_margin_ratio: float = 0.88,
    min_wrap_width: float = 0.9,
) -> float:
    aspect = get_window_aspect_ratio(window)
    available_width = aspect * horizontal_margin_ratio
    return min(base_wrap_width, max(min_wrap_width, available_width))


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


def get_or_create_visual_window(existing_window, visual, **kwargs):
    window = existing_window
    if _window_needs_recreation(window, **kwargs):
        safe_close_window(window)
        window = None

    if window is None:
        window = create_visual_window(visual, **kwargs)
    else:
        _apply_window_settings(window, **kwargs)

    try:
        window.clearAutoDraw()
    except Exception:
        pass

    try:
        window.flip()
    except Exception:
        pass

    return window


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


def _window_needs_recreation(window, **kwargs) -> bool:
    if window is None:
        return True

    requested_fullscr = bool(kwargs.get("fullscr", False))
    current_fullscr = bool(
        getattr(window, "fullscr", getattr(window, "_isFullScr", False))
    )
    if current_fullscr != requested_fullscr:
        return True

    requested_size = tuple(int(value) for value in kwargs.get("size", ()))
    if not requested_fullscr and requested_size:
        current_size = tuple(int(value) for value in getattr(window, "size", ()))
        if current_size != requested_size:
            return True

    return False


def _apply_window_settings(window, **kwargs) -> None:
    if "units" in kwargs:
        window.units = kwargs["units"]
    if "colorSpace" in kwargs:
        window.colorSpace = kwargs["colorSpace"]
    if "color" in kwargs:
        window.color = kwargs["color"]
    if hasattr(window, "backgroundImage"):
        window.backgroundImage = ""
    if hasattr(window, "backgroundFit"):
        window.backgroundFit = "none"
