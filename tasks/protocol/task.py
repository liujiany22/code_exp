from __future__ import annotations

import csv
import random
import re
import sys
from datetime import datetime
from dataclasses import asdict, dataclass
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
from config.settings import (
    LEARNING_CYCLE_PROTOCOL_TRIALS_FILE,
    LEARNING_CYCLE_QUESTIONNAIRE_DIR,
    PSYCHOPY_MONITOR_NAME,
    REST_ALLOW_GUI,
    REST_BACKGROUND_COLOR,
    REST_FONT,
    REST_FULLSCREEN,
    REST_TEXT_COLOR,
    REST_WINDOW_SIZE,
)
from tasks.learning_cycle.task import LearningCycleConfig, run as run_learning_cycle
from tasks.mental_arithmetic.task import MentalArithmeticConfig, run as run_mental_arithmetic
from tasks.resting_state.task import RestingStateConfig, run as run_resting_state
from tasks.wm_pretest.task import WMPretestConfig, run as run_wm_pretest

LEARNING_CYCLE_INTRO = (
    "接下来进入视频学习任务。\n"
    "当前版本先进行傅立叶变换这一组。\n"
    "整个流程包含前测、视频播放和后测三个部分。"
)

PRACTICE_LEARNING_DEMO = (
    "视频学习练习演示接口已预留。\n"
    "当前练习流程暂不播放真实视频材料，后续可在这里接入正式演示。"
)

BREAK_INTRO = (
    "练习阶段结束。\n"
    "请短暂休息，调整状态后进入正式实验。"
)

PRACTICE_HELP_FOOTER = "练习过程中若有任何疑问，请随时向主试问询"
TEST_STAGE_CHOICES = (
    "resting_state",
    "digit_span",
    "corsi_blocks",
    "mental_arithmetic",
    "learning_cycle",
)
TEST_STAGE_LABELS = {
    "resting_state": "静息态",
    "digit_span": "数字记忆",
    "corsi_blocks": "柯西方块",
    "mental_arithmetic": "心算任务",
    "learning_cycle": "视频学习任务",
}


@dataclass(frozen=True)
class ProtocolConfig:
    test_mode: bool = False
    test_stage: str | None = None
    auto_advance: bool = False
    fullscreen: bool = REST_FULLSCREEN
    allow_gui: bool = REST_ALLOW_GUI
    window_size: tuple[int, int] = REST_WINDOW_SIZE
    background_color: str = REST_BACKGROUND_COLOR
    text_color: str = REST_TEXT_COLOR
    font: str = REST_FONT


@dataclass(frozen=True)
class StageLogRow:
    StepNumber: int
    StageName: str
    Timestamp: str
    Detail: str


class ProtocolTask:
    def __init__(self, context: ExperimentContext, config: ProtocolConfig):
        self.context = context
        self.config = config
        self.stage_rows: list[dict[str, str]] = []
        self.window = None
        self.core = None
        self.event = None
        self.visual = None

    def run(self) -> Path:
        if self.config.test_mode:
            final_step_number = self._run_test_mode_segment()
        else:
            self._run_practice_segment()
            final_step_number = self._run_formal_segment()
        self._show_stage(
            step_number=final_step_number,
            stage_name="实验结束",
            title="实验结束",
            subtitle="本次实验流程已完成。",
            detail="感谢参与。按空格结束。",
        )
        return self._write_stage_log()

    def _run_practice_segment(self) -> None:
        self._show_practice_stage(
            step_number=1,
            stage_name="练习开始",
            title="练习环节",
            subtitle="为了帮助您更好地熟悉实验流程，接下来是练习环节。",
            detail="按空格进入练习。",
        )
        if not self._show_practice_stage(
            step_number=2,
            stage_name="静息引导语-练习",
            title="静息练习",
            subtitle=self._rest_intro_text(first_phase="eyes_open", seconds=3),
            detail="准备好后按空格开始静息练习。",
        ):
            run_resting_state(
                self.context,
                config=RestingStateConfig(
                    eyes_open_seconds=3,
                    eyes_closed_seconds=3,
                    cycles=1,
                    auto_advance=self.config.auto_advance,
                    phase_order=("eyes_open", "eyes_closed"),
                    randomize_phase_order=False,
                    show_task_intro=False,
                    show_phase_intro=False,
                    show_completion=False,
                    play_phase_transition_tone=True,
                ),
            )
        run_wm_pretest(
            self.context,
            config=WMPretestConfig(
                auto_advance=self.config.auto_advance,
                pilot_mode=True,
                task_timeout_seconds=12.0,
                selected_task_names=("digit_span",),
                show_wrapper_intro=False,
                show_wrapper_completion=False,
            ),
        )
        run_wm_pretest(
            self.context,
            config=WMPretestConfig(
                auto_advance=self.config.auto_advance,
                pilot_mode=True,
                task_timeout_seconds=12.0,
                selected_task_names=("corsi_blocks",),
                show_wrapper_intro=False,
                show_wrapper_completion=False,
            ),
        )
        if not self._show_practice_stage(
            step_number=8,
            stage_name="心算介绍-练习",
            title="心算练习",
            subtitle=(
                "在这个任务中，你将看到一道由黑色数字组成的加法题。\n"
                "请先在心中完成计算。\n"
                "随后中央会短暂出现“+”。\n"
                "当出现蓝色数字时，请判断它是否等于正确答案。"
            ),
            detail="如果蓝色数字等于正确答案，请按鼠标左键；如果不等，请按鼠标右键。按空格进入练习。",
        ):
            run_mental_arithmetic(
                self.context,
                config=MentalArithmeticConfig(
                    auto_advance=self.config.auto_advance,
                    show_instructions=False,
                    show_completion=False,
                    fixation_seconds=2.0,
                    pre_response_blank_seconds=0.2,
                    response_timeout_seconds=3.0,
                    inter_trial_seconds=0.2,
                    block_count=1,
                    trials_per_block=1,
                    block_rest_seconds=0.0,
                    trial_counts={"QE": 1, "QM": 0, "QH": 0},
                ),
            )
        self._show_practice_stage(
            step_number=10,
            stage_name="视频学习介绍-练习",
            title="视频学习练习",
            subtitle=LEARNING_CYCLE_INTRO,
            detail="练习阶段仅展示流程说明。按空格继续。",
        )
        self._show_practice_stage(
            step_number=11,
            stage_name="视频学习演示-练习",
            title="视频学习练习",
            subtitle=PRACTICE_LEARNING_DEMO,
            detail="按空格进入下一步。",
        )
        self._show_practice_stage(
            step_number=12,
            stage_name="休息引导语",
            title="短暂休息",
            subtitle=BREAK_INTRO,
            detail="按空格进入正式实验。",
        )

    def _run_formal_segment(self) -> int:
        self._run_formal_opening(step_number=13, test_mode=False, stage_name=None)
        self._run_formal_rest_stage(step_number=14, test_mode=False)
        self._run_formal_digit_span_stage(test_mode=False)
        self._run_formal_corsi_stage(test_mode=False)
        self._run_formal_mental_arithmetic_stage(step_number=18, test_mode=False)
        self._run_formal_learning_cycle_stage(step_number=19, test_mode=False)
        return 21

    def _run_test_mode_segment(self) -> int:
        selected_stage = self.config.test_stage
        self._run_formal_opening(step_number=1, test_mode=True, stage_name=selected_stage)
        if selected_stage is None:
            self._run_formal_rest_stage(step_number=2, test_mode=True)
            self._run_formal_digit_span_stage(test_mode=True)
            self._run_formal_corsi_stage(test_mode=True)
            self._run_formal_mental_arithmetic_stage(step_number=5, test_mode=True)
            self._run_formal_learning_cycle_stage(step_number=6, test_mode=True)
            return 7

        stage_runner_map = {
            "resting_state": lambda: self._run_formal_rest_stage(step_number=2, test_mode=True),
            "digit_span": lambda: self._run_formal_digit_span_stage(test_mode=True),
            "corsi_blocks": lambda: self._run_formal_corsi_stage(test_mode=True),
            "mental_arithmetic": lambda: self._run_formal_mental_arithmetic_stage(
                step_number=2,
                test_mode=True,
            ),
            "learning_cycle": lambda: self._run_formal_learning_cycle_stage(
                step_number=2,
                test_mode=True,
            ),
        }
        stage_runner_map[selected_stage]()
        return 3

    def _run_formal_opening(
        self,
        step_number: int,
        test_mode: bool,
        stage_name: str | None,
    ) -> bool:
        if test_mode and stage_name is not None:
            subtitle = (
                "现在开始正式实验测试。\n"
                f"本次仅运行：{TEST_STAGE_LABELS[stage_name]}。"
            )
        elif test_mode:
            subtitle = "现在开始正式实验测试。练习环节已跳过。"
        else:
            subtitle = "现在开始正式实验。"

        return self._show_stage(
            step_number=step_number,
            stage_name="正式开始",
            title="正式实验",
            subtitle=subtitle,
            detail="按空格进入正式实验。",
        )

    def _run_formal_rest_stage(self, step_number: int, test_mode: bool) -> None:
        rest_seconds = 3 if test_mode else 180
        if self._show_stage(
            step_number=step_number,
            stage_name="静息引导语-正式",
            title="静息态",
            subtitle=self._rest_intro_text(
                first_phase=self._formal_rest_first_phase(),
                seconds=rest_seconds,
            ),
            detail="准备好后按空格开始正式静息态记录。",
        ):
            return
        run_resting_state(
            self.context,
            config=RestingStateConfig(
                eyes_open_seconds=rest_seconds,
                eyes_closed_seconds=rest_seconds,
                cycles=1,
                auto_advance=self.config.auto_advance,
                randomize_phase_order=True,
                show_task_intro=False,
                show_phase_intro=False,
                show_completion=False,
                play_phase_transition_tone=True,
            ),
        )

    def _run_formal_digit_span_stage(self, test_mode: bool) -> None:
        wm_timeout_seconds = 8.0 if test_mode else None
        run_wm_pretest(
            self.context,
            config=WMPretestConfig(
                auto_advance=self.config.auto_advance,
                pilot_mode=test_mode,
                task_timeout_seconds=wm_timeout_seconds,
                selected_task_names=("digit_span",),
                show_wrapper_intro=False,
                show_wrapper_completion=False,
            ),
        )

    def _run_formal_corsi_stage(self, test_mode: bool) -> None:
        wm_timeout_seconds = 8.0 if test_mode else None
        run_wm_pretest(
            self.context,
            config=WMPretestConfig(
                auto_advance=self.config.auto_advance,
                pilot_mode=test_mode,
                task_timeout_seconds=wm_timeout_seconds,
                selected_task_names=("corsi_blocks",),
                show_wrapper_intro=False,
                show_wrapper_completion=False,
            ),
        )

    def _run_formal_mental_arithmetic_stage(
        self,
        step_number: int,
        test_mode: bool,
    ) -> None:
        if self._show_stage(
            step_number=step_number,
            stage_name="心算介绍-正式",
            title="心算任务",
            subtitle=(
                "在这个任务中，你将看到一道由黑色数字组成的加法题。\n"
                "请先在心中完成计算。\n"
                "随后中央会短暂出现“+”。\n"
                "当出现蓝色数字时，请判断它是否等于正确答案。"
            ),
            detail="如果蓝色数字等于正确答案，请按鼠标左键；如果不等，请按鼠标右键。",
        ):
            return
        run_mental_arithmetic(
            self.context,
            config=(
                MentalArithmeticConfig(
                    auto_advance=self.config.auto_advance,
                    show_instructions=False,
                    show_completion=False,
                    fixation_seconds=2.0,
                    pre_response_blank_seconds=0.2,
                    response_timeout_seconds=3.0,
                    inter_trial_seconds=0.2,
                    block_count=1,
                    trials_per_block=3,
                    block_rest_seconds=0.0,
                    trial_counts={"QE": 1, "QM": 1, "QH": 1},
                )
                if test_mode
                else MentalArithmeticConfig(
                    auto_advance=self.config.auto_advance,
                    show_instructions=False,
                    show_completion=False,
                )
            ),
        )

    def _run_formal_learning_cycle_stage(
        self,
        step_number: int,
        test_mode: bool,
    ) -> None:
        _ = test_mode
        if self._show_stage(
            step_number=step_number,
            stage_name="视频学习引导语",
            title="视频学习任务",
            subtitle=LEARNING_CYCLE_INTRO,
            detail=(
                "前测和后测均为：先口头复述，再完成 10 道判断题。\n"
                "视频按 3 分钟切分，段间和最后会出现 1-5 评分条。按空格开始任务。"
            ),
        ):
            return
        run_learning_cycle(
            self.context,
            config=LearningCycleConfig(
                trials_file=LEARNING_CYCLE_PROTOCOL_TRIALS_FILE,
                questionnaire_dir=LEARNING_CYCLE_QUESTIONNAIRE_DIR,
                expected_trials=1,
                inter_trial_rest_seconds=120.0,
                include_rating_phase=False,
                show_task_intro=False,
                show_completion=False,
                auto_advance=self.config.auto_advance,
            ),
        )

    def _show_stage(
        self,
        step_number: int,
        stage_name: str,
        title: str,
        subtitle: str,
        detail: str,
        footer_text: str = "",
        footer_color: str = "red",
    ) -> bool:
        self._log_stage(step_number, stage_name, detail)
        self._prepare_psychopy()
        _ = title
        win = self.window
        core = self.core
        event = self.event
        visual = self.visual
        if win is None or core is None or event is None or visual is None:
            raise RuntimeError("Protocol window is not ready.")

        body_lines = self._build_stage_lines(
            subtitle=subtitle,
            detail=detail,
            footer_text=footer_text,
            footer_color=footer_color,
        )
        prompt_text = self._extract_bottom_prompt(detail)
        body_stims = self._build_stage_stims(win, visual, body_lines)
        prompt_height = get_adaptive_text_height(win, 0.036)
        prompt_wrap_width = get_adaptive_wrap_width(win, 1.5)
        prompt_stim = visual.TextStim(
            win=win,
            text=wrap_text_for_display(
                win,
                prompt_text,
                text_height=prompt_height,
                base_wrap_width=prompt_wrap_width,
            ),
            font=self.config.font,
            color=self.config.text_color,
            colorSpace="named",
            height=prompt_height,
            pos=(0, -0.34),
            wrapWidth=prompt_wrap_width,
        )

        event.clearEvents()
        while True:
            if self.config.auto_advance:
                break
            keys = event.getKeys(keyList=["space", "return", "escape", "p", "P"])
            normalized_keys = {str(key).lower() for key in keys}
            if "escape" in normalized_keys:
                raise RuntimeError("Experiment aborted by user.")
            if "p" in normalized_keys:
                self._log_stage(step_number, f"{stage_name}-skipped", "Skipped via P/p.")
                return True
            if "space" in normalized_keys or "return" in normalized_keys:
                return False

            for stim in body_stims:
                stim.draw()
            if prompt_text:
                prompt_stim.draw()
            win.flip()

        if self.config.auto_advance:
            for stim in body_stims:
                stim.draw()
            if prompt_text:
                prompt_stim.draw()
            win.flip()
            core.wait(0.1)
        return False

    def _prepare_psychopy(self) -> None:
        configure_macos_psychopy_runtime()
        try:
            from psychopy import core, event, visual  # type: ignore
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "PsychoPy is required for protocol stage screens. "
                f"Current interpreter: {sys.executable} | Python {sys.version.split()[0]}."
            ) from exc

        self.core = core
        self.event = event
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

    def _log_stage(self, step_number: int, stage_name: str, detail: str) -> None:
        self.stage_rows.append(
            asdict(
                StageLogRow(
                    StepNumber=step_number,
                    StageName=stage_name,
                    Timestamp=datetime.now().isoformat(timespec="seconds"),
                    Detail=detail,
                )
            )
        )

    def _write_stage_log(self) -> Path:
        output_dir = self.context.output_dir / "protocol"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "protocol_stage_log.csv"
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=["StepNumber", "StageName", "Timestamp", "Detail"],
            )
            writer.writeheader()
            writer.writerows(self.stage_rows)
        return output_path

    def _show_practice_stage(
        self,
        step_number: int,
        stage_name: str,
        title: str,
        subtitle: str,
        detail: str,
    ) -> bool:
        return self._show_stage(
            step_number=step_number,
            stage_name=stage_name,
            title=title,
            subtitle=subtitle,
            detail=detail,
            footer_text=PRACTICE_HELP_FOOTER,
            footer_color="red",
        )

    @staticmethod
    def _split_text_lines(text: str) -> list[str]:
        return [line.strip() for line in text.splitlines() if line.strip()]

    @staticmethod
    def _split_sentences(text: str) -> list[str]:
        return [
            sentence.strip()
            for sentence in re.findall(r"[^。！？!?]+[。！？!?]?", text)
            if sentence.strip()
        ]

    def _extract_bottom_prompt(self, detail: str) -> str:
        prompt_sentences = [
            sentence
            for sentence in self._split_sentences(detail)
            if "按空格" in sentence or "按回车" in sentence or "按 Enter" in sentence
        ]
        return " ".join(prompt_sentences)

    def _detail_body_lines(self, detail: str) -> list[str]:
        body_lines: list[str] = []
        for raw_line in self._split_text_lines(detail):
            body_sentences = [
                sentence
                for sentence in self._split_sentences(raw_line)
                if "按空格" not in sentence
                and "按回车" not in sentence
                and "按 Enter" not in sentence
            ]
            if body_sentences:
                body_lines.append("".join(body_sentences))
        return body_lines

    def _build_stage_lines(
        self,
        subtitle: str,
        detail: str,
        footer_text: str,
        footer_color: str,
    ) -> list[tuple[str, str]]:
        lines: list[tuple[str, str]] = []
        lines.extend(
            (line, self.config.text_color) for line in self._split_text_lines(subtitle)
        )
        lines.extend(
            (line, self.config.text_color) for line in self._detail_body_lines(detail)
        )
        lines.extend((line, footer_color) for line in self._split_text_lines(footer_text))
        return lines

    def _build_stage_stims(self, win, visual, lines: list[tuple[str, str]]):
        if not lines:
            return []

        line_height = get_adaptive_text_height(win, 0.044)
        line_gap = line_height * (0.075 / 0.044)
        line_wrap_width = get_adaptive_wrap_width(win, 1.5)
        center_y = 0.08
        expanded_lines: list[tuple[str, str]] = []
        for line, color in lines:
            wrapped_line = wrap_text_for_display(
                win,
                line,
                text_height=line_height,
                base_wrap_width=line_wrap_width,
            )
            expanded_lines.extend((segment, color) for segment in wrapped_line.splitlines() if segment)
        start_y = center_y + ((len(expanded_lines) - 1) * line_gap / 2)
        stims = []
        for index, (line, color) in enumerate(expanded_lines):
            stims.append(
                visual.TextStim(
                    win=win,
                    text=line,
                    font=self.config.font,
                    color=color,
                    colorSpace="named",
                    height=line_height,
                    pos=(0, start_y - index * line_gap),
                    wrapWidth=line_wrap_width,
                )
            )
        return stims

    def _formal_rest_first_phase(self) -> str:
        phase_order = ["eyes_open", "eyes_closed"]
        cycle_random = random.Random(
            f"{self.context.participant_id}-{self.context.session_id}-1"
        )
        cycle_random.shuffle(phase_order)
        return phase_order[0]

    def _rest_intro_text(self, first_phase: str, seconds: int) -> str:
        phase_label = "睁眼" if first_phase == "eyes_open" else "闭眼"
        next_phase_label = "闭眼" if first_phase == "eyes_open" else "睁眼"
        duration_text = self._rest_duration_text(seconds)
        return f"请{phase_label}休息{duration_text}，听到滴声后{next_phase_label}。"

    @staticmethod
    def _rest_duration_text(seconds: int) -> str:
        if seconds % 60 == 0 and seconds >= 60:
            return f"{seconds // 60}分钟"
        return f"{seconds}秒"


def run(
    context: ExperimentContext,
    config: ProtocolConfig | None = None,
) -> Path:
    config = config or ProtocolConfig()
    return ProtocolTask(context=context, config=config).run()
