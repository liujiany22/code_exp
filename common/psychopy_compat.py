from __future__ import annotations

import gc
import sys
import time
import unicodedata


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


def wrap_text_for_display(
    window,
    text: str,
    *,
    text_height: float,
    base_wrap_width: float,
    horizontal_margin_ratio: float = 0.82,
    min_line_units: float = 12.0,
) -> str:
    if not isinstance(text, str) or not text:
        return text

    wrap_width = get_adaptive_wrap_width(
        window,
        base_wrap_width,
        horizontal_margin_ratio=horizontal_margin_ratio,
    )
    line_unit_limit = max(min_line_units, (wrap_width / max(text_height, 1e-6)) * 0.92)

    wrapped_lines: list[str] = []
    for raw_line in text.splitlines():
        if not raw_line.strip():
            wrapped_lines.append("")
            continue
        wrapped_lines.extend(_wrap_text_line(raw_line, line_unit_limit))
    return "\n".join(wrapped_lines)


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


def _wrap_text_line(text: str, line_unit_limit: float) -> list[str]:
    if _measure_text_units(text) <= line_unit_limit:
        return [text]

    lines: list[str] = []
    remaining = text.strip()
    while remaining:
        split_index = _find_wrap_index(remaining, line_unit_limit)
        current = remaining[:split_index].rstrip()
        if not current:
            current = remaining[:1]
            split_index = 1
        lines.append(current)
        remaining = remaining[split_index:].lstrip()
    return lines


def _find_wrap_index(text: str, line_unit_limit: float) -> int:
    total_units = 0.0
    last_break_index = -1

    for index, char in enumerate(text, start=1):
        total_units += _char_display_units(char)
        if _is_breakable_character(char):
            last_break_index = index
        if total_units > line_unit_limit:
            if last_break_index > 0:
                return last_break_index
            return max(1, index - 1)

    return len(text)


def _measure_text_units(text: str) -> float:
    return sum(_char_display_units(char) for char in text)


def _char_display_units(char: str) -> float:
    if char.isspace():
        return 0.35
    east_asian = unicodedata.east_asian_width(char)
    if east_asian in {"W", "F"}:
        return 1.0
    if east_asian == "A":
        return 0.8
    if char.isascii() and (char.isalpha() or char.isdigit()):
        return 0.62
    if char in "，。、；：,.!?！？":
        return 0.5
    return 0.7


def _is_breakable_character(char: str) -> bool:
    return char.isspace() or char in "，。、；：,.!?！？)]】）>}》」』"
