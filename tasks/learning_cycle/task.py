from __future__ import annotations

import csv
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from common.data_io import ExperimentContext
from config.event_codes import LEARNING_CYCLE
from config.settings import (
    DEFAULT_TRIGGER_WIDTH_MS,
    LEARNING_CYCLE_ALLOW_GUI,
    LEARNING_CYCLE_BACKGROUND_COLOR,
    LEARNING_CYCLE_EXPECTED_TRIALS,
    LEARNING_CYCLE_FONT,
    LEARNING_CYCLE_FORCE_MOUSE_VISIBLE,
    LEARNING_CYCLE_FULLSCREEN,
    LEARNING_CYCLE_MISSING_VIDEO_SECONDS,
    LEARNING_CYCLE_POST_PHASE_BLANK_SECONDS,
    LEARNING_CYCLE_QUESTIONNAIRE_DIR,
    LEARNING_CYCLE_TEXT_COLOR,
    LEARNING_CYCLE_TRIALS_FILE,
    LEARNING_CYCLE_WINDOW_SIZE,
    VIDEO_DIR,
)

EXPECTED_LOAD_LEVELS = ("low", "medium", "high")


@dataclass(frozen=True)
class LearningTrialSpec:
    base_position: int
    item_id: str
    topic: str
    load_level: str
    video_file: str
    planned_minutes: float
    pretest_form: str
    rating_form: str
    posttest_form: str
    notes: str


@dataclass(frozen=True)
class QuestionnaireOutcome:
    status: str
    form_file: str


@dataclass(frozen=True)
class LearningTrialLogRow:
    TrialNumber: int
    ItemId: str
    Topic: str
    LoadLevel: str
    VideoFile: str
    PlannedMinutes: float
    CounterbalanceRow: int
    PretestForm: str
    PretestStatus: str
    RatingForm: str
    RatingStatus: str
    PosttestForm: str
    PosttestStatus: str
    VideoStatus: str
    VideoDurationSeconds: str


@dataclass
class LearningCycleConfig:
    trials_file: Path | str = LEARNING_CYCLE_TRIALS_FILE
    questionnaire_dir: Path | str = LEARNING_CYCLE_QUESTIONNAIRE_DIR
    fullscreen: bool = LEARNING_CYCLE_FULLSCREEN
    allow_gui: bool = LEARNING_CYCLE_ALLOW_GUI
    force_mouse_visible: bool = LEARNING_CYCLE_FORCE_MOUSE_VISIBLE
    window_size: tuple[int, int] = LEARNING_CYCLE_WINDOW_SIZE
    background_color: str = LEARNING_CYCLE_BACKGROUND_COLOR
    text_color: str = LEARNING_CYCLE_TEXT_COLOR
    font: str = LEARNING_CYCLE_FONT
    expected_trials: int = LEARNING_CYCLE_EXPECTED_TRIALS
    missing_video_seconds: float = LEARNING_CYCLE_MISSING_VIDEO_SECONDS
    post_phase_blank_seconds: float = LEARNING_CYCLE_POST_PHASE_BLANK_SECONDS
    counterbalance_row: int | None = None
    auto_advance: bool = False

    def __post_init__(self) -> None:
        self.trials_file = Path(self.trials_file)
        self.questionnaire_dir = Path(self.questionnaire_dir)
        if self.expected_trials <= 0:
            raise ValueError("expected_trials must be positive.")
        if self.missing_video_seconds < 0:
            raise ValueError("missing_video_seconds must be non-negative.")
        if self.post_phase_blank_seconds < 0:
            raise ValueError("post_phase_blank_seconds must be non-negative.")
        if len(self.window_size) != 2 or any(size <= 0 for size in self.window_size):
            raise ValueError("window_size must contain two positive integers.")


class TaskAborted(RuntimeError):
    pass


class TrialOrderBuilder:
    @staticmethod
    def balanced_latin_square(size: int) -> list[list[int]]:
        if size <= 0:
            raise ValueError("size must be positive.")

        rows: list[list[int]] = []
        for row_index in range(size):
            row: list[int] = []
            for column_index in range(size):
                if column_index % 2 == 0:
                    value = (row_index + (column_index // 2)) % size
                else:
                    value = (row_index - ((column_index + 1) // 2)) % size
                row.append(value)
            rows.append(row)
        return rows

    @classmethod
    def select_row(
        cls,
        participant_id: str,
        size: int,
        explicit_row: int | None,
    ) -> tuple[int, list[int]]:
        rows = cls.balanced_latin_square(size)
        if explicit_row is not None:
            row_index = explicit_row % len(rows)
            return row_index, rows[row_index]

        stable_value = sum(ord(char) for char in participant_id)
        row_index = stable_value % len(rows)
        return row_index, rows[row_index]


class TrialLogger:
    TRIAL_FIELDS = (
        "TrialNumber",
        "ItemId",
        "Topic",
        "LoadLevel",
        "VideoFile",
        "PlannedMinutes",
        "CounterbalanceRow",
        "PretestForm",
        "PretestStatus",
        "RatingForm",
        "RatingStatus",
        "PosttestForm",
        "PosttestStatus",
        "VideoStatus",
        "VideoDurationSeconds",
    )
    EVENT_FIELDS = (
        "TrialNumber",
        "ItemId",
        "Topic",
        "LoadLevel",
        "EventName",
        "EventCode",
        "Timestamp",
        "Detail",
    )

    def __init__(self) -> None:
        self.trial_rows: list[dict[str, object]] = []
        self.event_rows: list[dict[str, object]] = []

    def log_trial(self, row: LearningTrialLogRow) -> None:
        self.trial_rows.append(asdict(row))

    def log_event(
        self,
        trial_number: int | str,
        trial: LearningTrialSpec | None,
        event_name: str,
        event_code: int,
        timestamp: float,
        detail: str = "",
    ) -> None:
        self.event_rows.append(
            {
                "TrialNumber": trial_number,
                "ItemId": "" if trial is None else trial.item_id,
                "Topic": "" if trial is None else trial.topic,
                "LoadLevel": "" if trial is None else trial.load_level,
                "EventName": event_name,
                "EventCode": event_code,
                "Timestamp": f"{timestamp:.6f}",
                "Detail": detail,
            }
        )

    def write_outputs(self, output_dir: Path) -> None:
        self._write_csv(
            output_dir / "learning_cycle_trial_log.csv",
            self.TRIAL_FIELDS,
            self.trial_rows,
        )
        self._write_csv(
            output_dir / "learning_cycle_events.csv",
            self.EVENT_FIELDS,
            self.event_rows,
        )

    @staticmethod
    def _write_csv(
        output_path: Path,
        fieldnames: tuple[str, ...],
        rows: list[dict[str, object]],
    ) -> None:
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
            writer.writeheader()
            writer.writerows(rows)


class LearningCycleTask:
    def __init__(self, context: ExperimentContext, config: LearningCycleConfig):
        self.context = context
        self.config = config
        self.logger = TrialLogger()
        self.base_trials = self._load_trials(config.trials_file)
        self.counterbalance_row, self.ordered_trials = self._build_trial_order(
            self.base_trials
        )
        self.window = None
        self.core = None
        self.event = None
        self.visual = None
        self.global_clock = None
        self.title_stim = None
        self.subtitle_stim = None
        self.detail_stim = None

    def run(self) -> Path:
        self._prepare_psychopy()
        output_dir = self.context.output_dir / "learning_cycle"
        output_dir.mkdir(parents=True, exist_ok=True)
        config_path = output_dir / "learning_cycle_config.json"
        order_path = output_dir / "learning_cycle_order.csv"

        task_error: BaseException | None = None

        try:
            self._show_task_intro()
            for trial_number, trial in enumerate(self.ordered_trials, start=1):
                self._run_trial(trial_number, trial)
            self._show_completion()
        except BaseException as exc:
            task_error = exc
        finally:
            if self.window is not None:
                self.window.close()
            self.logger.write_outputs(output_dir)
            self._write_order_snapshot(order_path)
            self._write_config_snapshot(config_path)

        if task_error is not None:
            raise task_error

        return output_dir / "learning_cycle_trial_log.csv"

    def _prepare_psychopy(self) -> None:
        try:
            from psychopy import core, event, visual  # type: ignore
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "PsychoPy is not installed in the Python interpreter running this task. "
                f"Current interpreter: {sys.executable} | Python {sys.version.split()[0]}."
            ) from exc

        self.core = core
        self.event = event
        self.visual = visual
        self.window = visual.Window(
            size=self.config.window_size,
            fullscr=self.config.fullscreen,
            color=self.config.background_color,
            colorSpace="named",
            units="height",
            allowGUI=self.config.allow_gui,
        )
        self._force_mouse_visible()
        self.global_clock = core.Clock()

        self.title_stim = visual.TextStim(
            win=self.window,
            text="",
            font=self.config.font,
            color=self.config.text_color,
            colorSpace="named",
            height=0.05,
            wrapWidth=1.5,
        )
        self.subtitle_stim = visual.TextStim(
            win=self.window,
            text="",
            font=self.config.font,
            color=self.config.text_color,
            colorSpace="named",
            height=0.03,
            pos=(0, -0.26),
            wrapWidth=1.5,
        )
        self.detail_stim = visual.TextStim(
            win=self.window,
            text="",
            font=self.config.font,
            color=self.config.text_color,
            colorSpace="named",
            height=0.028,
            pos=(0, -0.38),
            wrapWidth=1.5,
        )

    def _force_mouse_visible(self) -> None:
        if not self.config.force_mouse_visible or self.window is None:
            return

        try:
            self.window.mouseVisible = True
        except Exception:
            pass

        win_handle = getattr(self.window, "winHandle", None)
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

    def _load_trials(self, trials_file: Path) -> list[LearningTrialSpec]:
        if not trials_file.exists():
            raise FileNotFoundError(f"Learning-cycle trials file not found: {trials_file}")

        rows: list[LearningTrialSpec] = []
        with trials_file.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            required_columns = {
                "base_position",
                "item_id",
                "topic",
                "load_level",
                "video_file",
                "planned_minutes",
                "pretest_form",
                "rating_form",
                "posttest_form",
                "notes",
            }
            missing = required_columns - set(reader.fieldnames or [])
            if missing:
                raise ValueError(
                    "Learning-cycle trials file is missing columns: "
                    f"{sorted(missing)}."
                )

            for raw_row in reader:
                rows.append(
                    LearningTrialSpec(
                        base_position=int(raw_row["base_position"]),
                        item_id=raw_row["item_id"].strip(),
                        topic=raw_row["topic"].strip(),
                        load_level=raw_row["load_level"].strip().lower(),
                        video_file=raw_row["video_file"].strip(),
                        planned_minutes=float(raw_row["planned_minutes"]),
                        pretest_form=raw_row["pretest_form"].strip(),
                        rating_form=raw_row["rating_form"].strip(),
                        posttest_form=raw_row["posttest_form"].strip(),
                        notes=raw_row["notes"].strip(),
                    )
                )

        self._validate_trials(rows)
        return sorted(rows, key=lambda trial: trial.base_position)

    def _validate_trials(self, rows: list[LearningTrialSpec]) -> None:
        if len(rows) != self.config.expected_trials:
            raise ValueError(
                f"Expected {self.config.expected_trials} learning-cycle trials, "
                f"found {len(rows)}."
            )

        positions = [row.base_position for row in rows]
        if sorted(positions) != list(range(1, self.config.expected_trials + 1)):
            raise ValueError("base_position must be a complete 1..N sequence.")

        item_ids = [row.item_id for row in rows]
        if len(item_ids) != len(set(item_ids)):
            raise ValueError("item_id values must be unique.")

        for row in rows:
            if row.load_level not in EXPECTED_LOAD_LEVELS:
                raise ValueError(
                    f"Unsupported load_level for {row.item_id}: {row.load_level}."
                )
            if row.planned_minutes <= 0:
                raise ValueError(
                    f"planned_minutes must be positive for {row.item_id}."
                )

        load_counts = {level: 0 for level in EXPECTED_LOAD_LEVELS}
        topic_counts: dict[str, set[str]] = {}
        for row in rows:
            load_counts[row.load_level] += 1
            topic_counts.setdefault(row.topic, set()).add(row.load_level)

        if any(count != 2 for count in load_counts.values()):
            raise ValueError(
                "The 6-trial design must contain exactly two low, two medium, "
                "and two high load videos."
            )

        if len(topic_counts) != 2:
            raise ValueError("The current learning-cycle design expects exactly two topics.")

        if any(loads != set(EXPECTED_LOAD_LEVELS) for loads in topic_counts.values()):
            raise ValueError(
                "Each topic must include one low, one medium, and one high load video."
            )

    def _build_trial_order(
        self,
        base_trials: list[LearningTrialSpec],
    ) -> tuple[int, list[LearningTrialSpec]]:
        row_index, order = TrialOrderBuilder.select_row(
            participant_id=self.context.participant_id,
            size=len(base_trials),
            explicit_row=self.config.counterbalance_row,
        )
        ordered_trials = [base_trials[position] for position in order]
        return row_index, ordered_trials

    def _show_task_intro(self) -> None:
        record = self.context.trigger.emit(
            name="learning_cycle.task_start",
            code=LEARNING_CYCLE["task_start"],
            width_ms=DEFAULT_TRIGGER_WIDTH_MS,
        )
        self.logger.log_event(
            trial_number=0,
            trial=None,
            event_name="task_start",
            event_code=LEARNING_CYCLE["task_start"],
            timestamp=record.timestamp,
            detail=f"counterbalance_row={self.counterbalance_row}",
        )

        self._wait_for_space(
            main_text=(
                "视频学习任务\n\n"
                "共 6 个试次。\n"
                "每个试次依次包括：前测问卷、视频播放、主观量表、后测接口。\n"
                "请根据屏幕提示完成各阶段。"
            ),
            subtitle_text=(
                "视频开始和结束会记录 EEG 事件。"
                " 当前顺序已按被试编号自动分配平衡顺序。"
            ),
            detail_text="按空格开始，Esc 中止。",
        )

    def _run_trial(self, trial_number: int, trial: LearningTrialSpec) -> None:
        pretest_outcome = self._run_questionnaire_phase(
            trial_number=trial_number,
            trial=trial,
            phase_name="pretest",
            event_code=LEARNING_CYCLE["pretest_start"],
            form_file=trial.pretest_form,
            prompt_title="前测知识问卷",
            prompt_body=(
                "这里预留给后续接入选择题、判断题或填空题。\n"
                "当前版本只负责记录试次、表单引用和阶段完成状态。"
            ),
        )

        video_status, video_duration_seconds = self._run_video_phase(trial_number, trial)

        rating_outcome = self._run_questionnaire_phase(
            trial_number=trial_number,
            trial=trial,
            phase_name="rating",
            event_code=LEARNING_CYCLE["rating_start"],
            form_file=trial.rating_form,
            prompt_title="后测主观量表",
            prompt_body=(
                "这里预留给后续接入 NASA-TLX 或简化心理努力量表。\n"
                "当前版本只保留接口和完成确认。"
            ),
        )

        posttest_outcome = self._run_questionnaire_phase(
            trial_number=trial_number,
            trial=trial,
            phase_name="posttest",
            event_code=LEARNING_CYCLE["posttest_start"],
            form_file=trial.posttest_form,
            prompt_title="后测表现接口",
            prompt_body=(
                "这里预留给后续接入视频后的表现测验或认真作答检查。\n"
                "当前版本只保留接口和完成确认。"
            ),
        )

        self.logger.log_trial(
            LearningTrialLogRow(
                TrialNumber=trial_number,
                ItemId=trial.item_id,
                Topic=trial.topic,
                LoadLevel=trial.load_level,
                VideoFile=trial.video_file,
                PlannedMinutes=trial.planned_minutes,
                CounterbalanceRow=self.counterbalance_row,
                PretestForm=trial.pretest_form,
                PretestStatus=pretest_outcome.status,
                RatingForm=trial.rating_form,
                RatingStatus=rating_outcome.status,
                PosttestForm=trial.posttest_form,
                PosttestStatus=posttest_outcome.status,
                VideoStatus=video_status,
                VideoDurationSeconds=f"{video_duration_seconds:.6f}",
            )
        )

    def _run_questionnaire_phase(
        self,
        trial_number: int,
        trial: LearningTrialSpec,
        phase_name: str,
        event_code: int,
        form_file: str,
        prompt_title: str,
        prompt_body: str,
    ) -> QuestionnaireOutcome:
        record = self.context.trigger.emit(
            name=f"learning_cycle.{phase_name}_start",
            code=event_code,
            width_ms=DEFAULT_TRIGGER_WIDTH_MS,
        )
        resolved_form = self._resolve_form_path(form_file)
        self.logger.log_event(
            trial_number=trial_number,
            trial=trial,
            event_name=f"{phase_name}_start",
            event_code=event_code,
            timestamp=record.timestamp,
            detail=resolved_form,
        )

        self._wait_for_space(
            main_text=(
                f"{prompt_title}\n\n"
                f"Trial {trial_number} / {len(self.ordered_trials)}\n"
                f"主题: {trial.topic}\n"
                f"负荷等级: {trial.load_level}"
            ),
            subtitle_text=prompt_body,
            detail_text=(
                f"表单接口: {resolved_form}\n"
                "完成该阶段后按空格继续。"
            ),
        )

        self._show_blank(self.config.post_phase_blank_seconds)
        return QuestionnaireOutcome(status="placeholder_completed", form_file=resolved_form)

    def _run_video_phase(
        self,
        trial_number: int,
        trial: LearningTrialSpec,
    ) -> tuple[str, float]:
        video_path = self._resolve_video_path(trial.video_file)
        start_record = self.context.trigger.emit(
            name="learning_cycle.video_start",
            code=LEARNING_CYCLE["video_start"],
            width_ms=DEFAULT_TRIGGER_WIDTH_MS,
        )
        self.logger.log_event(
            trial_number=trial_number,
            trial=trial,
            event_name="video_start",
            event_code=LEARNING_CYCLE["video_start"],
            timestamp=start_record.timestamp,
            detail=video_path,
        )

        if Path(video_path).exists():
            status, elapsed_seconds = self._play_video_file(video_path)
        else:
            elapsed_seconds = self._run_missing_video_placeholder(trial_number, trial, video_path)
            status = "placeholder_missing_video"

        end_record = self.context.trigger.emit(
            name="learning_cycle.video_end",
            code=LEARNING_CYCLE["video_end"],
            width_ms=DEFAULT_TRIGGER_WIDTH_MS,
        )
        self.logger.log_event(
            trial_number=trial_number,
            trial=trial,
            event_name="video_end",
            event_code=LEARNING_CYCLE["video_end"],
            timestamp=end_record.timestamp,
            detail=f"{video_path}|{status}|{elapsed_seconds:.6f}",
        )

        self._show_blank(self.config.post_phase_blank_seconds)
        return status, elapsed_seconds

    def _play_video_file(self, video_path: str) -> tuple[str, float]:
        movie_stim = self._build_movie_stim(video_path)
        playback_clock = self.core.Clock()
        self.event.clearEvents()

        while True:
            self._ensure_escape_not_pressed()
            movie_stim.draw()
            self.window.flip()
            if self._movie_finished(movie_stim):
                break

        return "played", playback_clock.getTime()

    def _build_movie_stim(self, video_path: str):
        errors: list[str] = []
        for class_name in ("MovieStim", "MovieStim3"):
            stim_class = getattr(self.visual, class_name, None)
            if stim_class is None:
                continue
            try:
                return stim_class(self.window, filename=video_path)
            except Exception as exc:  # pragma: no cover - depends on local video backend
                errors.append(f"{class_name}: {exc}")

        raise RuntimeError(
            "Unable to create a PsychoPy movie stimulus. "
            f"Tried MovieStim backends for: {video_path}. Errors: {errors}"
        )

    def _movie_finished(self, movie_stim) -> bool:
        finished_flag = getattr(movie_stim, "isFinished", None)
        if isinstance(finished_flag, bool):
            return finished_flag
        status = getattr(movie_stim, "status", None)
        finished_constant = getattr(self.visual, "FINISHED", None)
        if finished_constant is not None and status == finished_constant:
            return True
        return False

    def _run_missing_video_placeholder(
        self,
        trial_number: int,
        trial: LearningTrialSpec,
        video_path: str,
    ) -> float:
        placeholder_seconds = self.config.missing_video_seconds
        start_clock = self.core.Clock()
        self.event.clearEvents()

        while start_clock.getTime() < placeholder_seconds:
            self._ensure_escape_not_pressed()
            self._draw_text_page(
                main_text=(
                    f"视频占位\n\nTrial {trial_number} / {len(self.ordered_trials)}\n"
                    f"主题: {trial.topic}\n负荷等级: {trial.load_level}"
                ),
                subtitle_text=(
                    "当前视频文件不存在，使用占位播放窗口继续联调。"
                ),
                detail_text=(
                    f"视频路径: {video_path}\n"
                    f"计划时长: {trial.planned_minutes:.2f} 分钟\n"
                    f"占位时长: {placeholder_seconds:.1f} 秒"
                ),
            )
            self.window.flip()

        return start_clock.getTime()

    def _show_completion(self) -> None:
        record = self.context.trigger.emit(
            name="learning_cycle.task_end",
            code=LEARNING_CYCLE["task_end"],
            width_ms=DEFAULT_TRIGGER_WIDTH_MS,
        )
        self.logger.log_event(
            trial_number="END",
            trial=None,
            event_name="task_end",
            event_code=LEARNING_CYCLE["task_end"],
            timestamp=record.timestamp,
            detail=f"completed_trials={len(self.ordered_trials)}",
        )

        self._wait_for_space(
            main_text=(
                "视频学习任务结束\n\n"
                f"已完成 {len(self.ordered_trials)} 个试次。"
            ),
            subtitle_text="日志已保存，可继续检查问卷接口和视频素材配置。",
            detail_text="按空格结束。",
        )

    def _wait_for_space(
        self,
        main_text: str,
        subtitle_text: str,
        detail_text: str,
    ) -> None:
        self.event.clearEvents()
        while True:
            if self.config.auto_advance:
                return

            keys = self.event.getKeys(keyList=["space", "escape", "return"])
            if "escape" in keys:
                raise TaskAborted("Experiment aborted by user.")
            if "space" in keys or "return" in keys:
                return

            self._draw_text_page(main_text, subtitle_text, detail_text)
            self.window.flip()

    def _draw_text_page(
        self,
        main_text: str,
        subtitle_text: str,
        detail_text: str,
    ) -> None:
        self.title_stim.text = main_text
        self.subtitle_stim.text = subtitle_text
        self.detail_stim.text = detail_text
        self.title_stim.draw()
        self.subtitle_stim.draw()
        self.detail_stim.draw()

    def _show_blank(self, seconds: float) -> None:
        if seconds <= 0:
            return

        blank_clock = self.core.Clock()
        self.event.clearEvents()
        while blank_clock.getTime() < seconds:
            self._ensure_escape_not_pressed()
            self.window.flip()

    def _ensure_escape_not_pressed(self) -> None:
        if "escape" in self.event.getKeys(keyList=["escape"]):
            raise TaskAborted("Experiment aborted by user.")

    def _resolve_video_path(self, video_file: str) -> str:
        candidate = Path(video_file)
        if candidate.is_absolute():
            return str(candidate)
        return str((VIDEO_DIR / candidate).resolve())

    def _resolve_form_path(self, form_file: str) -> str:
        if not form_file:
            return ""
        candidate = Path(form_file)
        if candidate.is_absolute():
            return str(candidate)
        return str((self.config.questionnaire_dir / candidate).resolve())

    def _write_order_snapshot(self, output_path: Path) -> None:
        rows = [
            {
                "TrialNumber": trial_number,
                "CounterbalanceRow": self.counterbalance_row,
                "BasePosition": trial.base_position,
                "ItemId": trial.item_id,
                "Topic": trial.topic,
                "LoadLevel": trial.load_level,
                "VideoFile": trial.video_file,
                "PlannedMinutes": trial.planned_minutes,
                "PretestForm": trial.pretest_form,
                "RatingForm": trial.rating_form,
                "PosttestForm": trial.posttest_form,
            }
            for trial_number, trial in enumerate(self.ordered_trials, start=1)
        ]
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    def _write_config_snapshot(self, output_path: Path) -> None:
        payload = {
            "config": {
                **asdict(self.config),
                "trials_file": str(self.config.trials_file),
                "questionnaire_dir": str(self.config.questionnaire_dir),
            },
            "counterbalance_row": self.counterbalance_row,
            "ordered_item_ids": [trial.item_id for trial in self.ordered_trials],
        }
        with output_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)


def run(
    context: ExperimentContext,
    config: LearningCycleConfig | None = None,
) -> Path:
    config = config or LearningCycleConfig()
    task = LearningCycleTask(context=context, config=config)
    return task.run()
