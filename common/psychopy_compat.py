from __future__ import annotations

import sys


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
