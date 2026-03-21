from __future__ import annotations

import csv
import random
import sys
from dataclasses import dataclass
from pathlib import Path

from common.data_io import ExperimentContext
from common.psychopy_compat import (
    build_window_kwargs,
    configure_macos_psychopy_runtime,
    get_adaptive_text_height,
    get_adaptive_wrap_width,
    get_or_create_visual_window,
    wrap_text_for_display,
)
from config.event_codes import RESTING_STATE
from config.settings import (
    DEFAULT_TRIGGER_WIDTH_MS,
    PSYCHOPY_AUDIO_LIB,
    PSYCHOPY_MONITOR_NAME,
    REST_ALLOW_GUI,
    REST_BACKGROUND_COLOR,
    REST_CYCLE_COUNT,
    REST_EYES_CLOSED_SECONDS,
    REST_EYES_OPEN_SECONDS,
    REST_FONT,
    REST_FULLSCREEN,
    REST_TEXT_COLOR,
    REST_WINDOW_SIZE,
)


@dataclass(frozen=True)
class RestingStateConfig:
    eyes_open_seconds: int = REST_EYES_OPEN_SECONDS
    eyes_closed_seconds: int = REST_EYES_CLOSED_SECONDS
    cycles: int = REST_CYCLE_COUNT
    fullscreen: bool = REST_FULLSCREEN
    allow_gui: bool = REST_ALLOW_GUI
    window_size: tuple[int, int] = REST_WINDOW_SIZE
    background_color: str = REST_BACKGROUND_COLOR
    text_color: str = REST_TEXT_COLOR
    font: str = REST_FONT
    auto_advance: bool = False
    phase_order: tuple[str, str] = ("eyes_open", "eyes_closed")
    randomize_phase_order: bool = False
    show_task_intro: bool = True
    show_phase_intro: bool = True
    show_completion: bool = True
    play_phase_transition_tone: bool = False

    def __post_init__(self) -> None:
        if self.eyes_open_seconds <= 0:
            raise ValueError("eyes_open_seconds must be positive.")
        if self.eyes_closed_seconds <= 0:
            raise ValueError("eyes_closed_seconds must be positive.")
        if self.cycles <= 0:
            raise ValueError("cycles must be positive.")
        if len(self.window_size) != 2 or any(size <= 0 for size in self.window_size):
            raise ValueError("window_size must contain two positive integers.")
        if sorted(self.phase_order) != ["eyes_closed", "eyes_open"]:
            raise ValueError("phase_order must contain eyes_open and eyes_closed exactly once.")


class TaskAborted(RuntimeError):
    pass


def _write_log(output_path: Path, rows: list[dict[str, object]]) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["cycle", "phase", "event_name", "event_code", "timestamp"],
        )
        writer.writeheader()
        writer.writerows(rows)


def _emit_event(
    context: ExperimentContext,
    rows: list[dict[str, object]],
    cycle_index: int,
    phase: str,
    event_name: str,
) -> None:
    code = RESTING_STATE[event_name]
    record = context.trigger.emit(
        name=f"resting_state.{event_name}",
        code=code,
        width_ms=DEFAULT_TRIGGER_WIDTH_MS,
    )
    rows.append(
        {
            "cycle": cycle_index,
            "phase": phase,
            "event_name": event_name,
            "event_code": code,
            "timestamp": f"{record.timestamp:.6f}",
        }
    )


class RestingStateTask:
    def __init__(self, context: ExperimentContext, config: RestingStateConfig) -> None:
        self.context = context
        self.config = config
        self.window = None
        self.core = None
        self.event = None
        self.visual = None
        self.title_stim = None
        self.subtitle_stim = None
        self.detail_stim = None
        self.fixation_stim = None
        self.sound = None
        self.transition_tone = None
        self._tone_warning_printed = False

    def run(self) -> Path:
        output_path = self.context.output_dir / "resting_state_events.csv"
        log_rows: list[dict[str, object]] = []
        task_error: BaseException | None = None

        try:
            self._prepare_psychopy()
            if self.config.show_task_intro:
                self._show_intro()
            _emit_event(self.context, log_rows, 0, "task", "task_start")

            for cycle_index in range(1, self.config.cycles + 1):
                phase_order = self._phase_order_for_cycle(cycle_index)
                for phase_position, phase_name in enumerate(phase_order):
                    if phase_position > 0 and self.config.play_phase_transition_tone:
                        self._play_tone()
                    if self.config.show_phase_intro:
                        self._show_phase_intro(
                            title=self._phase_title(cycle_index, phase_name),
                            subtitle=self._phase_subtitle(phase_name),
                        )
                    _emit_event(
                        self.context,
                        log_rows,
                        cycle_index,
                        phase_name,
                        f"{phase_name}_start",
                    )
                    self._run_phase(
                        seconds=self._phase_seconds(phase_name),
                        show_fixation=phase_name == "eyes_open",
                    )
                    _emit_event(
                        self.context,
                        log_rows,
                        cycle_index,
                        phase_name,
                        f"{phase_name}_end",
                    )

            _emit_event(self.context, log_rows, 0, "task", "task_end")
            if self.config.show_completion:
                self._show_completion()
        except BaseException as exc:
            task_error = exc
        finally:
            _write_log(output_path, log_rows)

        if task_error is not None:
            raise task_error

        return output_path

    def _prepare_psychopy(self) -> None:
        configure_macos_psychopy_runtime()
        try:
            from psychopy import prefs  # type: ignore
            prefs.hardware["audioLib"] = PSYCHOPY_AUDIO_LIB
            from psychopy import core, event, sound, visual  # type: ignore
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "PsychoPy is not installed in the Python interpreter running this task. "
                f"Current interpreter: {sys.executable} | Python {sys.version.split()[0]}."
            ) from exc

        self.core = core
        self.event = event
        self.sound = sound
        self.visual = visual
        self.window = get_or_create_visual_window(
            self.context.psychopy_window,
            visual,
            **build_window_kwargs(
                size=self.config.window_size,
                fullscr=self.config.fullscreen,
                monitor=PSYCHOPY_MONITOR_NAME,
                color=self.config.background_color,
                color_space="named",
                units="height",
                allow_gui=self.config.allow_gui,
            ),
        )
        self.context.psychopy_window = self.window
        title_height = get_adaptive_text_height(self.window, 0.05)
        subtitle_height = get_adaptive_text_height(self.window, 0.03)
        detail_height = get_adaptive_text_height(self.window, 0.028)
        text_wrap_width = get_adaptive_wrap_width(self.window, 1.5)
        self.title_stim = visual.TextStim(
            win=self.window,
            text="",
            font=self.config.font,
            color=self.config.text_color,
            colorSpace="named",
            height=title_height,
            wrapWidth=text_wrap_width,
        )
        self.subtitle_stim = visual.TextStim(
            win=self.window,
            text="",
            font=self.config.font,
            color=self.config.text_color,
            colorSpace="named",
            height=subtitle_height,
            pos=(0, -0.26),
            wrapWidth=text_wrap_width,
        )
        self.detail_stim = visual.TextStim(
            win=self.window,
            text="",
            font=self.config.font,
            color=self.config.text_color,
            colorSpace="named",
            height=detail_height,
            pos=(0, -0.38),
            wrapWidth=text_wrap_width,
        )
        self.fixation_stim = visual.TextStim(
            win=self.window,
            text="+",
            font=self.config.font,
            color=self.config.text_color,
            colorSpace="named",
            height=0.08,
        )
        self._prepare_transition_tone()

    def _show_intro(self) -> None:
        self._wait_for_continue(
            title="静息态引导",
            subtitle=(
                f"本任务包含 {self.config.cycles} 轮静息记录。\n"
                f"每轮包括睁眼静息 {self.config.eyes_open_seconds} 秒，"
                f"以及闭眼静息 {self.config.eyes_closed_seconds} 秒。"
            ),
            detail=(
                "睁眼阶段请注视中央十字，闭眼阶段请保持放松和安静。\n"
                "如需中止，按 Esc。按空格开始。"
            ),
        )

    def _show_phase_intro(self, title: str, subtitle: str) -> None:
        self._wait_for_continue(
            title=title,
            subtitle=subtitle,
            detail="实验员确认后按空格开始该阶段。",
        )

    def _show_completion(self) -> None:
        self._wait_for_continue(
            title="静息态结束",
            subtitle="请被试睁眼，保持放松，等待下一任务。",
            detail="按空格结束。",
        )

    def _wait_for_continue(self, title: str, subtitle: str, detail: str) -> None:
        self.event.clearEvents()
        while True:
            if self.config.auto_advance:
                return

            keys = self.event.getKeys(keyList=["space", "return", "escape"])
            if "escape" in keys:
                raise TaskAborted("Experiment aborted by user.")
            if "space" in keys or "return" in keys:
                return

            self._draw_text_page(title, subtitle, detail)
            self.window.flip()

    def _phase_order_for_cycle(self, cycle_index: int) -> tuple[str, str]:
        if not self.config.randomize_phase_order:
            return self.config.phase_order

        cycle_random = random.Random(
            f"{self.context.participant_id}-{self.context.session_id}-{cycle_index}"
        )
        phase_order = list(self.config.phase_order)
        cycle_random.shuffle(phase_order)
        return tuple(phase_order)

    def _phase_seconds(self, phase_name: str) -> int:
        return (
            self.config.eyes_open_seconds
            if phase_name == "eyes_open"
            else self.config.eyes_closed_seconds
        )

    def _phase_title(self, cycle_index: int, phase_name: str) -> str:
        return (
            f"第 {cycle_index} 轮：睁眼静息"
            if phase_name == "eyes_open"
            else f"第 {cycle_index} 轮：闭眼静息"
        )

    def _phase_subtitle(self, phase_name: str) -> str:
        if phase_name == "eyes_open":
            return (
                "请睁眼注视中央十字，保持放松，尽量减少眨眼和身体动作。\n"
                f"本阶段持续 {self.config.eyes_open_seconds} 秒。"
            )
        return (
            "请闭上双眼，保持放松和安静，尽量不要移动。\n"
            f"本阶段持续 {self.config.eyes_closed_seconds} 秒。"
        )

    def _play_tone(self) -> None:
        if self._play_psychopy_tone():
            return
        if self._play_windows_fallback_tone():
            return
        self._warn_tone_unavailable()

    def _prepare_transition_tone(self) -> None:
        self.transition_tone = None
        if self.sound is None:
            return
        try:
            cue = self.sound.Sound(value=880, secs=0.2, stereo=True)
            set_volume = getattr(cue, "setVolume", None)
            if callable(set_volume):
                set_volume(1.0)
            self.transition_tone = cue
        except Exception:
            self.transition_tone = None

    def _play_psychopy_tone(self) -> bool:
        cue = self.transition_tone
        if cue is None:
            self._prepare_transition_tone()
            cue = self.transition_tone
        if cue is None:
            return False
        try:
            stop = getattr(cue, "stop", None)
            if callable(stop):
                stop()
            cue.play()
            self.core.wait(0.25)
            return True
        except Exception:
            return False

    def _play_windows_fallback_tone(self) -> bool:
        if sys.platform != "win32":
            return False
        try:
            import winsound

            winsound.Beep(880, 200)
            return True
        except Exception:
            try:
                import winsound

                winsound.MessageBeep()
                return True
            except Exception:
                return False

    def _warn_tone_unavailable(self) -> None:
        if self._tone_warning_printed:
            return
        self._tone_warning_printed = True
        print(
            "Warning: resting-state transition tone could not be played. "
            f"Configured audio backend={PSYCHOPY_AUDIO_LIB!r}."
        )

    def _run_phase(self, seconds: int, show_fixation: bool) -> None:
        phase_clock = self.core.Clock()
        self.event.clearEvents()
        while phase_clock.getTime() < seconds:
            self._ensure_escape_not_pressed()
            if show_fixation:
                self.fixation_stim.draw()
            self.window.flip()

    def _draw_text_page(self, title: str, subtitle: str, detail: str) -> None:
        self.title_stim.text = self._wrap_for_stim(self.title_stim, title)
        self.subtitle_stim.text = self._wrap_for_stim(self.subtitle_stim, subtitle)
        self.detail_stim.text = self._wrap_for_stim(self.detail_stim, detail)
        self.title_stim.draw()
        self.subtitle_stim.draw()
        self.detail_stim.draw()

    def _wrap_for_stim(self, stim, text: str) -> str:
        return wrap_text_for_display(
            self.window,
            text,
            text_height=float(stim.height),
            base_wrap_width=float(stim.wrapWidth),
        )

    def _ensure_escape_not_pressed(self) -> None:
        if "escape" in self.event.getKeys(keyList=["escape"]):
            raise TaskAborted("Experiment aborted by user.")


def run(
    context: ExperimentContext,
    config: RestingStateConfig | None = None,
) -> Path:
    config = config or RestingStateConfig()
    task = RestingStateTask(context=context, config=config)
    return task.run()
