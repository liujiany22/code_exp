from __future__ import annotations

import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
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
from config.event_codes import LEARNING_CYCLE
from config.settings import (
    DEFAULT_TRIGGER_WIDTH_MS,
    LEARNING_CYCLE_ALLOW_GUI,
    LEARNING_CYCLE_BACKGROUND_COLOR,
    LEARNING_CYCLE_EXPECTED_TRIALS,
    LEARNING_CYCLE_FONT,
    LEARNING_CYCLE_FORCE_MOUSE_VISIBLE,
    LEARNING_CYCLE_FULLSCREEN,
    LEARNING_CYCLE_INTER_TRIAL_REST_SECONDS,
    LEARNING_CYCLE_MISSING_VIDEO_SECONDS,
    LEARNING_CYCLE_POST_PHASE_BLANK_SECONDS,
    LEARNING_CYCLE_QUESTIONNAIRE_DIR,
    LEARNING_CYCLE_QUESTION_REST_SECONDS,
    LEARNING_CYCLE_RESPONSE_SECONDS,
    LEARNING_CYCLE_SEGMENT_RATING_MAX,
    LEARNING_CYCLE_SEGMENT_RATING_MIN,
    LEARNING_CYCLE_SEGMENT_SECONDS,
    LEARNING_CYCLE_STATEMENT_SECONDS,
    LEARNING_CYCLE_TEXT_COLOR,
    LEARNING_CYCLE_TRIALS_FILE,
    LEARNING_CYCLE_WINDOW_SIZE,
    PSYCHOPY_MONITOR_NAME,
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
class QuestionnaireItem:
    item_number: int
    question_text: str
    correct_answer: str
    question_type: str


@dataclass(frozen=True)
class QuestionnaireResponseRow:
    TrialNumber: int
    ItemId: str
    PhaseName: str
    FormFile: str
    ItemNumber: int
    QuestionType: str
    QuestionText: str
    CorrectAnswer: str
    ParticipantAnswer: str
    IsCorrect: int
    ResponseTime: str


@dataclass(frozen=True)
class RecallResponseRow:
    TrialNumber: int
    ItemId: str
    PhaseName: str
    MaterialLabel: str
    PromptText: str
    DurationSeconds: str


@dataclass(frozen=True)
class SegmentRatingRow:
    TrialNumber: int
    ItemId: str
    Topic: str
    SegmentIndex: int
    TotalSegments: int
    RatingValue: int
    ResponseTime: str
    SegmentFile: str
    RatingMoment: str


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
    statement_seconds: float = LEARNING_CYCLE_STATEMENT_SECONDS
    response_seconds: float = LEARNING_CYCLE_RESPONSE_SECONDS
    question_rest_seconds: float = LEARNING_CYCLE_QUESTION_REST_SECONDS
    segment_seconds: float = LEARNING_CYCLE_SEGMENT_SECONDS
    segment_rating_min: int = LEARNING_CYCLE_SEGMENT_RATING_MIN
    segment_rating_max: int = LEARNING_CYCLE_SEGMENT_RATING_MAX
    inter_trial_rest_seconds: float = LEARNING_CYCLE_INTER_TRIAL_REST_SECONDS
    counterbalance_row: int | None = None
    auto_advance: bool = False
    include_rating_phase: bool = False
    show_task_intro: bool = True
    show_completion: bool = True

    def __post_init__(self) -> None:
        self.trials_file = Path(self.trials_file)
        self.questionnaire_dir = Path(self.questionnaire_dir)
        if self.expected_trials <= 0:
            raise ValueError("expected_trials must be positive.")
        if self.missing_video_seconds < 0:
            raise ValueError("missing_video_seconds must be non-negative.")
        if self.post_phase_blank_seconds < 0:
            raise ValueError("post_phase_blank_seconds must be non-negative.")
        if self.statement_seconds < 0:
            raise ValueError("statement_seconds must be non-negative.")
        if self.response_seconds < 0:
            raise ValueError("response_seconds must be non-negative.")
        if self.question_rest_seconds < 0:
            raise ValueError("question_rest_seconds must be non-negative.")
        if self.segment_seconds <= 0:
            raise ValueError("segment_seconds must be positive.")
        if self.inter_trial_rest_seconds < 0:
            raise ValueError("inter_trial_rest_seconds must be non-negative.")
        if self.segment_rating_max < self.segment_rating_min:
            raise ValueError("segment_rating_max must be >= segment_rating_min.")
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
    SEGMENT_RATING_FIELDS = (
        "TrialNumber",
        "ItemId",
        "Topic",
        "SegmentIndex",
        "TotalSegments",
        "RatingValue",
        "ResponseTime",
        "SegmentFile",
        "RatingMoment",
    )
    RECALL_FIELDS = (
        "TrialNumber",
        "ItemId",
        "PhaseName",
        "MaterialLabel",
        "PromptText",
        "DurationSeconds",
    )
    QUESTIONNAIRE_FIELDS = (
        "TrialNumber",
        "ItemId",
        "PhaseName",
        "FormFile",
        "ItemNumber",
        "QuestionType",
        "QuestionText",
        "CorrectAnswer",
        "ParticipantAnswer",
        "IsCorrect",
        "ResponseTime",
    )
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
        self.questionnaire_rows: list[dict[str, object]] = []
        self.recall_rows: list[dict[str, object]] = []
        self.segment_rating_rows: list[dict[str, object]] = []

    def log_trial(self, row: LearningTrialLogRow) -> None:
        self.trial_rows.append(asdict(row))

    def log_questionnaire_response(self, row: QuestionnaireResponseRow) -> None:
        self.questionnaire_rows.append(asdict(row))

    def log_recall_response(self, row: RecallResponseRow) -> None:
        self.recall_rows.append(asdict(row))

    def log_segment_rating(self, row: SegmentRatingRow) -> None:
        self.segment_rating_rows.append(asdict(row))

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
            output_dir / "learning_cycle_questionnaire_responses.csv",
            self.QUESTIONNAIRE_FIELDS,
            self.questionnaire_rows,
        )
        self._write_csv(
            output_dir / "learning_cycle_recall_responses.csv",
            self.RECALL_FIELDS,
            self.recall_rows,
        )
        self._write_csv(
            output_dir / "learning_cycle_segment_ratings.csv",
            self.SEGMENT_RATING_FIELDS,
            self.segment_rating_rows,
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
        self.mouse = None
        self.segment_rating_boxes = []
        self.segment_rating_labels = []
        self.segment_rating_hint = None

    def run(self) -> Path:
        self._prepare_psychopy()
        output_dir = self.context.output_dir / "learning_cycle"
        output_dir.mkdir(parents=True, exist_ok=True)
        config_path = output_dir / "learning_cycle_config.json"
        order_path = output_dir / "learning_cycle_order.csv"

        task_error: BaseException | None = None

        try:
            self._emit_event(
                trial_number=0,
                trial=None,
                event_name="task_start",
                event_code=LEARNING_CYCLE["task_start"],
                detail=f"counterbalance_row={self.counterbalance_row}",
            )
            if self.config.show_task_intro:
                self._show_task_intro()
            for trial_number, trial in enumerate(self.ordered_trials, start=1):
                self._run_trial(trial_number, trial)
                if (
                    trial_number < len(self.ordered_trials)
                    and self.config.inter_trial_rest_seconds > 0
                ):
                    self._run_inter_trial_rest(trial_number)
            self._emit_event(
                trial_number="END",
                trial=None,
                event_name="task_end",
                event_code=LEARNING_CYCLE["task_end"],
                detail=f"completed_trials={len(self.ordered_trials)}",
            )
            if self.config.show_completion:
                self._show_completion()
        except BaseException as exc:
            task_error = exc
        finally:
            self.logger.write_outputs(output_dir)
            self._write_order_snapshot(order_path)
            self._write_config_snapshot(config_path)

        if task_error is not None:
            raise task_error

        return output_dir / "learning_cycle_trial_log.csv"

    def _emit_event(
        self,
        trial_number: int | str,
        trial: LearningTrialSpec | None,
        event_name: str,
        event_code: int,
        detail: str = "",
        name: str | None = None,
    ) -> float:
        record = self.context.trigger.emit(
            name=name or f"learning_cycle.{event_name}",
            code=event_code,
            width_ms=DEFAULT_TRIGGER_WIDTH_MS,
        )
        self.logger.log_event(
            trial_number=trial_number,
            trial=trial,
            event_name=event_name,
            event_code=event_code,
            timestamp=record.timestamp,
            detail=detail,
        )
        return record.timestamp

    def _prepare_psychopy(self) -> None:
        configure_macos_psychopy_runtime()
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
        self._force_mouse_visible()
        self.global_clock = core.Clock()
        self.mouse = event.Mouse(win=self.window)
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
        self.segment_rating_boxes = []
        self.segment_rating_labels = []
        spacing = 0.14
        start_x = -((self.config.segment_rating_max - self.config.segment_rating_min) * spacing) / 2
        for index, rating_value in enumerate(
            range(self.config.segment_rating_min, self.config.segment_rating_max + 1)
        ):
            x_position = start_x + (index * spacing)
            self.segment_rating_boxes.append(
                visual.Rect(
                    win=self.window,
                    width=0.11,
                    height=0.11,
                    pos=(x_position, -0.16),
                    lineColor="white",
                    fillColor="#1a1a1a",
                    colorSpace="named",
                )
            )
            self.segment_rating_labels.append(
                visual.TextStim(
                    win=self.window,
                    text=str(rating_value),
                    font=self.config.font,
                    color="white",
                    colorSpace="named",
                    height=0.045,
                    pos=(x_position, -0.16),
                )
            )
        self.segment_rating_hint = visual.TextStim(
            win=self.window,
            text=(
                f"{self.config.segment_rating_min} = 最低     "
                f"{self.config.segment_rating_max} = 最高\n"
                "可点击条块，或按键盘数字 1-5。"
            ),
            font=self.config.font,
            color=self.config.text_color,
            colorSpace="named",
            height=detail_height,
            pos=(0, -0.32),
            wrapWidth=text_wrap_width,
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

        if self.config.expected_trials != 6:
            return

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
        self._wait_for_space(
            main_text=(
                "视频学习任务\n\n"
                f"共 {len(self.ordered_trials)} 个试次。\n"
                "每个试次都包含前测、视频播放和后测。\n"
                "前测和后测都按照“先口头复述，再完成 10 道判断题”的顺序进行。"
            ),
            subtitle_text=(
                "实验中会为您播放一段视频。\n"
                "视频会按 3 分钟切分，并在段间和播放结束后出现 1-5 评分条。"
            ),
            detail_text="视频开始和结束会记录 EEG 事件。按空格开始，Esc 中止。",
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
                "请先进行口头复述，再完成 10 道判断题。"
            ),
        )

        video_status, video_duration_seconds = self._run_video_phase(trial_number, trial)

        if self.config.include_rating_phase:
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
        else:
            rating_outcome = QuestionnaireOutcome(status="skipped", form_file="")

        posttest_outcome = self._run_questionnaire_phase(
            trial_number=trial_number,
            trial=trial,
            phase_name="posttest",
            event_code=LEARNING_CYCLE["posttest_start"],
            form_file=trial.posttest_form,
            prompt_title="后测测验",
            prompt_body=(
                "请先复述你对刚刚视频内容的理解，再完成 10 道判断题。"
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
        resolved_form = self._resolve_form_path(form_file)
        self._emit_event(
            trial_number=trial_number,
            trial=trial,
            event_name=f"{phase_name}_start",
            event_code=event_code,
            detail=resolved_form,
            name=f"learning_cycle.{phase_name}_start",
        )

        questionnaire_items = self._load_questionnaire_items(resolved_form)
        if phase_name in {"pretest", "posttest"} and questionnaire_items:
            if len(questionnaire_items) < 10:
                raise ValueError(
                    f"{phase_name} requires 10 questionnaire items, found {len(questionnaire_items)}: {resolved_form}"
                )
            questionnaire_items = questionnaire_items[:10]
        include_recall = phase_name in {"pretest", "posttest"}
        if include_recall:
            recall_status = self._run_recall_phase(
                trial_number=trial_number,
                trial=trial,
                phase_name=phase_name,
            )
        else:
            recall_status = "not_applicable"

        if questionnaire_items:
            self._wait_for_space(
                main_text=(
                    f"{prompt_title}\n\n"
                    f"Trial {trial_number} / {len(self.ordered_trials)}\n"
                    f"主题: {trial.topic}\n"
                    f"负荷等级: {trial.load_level}"
                ),
                subtitle_text=prompt_body,
                detail_text=(
                    "小测部分使用 F=对，J=错。\n"
                    f"每题流程：陈述 {self._format_seconds(self.config.statement_seconds)} + "
                    f"作答 {self._format_seconds(self.config.response_seconds)} + "
                    f"间隔 {self._format_seconds(self.config.question_rest_seconds)}。按空格开始。"
                ),
            )
            self._run_true_false_questionnaire(
                trial_number=trial_number,
                trial=trial,
                phase_name=phase_name,
                form_file=resolved_form,
                items=questionnaire_items,
            )
            questionnaire_status = "form_completed"
        else:
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
            questionnaire_status = "placeholder_completed"

        self._show_blank(self.config.post_phase_blank_seconds)
        combined_status = questionnaire_status
        if include_recall:
            combined_status = f"{questionnaire_status}+{recall_status}"
        return QuestionnaireOutcome(status=combined_status, form_file=resolved_form)

    def _load_questionnaire_items(self, resolved_form: str) -> list[QuestionnaireItem]:
        if not resolved_form:
            return []

        form_path = Path(resolved_form)
        if not form_path.exists() or form_path.suffix.lower() != ".csv":
            return []

        with form_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            required_columns = {"item_number", "question_text", "correct_answer"}
            missing = required_columns - set(reader.fieldnames or [])
            if missing:
                raise ValueError(
                    f"Questionnaire file is missing columns {sorted(missing)}: {form_path}"
                )

            items: list[QuestionnaireItem] = []
            for raw_row in reader:
                question_text = raw_row["question_text"].strip()
                if not question_text:
                    continue

                items.append(
                    QuestionnaireItem(
                        item_number=int(raw_row["item_number"]),
                        question_text=question_text,
                        correct_answer=self._normalize_true_false_answer(
                            raw_row["correct_answer"]
                        ),
                        question_type=raw_row.get("question_type", "true_false").strip()
                        or "true_false",
                    )
                )

        for item in items:
            if item.question_type != "true_false":
                raise ValueError(
                    f"Unsupported questionnaire item type '{item.question_type}' in {form_path}"
                )

        return sorted(items, key=lambda item: item.item_number)

    @staticmethod
    def _normalize_true_false_answer(raw_answer: str) -> str:
        normalized = raw_answer.strip().lower()
        if normalized in {"对", "true", "t", "yes", "y", "1"}:
            return "true"
        if normalized in {"错", "false", "f", "no", "n", "0"}:
            return "false"
        raise ValueError(f"Unsupported true/false answer value: {raw_answer}")

    def _run_true_false_questionnaire(
        self,
        trial_number: int,
        trial: LearningTrialSpec,
        phase_name: str,
        form_file: str,
        items: list[QuestionnaireItem],
    ) -> None:
        for item in items:
            self._emit_event(
                trial_number=trial_number,
                trial=trial,
                event_name=f"{phase_name}_question_onset",
                event_code=LEARNING_CYCLE["question_onset"],
                detail=f"item={item.item_number}",
                name=f"learning_cycle.{phase_name}.question_onset",
            )
            self._show_question_statement(
                trial_number=trial_number,
                trial=trial,
                phase_name=phase_name,
                item=item,
                total_items=len(items),
            )
            participant_answer, response_time = self._collect_true_false_response(
                trial_number=trial_number,
                trial=trial,
                phase_name=phase_name,
                item=item,
                total_items=len(items),
            )
            self._emit_event(
                trial_number=trial_number,
                trial=trial,
                event_name=f"{phase_name}_question_response",
                event_code=LEARNING_CYCLE["question_response"],
                detail=(
                    f"item={item.item_number}|answer={participant_answer or 'timeout'}|"
                    f"rt={response_time:.6f}"
                ),
                name=f"learning_cycle.{phase_name}.question_response",
            )
            self.logger.log_questionnaire_response(
                QuestionnaireResponseRow(
                    TrialNumber=trial_number,
                    ItemId=trial.item_id,
                    PhaseName=phase_name,
                    FormFile=form_file,
                    ItemNumber=item.item_number,
                    QuestionType=item.question_type,
                    QuestionText=item.question_text,
                    CorrectAnswer=item.correct_answer,
                    ParticipantAnswer=participant_answer,
                    IsCorrect=int(participant_answer == item.correct_answer),
                    ResponseTime=f"{response_time:.6f}",
                )
            )
            self._show_blank(self.config.question_rest_seconds)

    def _show_question_statement(
        self,
        trial_number: int,
        trial: LearningTrialSpec,
        phase_name: str,
        item: QuestionnaireItem,
        total_items: int,
    ) -> None:
        if self.config.statement_seconds <= 0:
            return

        statement_clock = self.core.Clock()
        phase_label = {
            "pretest": "前测",
            "rating": "主观量表",
            "posttest": "后测",
        }.get(phase_name, phase_name)
        self.event.clearEvents()

        while statement_clock.getTime() < self.config.statement_seconds:
            self._ensure_escape_not_pressed()
            self._draw_text_page(
                main_text=(
                    f"{phase_label}题目 {item.item_number} / {total_items}\n\n"
                    f"{item.question_text}"
                ),
                subtitle_text=(
                    f"Trial {trial_number} / {len(self.ordered_trials)}   "
                    f"主题: {trial.topic}"
                ),
                detail_text="请阅读陈述。",
            )
            self.window.flip()

    def _collect_true_false_response(
        self,
        trial_number: int,
        trial: LearningTrialSpec,
        phase_name: str,
        item: QuestionnaireItem,
        total_items: int,
    ) -> tuple[str, float]:
        if self.config.response_seconds <= 0:
            return "", 0.0

        response_clock = self.core.Clock()
        self.event.clearEvents()
        phase_label = {
            "pretest": "前测",
            "rating": "主观量表",
            "posttest": "后测",
        }.get(phase_name, phase_name)

        while True:
            keys = self.event.getKeys(keyList=["f", "j", "escape"], timeStamped=response_clock)
            for key, response_time in keys:
                if key == "escape":
                    raise TaskAborted("Experiment aborted by user.")
                if key == "f":
                    return "true", response_time
                if key == "j":
                    return "false", response_time
            if (
                self.config.response_seconds > 0
                and response_clock.getTime() >= self.config.response_seconds
            ):
                return "", self.config.response_seconds

            self._draw_text_page(
                main_text=(
                    f"{phase_label}题目 {item.item_number} / {total_items}\n\n"
                    f"{item.question_text}"
                ),
                subtitle_text=(
                    f"Trial {trial_number} / {len(self.ordered_trials)}   "
                    f"主题: {trial.topic}"
                ),
                detail_text="F = 对    J = 错",
            )
            self.window.flip()

    def _run_recall_phase(
        self,
        trial_number: int,
        trial: LearningTrialSpec,
        phase_name: str,
    ) -> str:
        material_label = trial.topic
        prompt_text = self._recall_prompt_text(phase_name, material_label)

        self._wait_for_space(
            main_text="复述任务",
            subtitle_text=prompt_text,
            detail_text="请按空格后开始描述。如果不了解，可报告不了解。",
        )

        self._emit_event(
            trial_number=trial_number,
            trial=trial,
            event_name=f"{phase_name}_recall_start",
            event_code=LEARNING_CYCLE["recall_start"],
            detail=material_label,
            name=f"learning_cycle.{phase_name}.recall_start",
        )
        duration_seconds = self._run_recall_recording_prompt(
            phase_name=phase_name,
            material_label=material_label,
        )
        self._emit_event(
            trial_number=trial_number,
            trial=trial,
            event_name=f"{phase_name}_recall_end",
            event_code=LEARNING_CYCLE["recall_end"],
            detail=f"{material_label}|duration={duration_seconds:.6f}",
            name=f"learning_cycle.{phase_name}.recall_end",
        )
        self.logger.log_recall_response(
            RecallResponseRow(
                TrialNumber=trial_number,
                ItemId=trial.item_id,
                PhaseName=phase_name,
                MaterialLabel=material_label,
                PromptText=prompt_text,
                DurationSeconds=f"{duration_seconds:.6f}",
            )
        )
        return "recall_completed"

    @staticmethod
    def _recall_prompt_text(phase_name: str, material_label: str) -> str:
        if phase_name == "pretest":
            return (
                f"请你描述你对待播视频已知的内容。\n"
                f"素材为：{material_label}。"
            )
        if phase_name == "posttest":
            return (
                f"请你描述你对刚刚视频内容的理解。\n"
                f"素材为：{material_label}。"
            )
        return f"请你描述你对该材料的理解。\n素材为：{material_label}。"

    @staticmethod
    def _format_seconds(seconds: float) -> str:
        value = float(seconds)
        if value.is_integer():
            return f"{int(value)} 秒"
        return f"{value:.1f} 秒"

    def _run_recall_recording_prompt(
        self,
        phase_name: str,
        material_label: str,
    ) -> float:
        recall_clock = self.core.Clock()
        self.event.clearEvents()
        phase_label = {
            "pretest": "前测",
            "posttest": "后测",
        }.get(phase_name, phase_name)

        if self.config.auto_advance:
            self._draw_text_page(
                main_text=f"{phase_label}复述中",
                subtitle_text=f"素材：{material_label}",
                detail_text="自动模式：已跳过口头复述。",
            )
            self.window.flip()
            self.core.wait(0.1)
            return 0.0

        while True:
            keys = self.event.getKeys(keyList=["space", "return", "escape"])
            if "escape" in keys:
                raise TaskAborted("Experiment aborted by user.")
            if "space" in keys or "return" in keys:
                return recall_clock.getTime()

            self._draw_text_page(
                main_text=f"{phase_label}复述中",
                subtitle_text=(
                    f"素材：{material_label}\n"
                    "请开始口头描述。"
                ),
                detail_text="完成描述后按空格继续。",
            )
            self.window.flip()

    def _run_video_phase(
        self,
        trial_number: int,
        trial: LearningTrialSpec,
    ) -> tuple[str, float]:
        video_path = self._resolve_video_path(trial.video_file)
        if Path(video_path).exists():
            try:
                with tempfile.TemporaryDirectory(
                    prefix=f"learning_cycle_segments_{trial.item_id}_"
                ) as cache_dir:
                    segment_paths = self._prepare_video_segments(
                        video_path=video_path,
                        cache_dir=Path(cache_dir),
                    )
                    self._emit_event(
                        trial_number=trial_number,
                        trial=trial,
                        event_name="video_start",
                        event_code=LEARNING_CYCLE["video_start"],
                        detail=f"{video_path}|segments={len(segment_paths)}",
                        name="learning_cycle.video_start",
                    )

                    elapsed_seconds = 0.0
                    segment_statuses: list[str] = []
                    total_segments = len(segment_paths)
                    for segment_index, segment_path in enumerate(segment_paths, start=1):
                        segment_status, segment_elapsed_seconds = self._play_video_file(
                            str(segment_path)
                        )
                        segment_statuses.append(segment_status)
                        elapsed_seconds += segment_elapsed_seconds

                        rating_moment = (
                            "final"
                            if segment_index == total_segments
                            else "between_segments"
                        )
                        if segment_index == total_segments:
                            self._emit_event(
                                trial_number=trial_number,
                                trial=trial,
                                event_name="video_end",
                                event_code=LEARNING_CYCLE["video_end"],
                                detail=(
                                    f"{video_path}|segments={total_segments}|"
                                    f"status={','.join(segment_statuses)}|"
                                    f"elapsed={elapsed_seconds:.6f}"
                                ),
                                name="learning_cycle.video_end",
                            )

                        self._collect_segment_rating(
                            trial_number=trial_number,
                            trial=trial,
                            segment_index=segment_index,
                            total_segments=total_segments,
                            segment_file=str(segment_path),
                            rating_moment=rating_moment,
                        )

                    status = "played_segmented"
            except TaskAborted:
                raise
            except Exception as exc:
                error_detail = self._summarize_video_error(exc)
                self._emit_event(
                    trial_number=trial_number,
                    trial=trial,
                    event_name="video_start",
                    event_code=LEARNING_CYCLE["video_start"],
                    detail=video_path,
                    name="learning_cycle.video_start",
                )
                elapsed_seconds = self._run_missing_video_placeholder(
                    trial_number,
                    trial,
                    video_path,
                    reason_text=(
                        "当前设备无法正常创建视频播放后端，已切换为占位播放以继续联调。\n"
                        f"失败原因：{error_detail}"
                    ),
                )
                status = "placeholder_unplayable_video"
                self._emit_event(
                    trial_number=trial_number,
                    trial=trial,
                    event_name="video_end",
                    event_code=LEARNING_CYCLE["video_end"],
                    detail=f"{video_path}|{status}|{elapsed_seconds:.6f}",
                    name="learning_cycle.video_end",
                )
        else:
            self._emit_event(
                trial_number=trial_number,
                trial=trial,
                event_name="video_start",
                event_code=LEARNING_CYCLE["video_start"],
                detail=video_path,
                name="learning_cycle.video_start",
            )
            elapsed_seconds = self._run_missing_video_placeholder(
                trial_number,
                trial,
                video_path,
            )
            status = "placeholder_missing_video"
            self._emit_event(
                trial_number=trial_number,
                trial=trial,
                event_name="video_end",
                event_code=LEARNING_CYCLE["video_end"],
                detail=f"{video_path}|{status}|{elapsed_seconds:.6f}",
                name="learning_cycle.video_end",
            )

        self._show_blank(self.config.post_phase_blank_seconds)
        return status, elapsed_seconds

    def _play_video_file(self, video_path: str) -> tuple[str, float]:
        movie_stim = None
        playback_clock = self.core.Clock()
        self.event.clearEvents()

        try:
            with self._suppress_movie_backend_stderr():
                try:
                    movie_stim, status = self._build_movie_stim(video_path)
                    while True:
                        self._ensure_escape_not_pressed()
                        movie_stim.draw()
                        self.window.flip()
                        if self._movie_finished(movie_stim):
                            break
                except Exception:
                    if not self._ffplay_available():
                        raise
                    self._play_video_with_ffplay(video_path)
                    status = "played_ffplay"
        finally:
            self._safe_close_movie_stim(movie_stim)

        return status, playback_clock.getTime()

    def _build_movie_stim(self, video_path: str):
        errors: list[str] = []
        for status, backend_name, factory in self._movie_stim_attempts(video_path):
            try:
                return factory(), status
            except Exception as exc:  # pragma: no cover - depends on local video backend
                errors.append(f"{backend_name}: {self._summarize_video_error(exc)}")

        raise RuntimeError(
            "Unable to create a PsychoPy movie stimulus. "
            f"Tried MovieStim backends for: {video_path}. Errors: {errors}"
        )

    def _movie_stim_attempts(self, video_path: str):
        attempts: list[tuple[str, str, object]] = []
        attempts.append(
            (
                "played_vlc",
                "VlcMovieStim(audio)",
                lambda: self._create_vlc_movie_stim(video_path, no_audio=False),
            )
        )

        attempts.append(
            (
                "played_ffpyplayer",
                "MovieStim(ffpyplayer+audio)",
                lambda: self._create_ffpyplayer_movie_stim(video_path, no_audio=False),
            )
        )

        if self._allow_silent_video_fallback():
            attempts.append(
                (
                    "played_vlc_silent",
                    "VlcMovieStim(silent)",
                    lambda: self._create_vlc_movie_stim(video_path, no_audio=True),
                )
            )
            attempts.append(
                (
                    "played_ffpyplayer_silent",
                    "MovieStim(ffpyplayer+silent)",
                    lambda: self._create_ffpyplayer_movie_stim(video_path, no_audio=True),
                )
            )

        return attempts

    def _allow_silent_video_fallback(self) -> bool:
        return True

    def _create_ffpyplayer_movie_stim(self, video_path: str, no_audio: bool):
        stim_class = getattr(self.visual, "MovieStim", None)
        if stim_class is None:
            raise RuntimeError("PsychoPy MovieStim is not available in this environment.")
        if no_audio:
            movie_stim = stim_class(
                self.window,
                filename="",
                movieLib="ffpyplayer",
                audioLib="sdl2",
                noAudio=True,
                autoStart=True,
            )
            movie_stim._decoderOpts["an"] = True
            movie_stim.loadMovie(video_path)
            return movie_stim
        return stim_class(
            self.window,
            filename=video_path,
            movieLib="ffpyplayer",
            audioLib="sdl2",
            noAudio=no_audio,
            autoStart=True,
        )

    def _create_vlc_movie_stim(self, video_path: str, no_audio: bool):
        from psychopy.visual.vlcmoviestim import VlcMovieStim  # type: ignore

        return VlcMovieStim(
            self.window,
            filename=video_path,
            noAudio=no_audio,
            autoStart=True,
        )

    @staticmethod
    def _ffplay_available() -> bool:
        return shutil.which("ffplay") is not None

    def _play_video_with_ffplay(self, video_path: str) -> None:
        command = [
            "ffplay",
            "-autoexit",
            "-fs",
            "-loglevel",
            "error",
            video_path,
        ]
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            error_text = completed.stderr.strip() or completed.stdout.strip()
            raise RuntimeError(f"ffplay playback failed: {error_text}")

    def _movie_finished(self, movie_stim) -> bool:
        finished_flag = getattr(movie_stim, "isFinished", None)
        if isinstance(finished_flag, bool):
            return finished_flag
        status = getattr(movie_stim, "status", None)
        finished_constant = getattr(self.visual, "FINISHED", None)
        if finished_constant is not None and status == finished_constant:
            return True
        return False

    def _prepare_video_segments(
        self,
        video_path: str,
        cache_dir: Path,
    ) -> list[Path]:
        output_pattern = cache_dir / "segment_%03d.mp4"
        segment_seconds = max(1, int(self.config.segment_seconds))
        command = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            video_path,
            "-map",
            "0:v:0",
            "-map",
            "0:a?",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-crf",
            "23",
            "-pix_fmt",
            "yuv420p",
            "-force_key_frames",
            f"expr:gte(t,n_forced*{segment_seconds})",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-f",
            "segment",
            "-segment_time",
            str(segment_seconds),
            "-segment_format_options",
            "movflags=+faststart",
            "-reset_timestamps",
            "1",
            str(output_pattern),
        ]
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            error_text = completed.stderr.strip() or completed.stdout.strip()
            raise RuntimeError(f"ffmpeg segmenting failed: {error_text}")

        segment_paths = sorted(cache_dir.glob("segment_*.mp4"))
        if not segment_paths:
            raise RuntimeError("ffmpeg segmenting produced no playable segments.")
        return segment_paths

    def _collect_segment_rating(
        self,
        trial_number: int,
        trial: LearningTrialSpec,
        segment_index: int,
        total_segments: int,
        segment_file: str,
        rating_moment: str,
    ) -> None:
        response_clock = self.core.Clock()
        self.event.clearEvents()
        self.mouse.clickReset()
        previous_buttons = self.mouse.getPressed()
        rating_values = list(
            range(self.config.segment_rating_min, self.config.segment_rating_max + 1)
        )
        key_to_rating = {str(value): value for value in rating_values}
        key_to_rating.update({f"num_{value}": value for value in rating_values})
        self._emit_event(
            trial_number=trial_number,
            trial=trial,
            event_name="segment_rating_start",
            event_code=LEARNING_CYCLE["segment_rating_start"],
            detail=(
                f"segment={segment_index}/{total_segments}|moment={rating_moment}|"
                f"file={Path(segment_file).name}"
            ),
            name="learning_cycle.segment_rating_start",
        )

        while True:
            self._ensure_escape_not_pressed()
            keys = self.event.getKeys(
                keyList=list(key_to_rating.keys()) + ["escape"],
                timeStamped=response_clock,
            )
            for key, response_time in keys:
                if key == "escape":
                    raise TaskAborted("Experiment aborted by user.")
                rating_value = key_to_rating[key]
                self._emit_event(
                    trial_number=trial_number,
                    trial=trial,
                    event_name="segment_rating_response",
                    event_code=LEARNING_CYCLE["segment_rating_response"],
                    detail=(
                        f"segment={segment_index}/{total_segments}|rating={rating_value}|"
                        f"rt={response_time:.6f}|moment={rating_moment}"
                    ),
                    name="learning_cycle.segment_rating_response",
                )
                self.logger.log_segment_rating(
                    SegmentRatingRow(
                        TrialNumber=trial_number,
                        ItemId=trial.item_id,
                        Topic=trial.topic,
                        SegmentIndex=segment_index,
                        TotalSegments=total_segments,
                        RatingValue=rating_value,
                        ResponseTime=f"{response_time:.6f}",
                        SegmentFile=segment_file,
                        RatingMoment=rating_moment,
                    )
                )
                return

            buttons = self.mouse.getPressed()
            if buttons != previous_buttons:
                for rating_value, box in zip(rating_values, self.segment_rating_boxes):
                    if box.contains(self.mouse) and buttons[0]:
                        self._emit_event(
                            trial_number=trial_number,
                            trial=trial,
                            event_name="segment_rating_response",
                            event_code=LEARNING_CYCLE["segment_rating_response"],
                            detail=(
                                f"segment={segment_index}/{total_segments}|rating={rating_value}|"
                                f"rt={response_clock.getTime():.6f}|moment={rating_moment}"
                            ),
                            name="learning_cycle.segment_rating_response",
                        )
                        self.logger.log_segment_rating(
                            SegmentRatingRow(
                                TrialNumber=trial_number,
                                ItemId=trial.item_id,
                                Topic=trial.topic,
                                SegmentIndex=segment_index,
                                TotalSegments=total_segments,
                                RatingValue=rating_value,
                                ResponseTime=f"{response_clock.getTime():.6f}",
                                SegmentFile=segment_file,
                                RatingMoment=rating_moment,
                            )
                        )
                        return
            previous_buttons = buttons

            self._draw_segment_rating_page(segment_index, total_segments, rating_moment)
            self.window.flip()

    def _draw_segment_rating_page(
        self,
        segment_index: int,
        total_segments: int,
        rating_moment: str,
    ) -> None:
        if rating_moment == "final":
            self.title_stim.text = self._wrap_for_stim(self.title_stim, "视频播放结束")
            self.subtitle_stim.text = self._wrap_for_stim(
                self.subtitle_stim,
                f"请对第 {segment_index} 段 / 共 {total_segments} 段视频进行评分。",
            )
        else:
            self.title_stim.text = self._wrap_for_stim(self.title_stim, "片段播放结束")
            self.subtitle_stim.text = self._wrap_for_stim(
                self.subtitle_stim,
                f"请对第 {segment_index} 段 / 共 {total_segments} 段视频进行评分。",
            )
        self.detail_stim.text = ""
        self.title_stim.draw()
        self.subtitle_stim.draw()
        for box, label in zip(self.segment_rating_boxes, self.segment_rating_labels):
            box.draw()
            label.draw()
        self.segment_rating_hint.draw()

    def _run_missing_video_placeholder(
        self,
        trial_number: int,
        trial: LearningTrialSpec,
        video_path: str,
        reason_text: str | None = None,
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
                    "当前视频无法正常播放，使用占位播放窗口继续联调。"
                ),
                detail_text=(
                    f"{reason_text or '视频文件不存在或暂未接入。'}\n"
                    f"视频路径: {video_path}\n"
                    f"计划时长: {trial.planned_minutes:.2f} 分钟\n"
                    f"占位时长: {placeholder_seconds:.1f} 秒"
                ),
            )
            self.window.flip()

        return start_clock.getTime()

    def _show_completion(self) -> None:
        self._wait_for_space(
            main_text=(
                "视频学习任务结束\n\n"
                f"已完成 {len(self.ordered_trials)} 个试次。"
            ),
            subtitle_text="日志已保存，可继续检查问卷接口和视频素材配置。",
            detail_text="按空格结束。",
        )

    def _run_inter_trial_rest(self, completed_trial_number: int) -> None:
        rest_seconds = self.config.inter_trial_rest_seconds
        if rest_seconds <= 0:
            return

        rest_clock = self.core.Clock()
        self.event.clearEvents()
        while rest_clock.getTime() < rest_seconds:
            self._ensure_escape_not_pressed()
            remaining_seconds = max(0, int(rest_seconds - rest_clock.getTime()))
            self._draw_text_page(
                main_text=(
                    "组间休息\n\n"
                    f"已完成 {completed_trial_number} / {len(self.ordered_trials)} 组。"
                ),
                subtitle_text="请放松休息，等待下一组视频学习任务。",
                detail_text=f"剩余约 {remaining_seconds} 秒。",
            )
            self.window.flip()

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
        self.title_stim.text = self._wrap_for_stim(self.title_stim, main_text)
        self.subtitle_stim.text = self._wrap_for_stim(self.subtitle_stim, subtitle_text)
        self.detail_stim.text = self._wrap_for_stim(self.detail_stim, detail_text)
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

    @staticmethod
    def _summarize_video_error(exc: BaseException) -> str:
        message = str(exc).strip() or exc.__class__.__name__
        return " ".join(message.split())

    @staticmethod
    def _safe_close_movie_stim(movie_stim) -> None:
        if movie_stim is None:
            return
        for method_name, args in (
            ("stop", ()),
            ("pause", (True,)),
            ("unload", ()),
            ("close", ()),
        ):
            method = getattr(movie_stim, method_name, None)
            if callable(method):
                try:
                    method(*args)
                except Exception:
                    pass

    @contextmanager
    def _suppress_movie_backend_stderr(self):
        saved_stderr_fd = None
        devnull_fd = None
        try:
            saved_stderr_fd = os.dup(2)
            devnull_fd = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull_fd, 2)
        except OSError:
            saved_stderr_fd = None
            devnull_fd = None

        try:
            yield
        finally:
            if saved_stderr_fd is not None:
                try:
                    os.dup2(saved_stderr_fd, 2)
                except OSError:
                    pass
                os.close(saved_stderr_fd)
            if devnull_fd is not None:
                os.close(devnull_fd)

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
