from __future__ import annotations

import csv
import json
import random
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

from common.data_io import ExperimentContext
from config.event_codes import MENTAL_ARITHMETIC
from config.settings import (
    MENTAL_ARITHMETIC_ALLOW_GUI,
    MENTAL_ARITHMETIC_BACKGROUND_COLOR,
    MENTAL_ARITHMETIC_FIXATION_SECONDS,
    MENTAL_ARITHMETIC_FONT,
    MENTAL_ARITHMETIC_FORCE_MOUSE_VISIBLE,
    MENTAL_ARITHMETIC_FULLSCREEN,
    MENTAL_ARITHMETIC_INTER_TRIAL_SECONDS,
    MENTAL_ARITHMETIC_Q_RULES,
    MENTAL_ARITHMETIC_RANDOM_SEED,
    MENTAL_ARITHMETIC_RESPONSE_TIMEOUT_SECONDS,
    MENTAL_ARITHMETIC_TEXT_COLOR,
    MENTAL_ARITHMETIC_TRIALS_PER_LEVEL,
    MENTAL_ARITHMETIC_WINDOW_SIZE,
)

EXPECTED_DIFFICULTY_LEVELS = ("QE", "QM", "QH")


@dataclass(frozen=True)
class DifficultyRule:
    level: str
    min_q: float
    max_q: float | None
    digit_pairs: tuple[tuple[int, int], ...]

    def matches(self, q_value: float) -> bool:
        if q_value < self.min_q:
            return False
        if self.max_q is not None and q_value >= self.max_q:
            return False
        return True


@dataclass(frozen=True)
class ArithmeticProblem:
    difficulty_level: str
    left_operand: int
    right_operand: int
    question: str
    correct_answer: int
    q_value: float
    carry_count: int
    digit_complexity: int


@dataclass(frozen=True)
class TrialResult:
    TrialNumber: int
    DifficultyLevel: str
    Question: str
    CorrectAnswer: int
    ParticipantAnswer: str
    ResponseTime: str
    QValue: float
    CarryCount: int
    ParticipantCorrect: int


@dataclass
class MentalArithmeticConfig:
    fullscreen: bool = MENTAL_ARITHMETIC_FULLSCREEN
    allow_gui: bool = MENTAL_ARITHMETIC_ALLOW_GUI
    force_mouse_visible: bool = MENTAL_ARITHMETIC_FORCE_MOUSE_VISIBLE
    window_size: tuple[int, int] = MENTAL_ARITHMETIC_WINDOW_SIZE
    background_color: str = MENTAL_ARITHMETIC_BACKGROUND_COLOR
    text_color: str = MENTAL_ARITHMETIC_TEXT_COLOR
    font: str = MENTAL_ARITHMETIC_FONT
    fixation_seconds: float = MENTAL_ARITHMETIC_FIXATION_SECONDS
    inter_trial_seconds: float = MENTAL_ARITHMETIC_INTER_TRIAL_SECONDS
    response_timeout_seconds: float = MENTAL_ARITHMETIC_RESPONSE_TIMEOUT_SECONDS
    random_seed: int | None = MENTAL_ARITHMETIC_RANDOM_SEED
    trial_counts: dict[str, int] = field(
        default_factory=lambda: dict(MENTAL_ARITHMETIC_TRIALS_PER_LEVEL)
    )
    difficulty_rule_specs: dict[str, dict[str, object]] = field(
        default_factory=lambda: {
            level: {
                "min_q": spec["min_q"],
                "max_q": spec["max_q"],
                "digit_pairs": tuple(spec["digit_pairs"]),
            }
            for level, spec in MENTAL_ARITHMETIC_Q_RULES.items()
        }
    )
    auto_advance: bool = False

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if len(self.window_size) != 2 or any(size <= 0 for size in self.window_size):
            raise ValueError("window_size must contain two positive integers.")

        for field_name in (
            "fixation_seconds",
            "inter_trial_seconds",
            "response_timeout_seconds",
        ):
            if getattr(self, field_name) < 0:
                raise ValueError(f"{field_name} must be non-negative.")

        unknown_trial_levels = set(self.trial_counts) - set(EXPECTED_DIFFICULTY_LEVELS)
        if unknown_trial_levels:
            raise ValueError(
                "trial_counts contains unsupported levels: "
                f"{sorted(unknown_trial_levels)}."
            )

        missing_trial_levels = set(EXPECTED_DIFFICULTY_LEVELS) - set(self.trial_counts)
        if missing_trial_levels:
            raise ValueError(
                "trial_counts is missing levels: "
                f"{sorted(missing_trial_levels)}."
            )

        for level, count in self.trial_counts.items():
            if count < 0:
                raise ValueError(f"trial count for {level} must be non-negative.")

        unknown_rule_levels = set(self.difficulty_rule_specs) - set(EXPECTED_DIFFICULTY_LEVELS)
        if unknown_rule_levels:
            raise ValueError(
                "difficulty_rule_specs contains unsupported levels: "
                f"{sorted(unknown_rule_levels)}."
            )

        missing_rule_levels = set(EXPECTED_DIFFICULTY_LEVELS) - set(self.difficulty_rule_specs)
        if missing_rule_levels:
            raise ValueError(
                "difficulty_rule_specs is missing levels: "
                f"{sorted(missing_rule_levels)}."
            )

        for level, spec in self.difficulty_rule_specs.items():
            min_q = float(spec["min_q"])
            max_q = None if spec["max_q"] is None else float(spec["max_q"])
            if max_q is not None and max_q <= min_q:
                raise ValueError(
                    f"Difficulty rule {level} has max_q <= min_q: {min_q}, {max_q}."
                )

            digit_pairs = tuple(spec["digit_pairs"])
            if not digit_pairs:
                raise ValueError(f"Difficulty rule {level} must include digit_pairs.")
            for pair in digit_pairs:
                if len(pair) != 2 or any(int(digit) <= 0 for digit in pair):
                    raise ValueError(
                        f"Difficulty rule {level} contains invalid digit pair: {pair}."
                    )


class TaskAborted(RuntimeError):
    pass


class QValueCalculator:
    @staticmethod
    def carry_count(left_operand: int, right_operand: int) -> int:
        carries = 0
        carry = 0
        left = left_operand
        right = right_operand

        while left > 0 or right > 0:
            digit_sum = (left % 10) + (right % 10) + carry
            if digit_sum >= 10:
                carries += 1
                carry = 1
            else:
                carry = 0
            left //= 10
            right //= 10

        return carries

    @staticmethod
    def digit_complexity(left_operand: int, right_operand: int) -> int:
        left_digits = len(str(left_operand))
        right_digits = len(str(right_operand))
        return (left_digits + right_digits) - 2

    @classmethod
    def q_value(cls, left_operand: int, right_operand: int) -> tuple[float, int, int]:
        carries = cls.carry_count(left_operand, right_operand)
        digit_complexity = cls.digit_complexity(left_operand, right_operand)
        q_value = float(digit_complexity + carries)
        return q_value, carries, digit_complexity


class ProblemGenerator:
    def __init__(self, config: MentalArithmeticConfig):
        self.config = config
        self.random = random.Random(config.random_seed)
        self.rules = {
            level: DifficultyRule(
                level=level,
                min_q=float(spec["min_q"]),
                max_q=None if spec["max_q"] is None else float(spec["max_q"]),
                digit_pairs=tuple(spec["digit_pairs"]),
            )
            for level, spec in config.difficulty_rule_specs.items()
        }

    def generate_problem(self, level: str) -> ArithmeticProblem:
        rule = self.rules[level]
        max_attempts = 5000

        for _ in range(max_attempts):
            left_digits, right_digits = self.random.choice(rule.digit_pairs)
            left_operand = self._random_operand(left_digits)
            right_operand = self._random_operand(right_digits)

            q_value, carry_count, digit_complexity = QValueCalculator.q_value(
                left_operand,
                right_operand,
            )

            if not rule.matches(q_value):
                continue

            return ArithmeticProblem(
                difficulty_level=level,
                left_operand=left_operand,
                right_operand=right_operand,
                question=f"{left_operand} + {right_operand} = ?",
                correct_answer=left_operand + right_operand,
                q_value=q_value,
                carry_count=carry_count,
                digit_complexity=digit_complexity,
            )

        raise RuntimeError(f"Unable to generate a valid problem for difficulty {level}.")

    def generate_problem_set(self) -> list[ArithmeticProblem]:
        problems: list[ArithmeticProblem] = []
        seen_questions: set[str] = set()

        for level, count in self.config.trial_counts.items():
            generated_for_level: list[ArithmeticProblem] = []
            while len(generated_for_level) < count:
                problem = self.generate_problem(level)
                if problem.question in seen_questions:
                    continue
                seen_questions.add(problem.question)
                generated_for_level.append(problem)

            self.random.shuffle(generated_for_level)
            problems.extend(generated_for_level)

        self.random.shuffle(problems)
        return problems

    def _random_operand(self, digits: int) -> int:
        if digits <= 1:
            return self.random.randint(1, 9)
        lower = 10 ** (digits - 1)
        upper = (10**digits) - 1
        return self.random.randint(lower, upper)


class TrialLogger:
    TRIAL_FIELDNAMES = (
        "TrialNumber",
        "DifficultyLevel",
        "Question",
        "CorrectAnswer",
        "ParticipantAnswer",
        "ResponseTime",
        "QValue",
        "CarryCount",
        "ParticipantCorrect",
    )
    EVENT_FIELDNAMES = (
        "TrialNumber",
        "DifficultyLevel",
        "EventName",
        "EventCode",
        "Timestamp",
    )

    def __init__(self) -> None:
        self.trial_rows: list[dict[str, object]] = []
        self.event_rows: list[dict[str, object]] = []

    def log_trial(self, result: TrialResult) -> None:
        self.trial_rows.append(asdict(result))

    def log_event(
        self,
        trial_number: int | str,
        difficulty_level: str,
        event_name: str,
        event_code: int,
        timestamp: float,
    ) -> None:
        self.event_rows.append(
            {
                "TrialNumber": trial_number,
                "DifficultyLevel": difficulty_level,
                "EventName": event_name,
                "EventCode": event_code,
                "Timestamp": f"{timestamp:.6f}",
            }
        )

    def write_outputs(self, output_dir: Path) -> None:
        self._write_csv(
            output_dir / "mental_arithmetic_behavior.csv",
            self.TRIAL_FIELDNAMES,
            self.trial_rows,
        )
        self._write_csv(
            output_dir / "mental_arithmetic_events.csv",
            self.EVENT_FIELDNAMES,
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


class MentalArithmeticTask:
    def __init__(self, context: ExperimentContext, config: MentalArithmeticConfig):
        self.context = context
        self.config = config
        self.generator = ProblemGenerator(config)
        self.logger = TrialLogger()
        self.problems = self.generator.generate_problem_set()
        self.window = None
        self.title_stim = None
        self.subtitle_stim = None
        self.input_stim = None
        self.fixation_stim = None
        self.summary_stim = None
        self.core = None
        self.event = None
        self.visual = None
        self.global_clock = None

    def run(self) -> Path:
        self._prepare_psychopy()
        output_dir = self.context.output_dir / "mental_arithmetic"
        output_dir.mkdir(parents=True, exist_ok=True)
        generated_path = output_dir / "mental_arithmetic_generated_problems.csv"
        config_path = output_dir / "mental_arithmetic_config.json"

        task_error: BaseException | None = None

        try:
            self._show_instructions()
            for trial_number, problem in enumerate(self.problems, start=1):
                self._run_trial(trial_number, problem)
            self._show_completion()
        except BaseException as exc:
            task_error = exc
        finally:
            if self.window is not None:
                self.window.close()
            self.logger.write_outputs(output_dir)
            self._write_generated_problems(generated_path)
            self._write_config_snapshot(config_path)

        if task_error is not None:
            raise task_error

        return output_dir / "mental_arithmetic_behavior.csv"

    def _prepare_psychopy(self) -> None:
        try:
            import psychopy  # type: ignore
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
            wrapWidth=1.4,
        )
        self.subtitle_stim = visual.TextStim(
            win=self.window,
            text="",
            font=self.config.font,
            color=self.config.text_color,
            colorSpace="named",
            height=0.03,
            pos=(0, -0.30),
            wrapWidth=1.4,
        )
        self.input_stim = visual.TextStim(
            win=self.window,
            text="_",
            font=self.config.font,
            color=self.config.text_color,
            colorSpace="named",
            height=0.07,
            pos=(0, -0.08),
        )
        self.fixation_stim = visual.TextStim(
            win=self.window,
            text="+",
            font=self.config.font,
            color=self.config.text_color,
            colorSpace="named",
            height=0.08,
        )
        self.summary_stim = visual.TextStim(
            win=self.window,
            text="",
            font=self.config.font,
            color=self.config.text_color,
            colorSpace="named",
            height=0.04,
            wrapWidth=1.4,
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

    def _show_instructions(self) -> None:
        # EEG Trigger Placeholder: task_start
        self.logger.log_event(
            trial_number=0,
            difficulty_level="NA",
            event_name="task_start",
            event_code=MENTAL_ARITHMETIC["task_start"],
            timestamp=self.global_clock.getTime(),
        )
        # EEG Trigger Placeholder: instruction_start
        self.logger.log_event(
            trial_number=0,
            difficulty_level="NA",
            event_name="instruction_start",
            event_code=MENTAL_ARITHMETIC["instruction_start"],
            timestamp=self.global_clock.getTime(),
        )

        instruction_text = (
            "心算任务\n\n"
            "你将看到一道加法题，请在心中完成计算。\n"
            "使用键盘输入答案，按回车提交。\n"
            "如果输错，可以按退格删除。\n"
            "请尽量又快又准地作答。\n"
            "按空格开始。"
        )

        self._wait_for_key(
            main_text=instruction_text,
            subtitle_text=(
                "按键说明: 数字键输入，Backspace 删除，Enter 提交，Esc 中止。"
            ),
            allowed_keys=("space", "return"),
            auto_advance=self.config.auto_advance,
        )

    def _run_trial(self, trial_number: int, problem: ArithmeticProblem) -> None:
        # EEG Trigger Placeholder: trial_start
        self.logger.log_event(
            trial_number=trial_number,
            difficulty_level=problem.difficulty_level,
            event_name="trial_start",
            event_code=MENTAL_ARITHMETIC["trial_start"],
            timestamp=self.global_clock.getTime(),
        )

        self._run_fixation()

        # EEG Trigger Placeholder: question_onset
        self.logger.log_event(
            trial_number=trial_number,
            difficulty_level=problem.difficulty_level,
            event_name="question_onset",
            event_code=MENTAL_ARITHMETIC["question_onset"],
            timestamp=self.global_clock.getTime(),
        )

        participant_answer, response_time = self._collect_answer(problem, trial_number)
        participant_correct = int(str(problem.correct_answer) == participant_answer)

        self.logger.log_trial(
            TrialResult(
                TrialNumber=trial_number,
                DifficultyLevel=problem.difficulty_level,
                Question=problem.question,
                CorrectAnswer=problem.correct_answer,
                ParticipantAnswer=participant_answer,
                ResponseTime=""
                if response_time is None
                else f"{response_time:.6f}",
                QValue=problem.q_value,
                CarryCount=problem.carry_count,
                ParticipantCorrect=participant_correct,
            )
        )

        # EEG Trigger Placeholder: response
        self.logger.log_event(
            trial_number=trial_number,
            difficulty_level=problem.difficulty_level,
            event_name="response",
            event_code=MENTAL_ARITHMETIC["response"],
            timestamp=self.global_clock.getTime(),
        )

        if self.config.inter_trial_seconds > 0:
            # EEG Trigger Placeholder: inter_trial
            self.logger.log_event(
                trial_number=trial_number,
                difficulty_level=problem.difficulty_level,
                event_name="inter_trial",
                event_code=MENTAL_ARITHMETIC["inter_trial"],
                timestamp=self.global_clock.getTime(),
            )
            self._show_blank(self.config.inter_trial_seconds)

    def _run_fixation(self) -> None:
        phase_clock = self.core.Clock()
        self.event.clearEvents()
        while phase_clock.getTime() < self.config.fixation_seconds:
            self._ensure_escape_not_pressed()
            self.fixation_stim.draw()
            self.window.flip()

    def _collect_answer(
        self,
        problem: ArithmeticProblem,
        trial_number: int,
    ) -> tuple[str, float | None]:
        typed = ""
        self.event.clearEvents()

        self.title_stim.text = (
            f"Trial {trial_number} / {len(self.problems)}\n"
            f"Difficulty: {problem.difficulty_level}\n\n"
            f"{problem.question}"
        )
        self.subtitle_stim.text = "输入答案后按回车提交。"
        self.input_stim.text = "_"

        self.title_stim.draw()
        self.subtitle_stim.draw()
        self.input_stim.draw()
        self.window.flip()

        rt_clock = self.core.Clock()
        while True:
            keys = self.event.getKeys()
            for key in keys:
                normalized = self._normalize_key_name(key)
                if normalized is None:
                    continue
                if normalized == "escape":
                    raise TaskAborted("Experiment aborted by user.")
                if normalized == "backspace":
                    typed = typed[:-1]
                    continue
                if normalized in {"return", "num_enter"}:
                    return typed, rt_clock.getTime()
                typed += normalized

            if (
                self.config.response_timeout_seconds > 0
                and rt_clock.getTime() >= self.config.response_timeout_seconds
            ):
                return typed, None

            self.title_stim.draw()
            self.subtitle_stim.draw()
            self.input_stim.text = typed if typed else "_"
            self.input_stim.draw()
            self.window.flip()

    def _show_completion(self) -> None:
        accuracy = 0.0
        if self.logger.trial_rows:
            accuracy = sum(row["ParticipantCorrect"] for row in self.logger.trial_rows) / len(
                self.logger.trial_rows
            )

        # EEG Trigger Placeholder: task_end
        self.logger.log_event(
            trial_number="END",
            difficulty_level="NA",
            event_name="task_end",
            event_code=MENTAL_ARITHMETIC["task_end"],
            timestamp=self.global_clock.getTime(),
        )

        self._wait_for_key(
            main_text=(
                "任务结束\n\n"
                f"已完成 {len(self.logger.trial_rows)} 题\n"
                f"正确率: {accuracy * 100:.1f}%"
            ),
            subtitle_text="按空格结束。",
            allowed_keys=("space", "return"),
            auto_advance=self.config.auto_advance,
        )

    def _wait_for_key(
        self,
        main_text: str,
        subtitle_text: str,
        allowed_keys: tuple[str, ...],
        auto_advance: bool,
    ) -> None:
        self.event.clearEvents()
        while True:
            if auto_advance:
                return

            keys = self.event.getKeys(keyList=list(allowed_keys) + ["escape"])
            if "escape" in keys:
                raise TaskAborted("Experiment aborted by user.")
            if any(key in keys for key in allowed_keys):
                return

            self.title_stim.text = main_text
            self.subtitle_stim.text = subtitle_text
            self.title_stim.draw()
            self.subtitle_stim.draw()
            self.window.flip()

    def _show_blank(self, seconds: float) -> None:
        blank_clock = self.core.Clock()
        self.event.clearEvents()
        while blank_clock.getTime() < seconds:
            self._ensure_escape_not_pressed()
            self.window.flip()

    def _ensure_escape_not_pressed(self) -> None:
        if "escape" in self.event.getKeys(keyList=["escape"]):
            raise TaskAborted("Experiment aborted by user.")

    @staticmethod
    def _normalize_key_name(key_name: str) -> str | None:
        if key_name.isdigit():
            return key_name
        if key_name.startswith("num_") and key_name[4:].isdigit():
            return key_name[4:]
        if key_name in {"backspace", "return", "num_enter", "escape"}:
            return key_name
        return None

    def _write_generated_problems(self, output_path: Path) -> None:
        rows = [asdict(problem) for problem in self.problems]
        if not rows:
            return
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    def _write_config_snapshot(self, output_path: Path) -> None:
        payload = {
            "config": asdict(self.config),
            "difficulty_rules": self.config.difficulty_rule_specs,
        }
        with output_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)


def run(
    context: ExperimentContext,
    config: MentalArithmeticConfig | None = None,
) -> Path:
    config = config or MentalArithmeticConfig()
    task = MentalArithmeticTask(context=context, config=config)
    return task.run()
