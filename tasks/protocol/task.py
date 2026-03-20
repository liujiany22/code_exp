from __future__ import annotations

import csv
import sys
from datetime import datetime
from dataclasses import asdict, dataclass
from pathlib import Path

from common.data_io import ExperimentContext
from common.psychopy_compat import configure_macos_psychopy_runtime
from config.settings import (
    LEARNING_CYCLE_PRACTICE_TRIALS_FILE,
    LEARNING_CYCLE_PROTOCOL_TRIALS_FILE,
    LEARNING_CYCLE_QUESTIONNAIRE_DIR,
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

PRACTICE_REST_INTRO = (
    "接下来进入静息练习。\n"
    "请按照屏幕提示完成睁眼和闭眼两个阶段。\n"
    "睁眼时请注视屏幕中央，闭眼时请保持安静放松。"
)

FORMAL_REST_INTRO = (
    "接下来进入正式静息态记录。\n"
    "本阶段包含睁眼和闭眼两个部分，顺序将随机呈现。\n"
    "听到提示音后，请根据提示及时切换状态，并尽量保持身体稳定。"
)

FORMAL_DIGIT_SPAN_INTRO = (
    "在这个任务中，你需要记住屏幕上依次闪现的数字。\n"
    "当屏幕上出现“回忆”提示时，请使用键盘上方的数字键，"
    "按照刚才看到的顺序输入你记住的所有数字。"
)

FORMAL_CORSI_INTRO = (
    "在这个任务中，你需要仔细观察并记住屏幕上方块亮起的顺序。\n"
    "在呈现结束后，请按照相同的顺序点击这些方块。"
)

LEARNING_CYCLE_INTRO = (
    "接下来进入视频学习任务。\n"
    "每组实验都包含前测、视频播放和后测三个部分。\n"
    "请认真观看视频，并根据要求完成前后测作答。"
)

PRACTICE_LEARNING_DEMO = (
    "视频学习练习演示接口已预留。\n"
    "当前练习流程暂不播放真实视频材料，后续可在这里接入正式演示。"
)

BREAK_INTRO = (
    "练习阶段结束。\n"
    "请短暂休息，调整状态后进入正式实验。"
)


@dataclass(frozen=True)
class ProtocolConfig:
    test_mode: bool = False
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

    def run(self) -> Path:
        self._run_practice_segment()
        self._run_formal_segment()
        self._show_stage(
            step_number=21,
            stage_name="实验结束",
            title="实验结束",
            subtitle="本次实验流程已完成。",
            detail="感谢参与。按空格结束。",
        )
        return self._write_stage_log()

    def _run_practice_segment(self) -> None:
        self._show_stage(
            step_number=1,
            stage_name="练习开始",
            title="引导语",
            subtitle="现在开始练习环节。",
            detail="按空格进入练习。",
        )
        self._show_stage(
            step_number=2,
            stage_name="静息引导语-练习",
            title="静息引导语",
            subtitle=PRACTICE_REST_INTRO,
            detail="准备好后按空格开始静息练习。",
        )
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
        self._show_stage(
            step_number=4,
            stage_name="数字记忆介绍-练习",
            title="数字记忆任务介绍语",
            subtitle=(
                "在这个任务中，你需要记住屏幕上依次闪现的数字。\n"
                "当屏幕上出现“回忆”提示时，请使用键盘上方的数字键，"
                "按照刚才看到的顺序输入你记住的所有数字。"
            ),
            detail="请尽量按照原顺序完整作答。按空格进入练习。",
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
        self._show_stage(
            step_number=6,
            stage_name="柯西方块介绍-练习",
            title="柯西方块介绍语",
            subtitle=(
                "在这个任务中，你需要仔细观察并记住屏幕上方块亮起的顺序。\n"
                "在呈现结束后，请按照相同的顺序点击这些方块。"
            ),
            detail="请尽量准确复现亮起顺序。按空格进入练习。",
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
        self._show_stage(
            step_number=8,
            stage_name="心算介绍-练习",
            title="心算介绍语",
            subtitle=(
                "在这个任务中，你将看到一道由黑色数字组成的加法题。\n"
                "请先在心中完成计算。随后中央会短暂出现“+”。当出现蓝色数字时，"
                "请判断它是否等于正确答案。"
            ),
            detail="如果蓝色数字等于正确答案，请按鼠标左键；如果不等，请按鼠标右键。按空格进入练习。",
        )
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
        self._show_stage(
            step_number=10,
            stage_name="视频学习介绍-练习",
            title="视频学习任务介绍语",
            subtitle=LEARNING_CYCLE_INTRO,
            detail="练习阶段仅展示流程说明。按空格继续。",
        )
        self._show_stage(
            step_number=11,
            stage_name="视频学习演示-练习",
            title="视频学习演示",
            subtitle=PRACTICE_LEARNING_DEMO,
            detail="按空格进入下一步。",
        )
        self._show_stage(
            step_number=12,
            stage_name="休息引导语",
            title="休息引导语",
            subtitle=BREAK_INTRO,
            detail="按空格进入正式实验。",
        )

    def _run_formal_segment(self) -> None:
        self._show_stage(
            step_number=13,
            stage_name="正式开始",
            title="引导语",
            subtitle="现在开始正式实验。",
            detail="按空格进入正式实验。",
        )
        self._show_stage(
            step_number=14,
            stage_name="静息引导语-正式",
            title="静息引导语",
            subtitle=FORMAL_REST_INTRO,
            detail="准备好后按空格开始正式静息态记录。",
        )
        rest_seconds = 3 if self.config.test_mode else 180
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
        self._show_stage(
            step_number=16,
            stage_name="数字记忆介绍-正式",
            title="数字记忆任务介绍语",
            subtitle=FORMAL_DIGIT_SPAN_INTRO,
            detail="请尽量按照原顺序完整作答。按空格开始任务。",
        )
        run_wm_pretest(
            self.context,
            config=WMPretestConfig(
                auto_advance=self.config.auto_advance,
                pilot_mode=self.config.test_mode,
                task_timeout_seconds=12.0 if self.config.test_mode else None,
                selected_task_names=("digit_span",),
                show_wrapper_intro=False,
                show_wrapper_completion=False,
            ),
        )
        self._show_stage(
            step_number=17,
            stage_name="柯西方块介绍-正式",
            title="柯西方块任务介绍语",
            subtitle=FORMAL_CORSI_INTRO,
            detail="请尽量准确复现亮起顺序。按空格开始任务。",
        )
        run_wm_pretest(
            self.context,
            config=WMPretestConfig(
                auto_advance=self.config.auto_advance,
                pilot_mode=self.config.test_mode,
                task_timeout_seconds=12.0 if self.config.test_mode else None,
                selected_task_names=("corsi_blocks",),
                show_wrapper_intro=False,
                show_wrapper_completion=False,
            ),
        )
        self._show_stage(
            step_number=18,
            stage_name="心算介绍-正式",
            title="心算介绍语",
            subtitle=(
                "在这个任务中，你将看到一道由黑色数字组成的加法题。\n"
                "请先在心中完成计算。随后中央会短暂出现“+”。当出现蓝色数字时，"
                "请判断它是否等于正确答案。"
            ),
            detail="如果蓝色数字等于正确答案，请按鼠标左键；如果不等，请按鼠标右键。",
        )
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
                if self.config.test_mode
                else MentalArithmeticConfig(
                    auto_advance=self.config.auto_advance,
                    show_instructions=False,
                    show_completion=False,
                )
            ),
        )
        self._show_stage(
            step_number=19,
            stage_name="视频学习引导语",
            title="视频学习引导语",
            subtitle=LEARNING_CYCLE_INTRO,
            detail="每两组之间会安排休息时间。按空格开始任务。",
        )
        run_learning_cycle(
            self.context,
            config=(
                LearningCycleConfig(
                    trials_file=LEARNING_CYCLE_PRACTICE_TRIALS_FILE,
                    questionnaire_dir=LEARNING_CYCLE_QUESTIONNAIRE_DIR,
                    expected_trials=1,
                    missing_video_seconds=1.0,
                    inter_trial_rest_seconds=0.0,
                    include_rating_phase=False,
                    show_task_intro=False,
                    show_completion=False,
                    auto_advance=self.config.auto_advance,
                )
                if self.config.test_mode
                else LearningCycleConfig(
                    trials_file=LEARNING_CYCLE_PROTOCOL_TRIALS_FILE,
                    questionnaire_dir=LEARNING_CYCLE_QUESTIONNAIRE_DIR,
                    expected_trials=2,
                    inter_trial_rest_seconds=120.0,
                    include_rating_phase=False,
                    show_task_intro=False,
                    show_completion=False,
                    auto_advance=self.config.auto_advance,
                )
            ),
        )

    def _show_stage(
        self,
        step_number: int,
        stage_name: str,
        title: str,
        subtitle: str,
        detail: str,
    ) -> None:
        self._log_stage(step_number, stage_name, detail)
        configure_macos_psychopy_runtime()
        try:
            from psychopy import core, event, visual  # type: ignore
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "PsychoPy is required for protocol stage screens. "
                f"Current interpreter: {sys.executable} | Python {sys.version.split()[0]}."
            ) from exc

        win = visual.Window(
            size=self.config.window_size,
            fullscr=self.config.fullscreen,
            color=self.config.background_color,
            colorSpace="named",
            units="height",
            allowGUI=self.config.allow_gui,
        )
        title_stim = visual.TextStim(
            win=win,
            text=title,
            font=self.config.font,
            color=self.config.text_color,
            colorSpace="named",
            height=0.05,
            wrapWidth=1.5,
        )
        subtitle_stim = visual.TextStim(
            win=win,
            text=subtitle,
            font=self.config.font,
            color=self.config.text_color,
            colorSpace="named",
            height=0.03,
            pos=(0, -0.24),
            wrapWidth=1.5,
        )
        detail_stim = visual.TextStim(
            win=win,
            text=detail,
            font=self.config.font,
            color=self.config.text_color,
            colorSpace="named",
            height=0.028,
            pos=(0, -0.38),
            wrapWidth=1.5,
        )

        event.clearEvents()
        while True:
            if self.config.auto_advance:
                break
            keys = event.getKeys(keyList=["space", "return", "escape"])
            if "escape" in keys:
                win.close()
                raise RuntimeError("Experiment aborted by user.")
            if "space" in keys or "return" in keys:
                break

            title_stim.draw()
            subtitle_stim.draw()
            detail_stim.draw()
            win.flip()

        if self.config.auto_advance:
            title_stim.draw()
            subtitle_stim.draw()
            detail_stim.draw()
            win.flip()
            core.wait(0.1)

        win.close()

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


def run(
    context: ExperimentContext,
    config: ProtocolConfig | None = None,
) -> Path:
    config = config or ProtocolConfig()
    return ProtocolTask(context=context, config=config).run()
