from __future__ import annotations

import argparse
import csv
from pathlib import Path

from common.participant_info import collect_participant_info
from config.settings import (
    LEARNING_CYCLE_INTER_TRIAL_REST_SECONDS,
    LEARNING_CYCLE_PROTOCOL_TRIALS_FILE,
    MENTAL_ARITHMETIC_TEST_BLOCK_COUNT,
    MENTAL_ARITHMETIC_TEST_BLOCK_REST_SECONDS,
    MENTAL_ARITHMETIC_TEST_FIXATION_SECONDS,
    MENTAL_ARITHMETIC_TEST_INTER_TRIAL_SECONDS,
    MENTAL_ARITHMETIC_TEST_PRE_RESPONSE_BLANK_SECONDS,
    MENTAL_ARITHMETIC_TEST_RESPONSE_TIMEOUT_SECONDS,
    MENTAL_ARITHMETIC_TEST_TRIALS_PER_BLOCK,
    MENTAL_ARITHMETIC_TEST_TRIALS_PER_LEVEL,
    REST_TEST_CYCLE_COUNT,
    REST_TEST_EYES_CLOSED_SECONDS,
    REST_TEST_EYES_OPEN_SECONDS,
    WM_PRETEST_TEST_TASK_TIMEOUT_SECONDS,
    ensure_directories,
)
from common.data_io import build_context, cleanup_context
from tasks import DEFAULT_TASK_SLUG, TASK_MAP, TASK_REGISTRY
from tasks.learning_cycle.task import LearningCycleConfig
from tasks.mental_arithmetic.task import MentalArithmeticConfig
from tasks.protocol.task import ProtocolConfig, TEST_STAGE_CHOICES
from tasks.resting_state.task import RestingStateConfig
from tasks.wm_pretest.task import WMPretestConfig

def _build_task_map() -> dict[str, object]:
    return {slug: spec.runner for slug, spec in TASK_MAP.items()}


def _count_condition_rows(trials_file: Path | str) -> int:
    path = Path(trials_file)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def _build_resting_state_config(args: argparse.Namespace) -> RestingStateConfig:
    default_config = RestingStateConfig()
    default_eyes_open = (
        REST_TEST_EYES_OPEN_SECONDS if args.test_mode else default_config.eyes_open_seconds
    )
    default_eyes_closed = (
        REST_TEST_EYES_CLOSED_SECONDS
        if args.test_mode
        else default_config.eyes_closed_seconds
    )
    default_cycles = REST_TEST_CYCLE_COUNT if args.test_mode else default_config.cycles
    return RestingStateConfig(
        eyes_open_seconds=default_eyes_open if args.eyes_open is None else args.eyes_open,
        eyes_closed_seconds=(
            default_eyes_closed if args.eyes_closed is None else args.eyes_closed
        ),
        cycles=default_cycles if args.cycles is None else args.cycles,
        fullscreen=default_config.fullscreen,
        allow_gui=default_config.allow_gui,
        window_size=default_config.window_size,
        background_color=default_config.background_color,
        text_color=default_config.text_color,
        font=default_config.font,
        auto_advance=args.auto_advance,
    )


def _build_wm_pretest_config(args: argparse.Namespace) -> WMPretestConfig:
    default_task_timeout_seconds = (
        WM_PRETEST_TEST_TASK_TIMEOUT_SECONDS if args.test_mode else None
    )
    return WMPretestConfig(
        auto_advance=args.auto_advance,
        pilot_mode=args.test_mode,
        task_timeout_seconds=(
            default_task_timeout_seconds
            if args.wm_timeout_seconds is None
            else args.wm_timeout_seconds
        ),
    )


def _build_mental_arithmetic_config(
    args: argparse.Namespace,
) -> MentalArithmeticConfig:
    default_config = MentalArithmeticConfig()
    default_fixation_seconds = (
        MENTAL_ARITHMETIC_TEST_FIXATION_SECONDS
        if args.test_mode
        else default_config.fixation_seconds
    )
    default_inter_trial_seconds = (
        MENTAL_ARITHMETIC_TEST_INTER_TRIAL_SECONDS
        if args.test_mode
        else default_config.inter_trial_seconds
    )
    default_response_timeout_seconds = (
        MENTAL_ARITHMETIC_TEST_RESPONSE_TIMEOUT_SECONDS
        if args.test_mode
        else default_config.response_timeout_seconds
    )
    default_pre_response_blank_seconds = (
        MENTAL_ARITHMETIC_TEST_PRE_RESPONSE_BLANK_SECONDS
        if args.test_mode
        else default_config.pre_response_blank_seconds
    )
    default_trial_counts = (
        dict(MENTAL_ARITHMETIC_TEST_TRIALS_PER_LEVEL)
        if args.test_mode
        else dict(default_config.trial_counts)
    )
    return MentalArithmeticConfig(
        fullscreen=False if args.ma_windowed else default_config.fullscreen,
        allow_gui=False if args.ma_no_gui else default_config.allow_gui,
        force_mouse_visible=default_config.force_mouse_visible,
        window_size=default_config.window_size,
        background_color=default_config.background_color,
        text_color=default_config.text_color,
        font=default_config.font,
        fixation_seconds=(
            default_fixation_seconds
            if args.ma_fixation_seconds is None
            else args.ma_fixation_seconds
        ),
        pre_response_blank_seconds=default_pre_response_blank_seconds,
        inter_trial_seconds=(
            default_inter_trial_seconds
            if args.ma_inter_trial_seconds is None
            else args.ma_inter_trial_seconds
        ),
        response_timeout_seconds=(
            default_response_timeout_seconds
            if args.ma_response_timeout_seconds is None
            else args.ma_response_timeout_seconds
        ),
        random_seed=default_config.random_seed if args.ma_seed is None else args.ma_seed,
        block_count=(
            MENTAL_ARITHMETIC_TEST_BLOCK_COUNT
            if args.test_mode
            else default_config.block_count
        ),
        trials_per_block=(
            MENTAL_ARITHMETIC_TEST_TRIALS_PER_BLOCK
            if args.test_mode
            else default_config.trials_per_block
        ),
        block_rest_seconds=(
            MENTAL_ARITHMETIC_TEST_BLOCK_REST_SECONDS
            if args.test_mode
            else default_config.block_rest_seconds
        ),
        trial_counts={
            "QE": (
                default_trial_counts["QE"]
                if args.ma_qe_count is None
                else args.ma_qe_count
            ),
            "QM": (
                default_trial_counts["QM"]
                if args.ma_qm_count is None
                else args.ma_qm_count
            ),
            "QH": (
                default_trial_counts["QH"]
                if args.ma_qh_count is None
                else args.ma_qh_count
            ),
        },
        difficulty_rule_specs=default_config.difficulty_rule_specs,
        auto_advance=args.auto_advance,
    )


def _build_learning_cycle_config(args: argparse.Namespace) -> LearningCycleConfig:
    default_config = LearningCycleConfig()
    trials_file = (
        LEARNING_CYCLE_PROTOCOL_TRIALS_FILE
        if args.lc_trials_file is None
        else args.lc_trials_file
    )
    return LearningCycleConfig(
        trials_file=trials_file,
        questionnaire_dir=default_config.questionnaire_dir,
        fullscreen=False if args.lc_windowed else default_config.fullscreen,
        allow_gui=False if args.lc_no_gui else default_config.allow_gui,
        force_mouse_visible=default_config.force_mouse_visible,
        window_size=default_config.window_size,
        background_color=default_config.background_color,
        text_color=default_config.text_color,
        font=default_config.font,
        expected_trials=_count_condition_rows(trials_file),
        missing_video_seconds=(
            default_config.missing_video_seconds
            if args.lc_missing_video_seconds is None
            else args.lc_missing_video_seconds
        ),
        post_phase_blank_seconds=default_config.post_phase_blank_seconds,
        statement_seconds=default_config.statement_seconds,
        response_seconds=default_config.response_seconds,
        question_rest_seconds=default_config.question_rest_seconds,
        inter_trial_rest_seconds=LEARNING_CYCLE_INTER_TRIAL_REST_SECONDS,
        counterbalance_row=args.lc_counterbalance_row,
        auto_advance=args.auto_advance,
        include_rating_phase=False,
    )


def _build_protocol_config(args: argparse.Namespace) -> ProtocolConfig:
    return ProtocolConfig(
        test_mode=args.test_mode,
        test_stage=args.test_stage,
        auto_advance=args.auto_advance,
    )


def _build_task_config(task_name: str, args: argparse.Namespace):
    if task_name == "protocol":
        return _build_protocol_config(args)
    if task_name == "resting_state":
        return _build_resting_state_config(args)
    if task_name == "wm_pretest":
        return _build_wm_pretest_config(args)
    if task_name == "mental_arithmetic":
        return _build_mental_arithmetic_config(args)
    if task_name == "learning_cycle":
        return _build_learning_cycle_config(args)
    raise ValueError(f"Unsupported task: {task_name}")


def _resolve_task_sequence(task_name: str | None) -> list[str]:
    if task_name in (None, "all"):
        return [DEFAULT_TASK_SLUG]
    return [task_name]


def main() -> None:
    parser = argparse.ArgumentParser(description="Cognitive load experiment launcher")
    parser.add_argument("--list", action="store_true", help="List registered tasks")
    parser.add_argument(
        "--task",
        choices=["all", *TASK_MAP.keys()],
        help="Run the full experiment or a single task",
    )
    parser.add_argument(
        "--participant",
        default="pilot",
        help="Participant identifier",
    )
    parser.add_argument(
        "--name",
        default="",
        help="Participant name",
    )
    parser.add_argument(
        "--age",
        default="",
        help="Participant age",
    )
    parser.add_argument(
        "--session",
        default="001",
        help="Session identifier",
    )
    parser.add_argument(
        "--skip-subject-dialog",
        action="store_true",
        help="Use CLI participant fields directly without showing the startup dialog",
    )
    parser.add_argument(
        "--auto-advance",
        action="store_true",
        help="Skip manual Enter prompts for scripted tests",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Greatly shrink all tasks for end-to-end testing",
    )
    parser.add_argument(
        "--test-stage",
        choices=TEST_STAGE_CHOICES,
        default=None,
        help="When used with --test-mode, run only one formal stage of the protocol",
    )
    parser.add_argument(
        "--eyes-open",
        type=int,
        default=None,
        help="Override resting-state eyes-open duration in seconds",
    )
    parser.add_argument(
        "--eyes-closed",
        type=int,
        default=None,
        help="Override resting-state eyes-closed duration in seconds",
    )
    parser.add_argument(
        "--cycles",
        type=int,
        default=None,
        help="Override resting-state cycle count",
    )
    parser.add_argument(
        "--wm-timeout-seconds",
        type=float,
        default=None,
        help="Cap each working-memory pretest subtask after this many seconds",
    )
    parser.add_argument(
        "--ma-qe-count",
        type=int,
        default=None,
        help="Number of easy (QE) arithmetic trials",
    )
    parser.add_argument(
        "--ma-qm-count",
        type=int,
        default=None,
        help="Number of medium (QM) arithmetic trials",
    )
    parser.add_argument(
        "--ma-qh-count",
        type=int,
        default=None,
        help="Number of hard (QH) arithmetic trials",
    )
    parser.add_argument(
        "--ma-seed",
        type=int,
        default=None,
        help="Random seed for arithmetic problem generation",
    )
    parser.add_argument(
        "--ma-fixation-seconds",
        type=float,
        default=None,
        help="Override arithmetic fixation duration",
    )
    parser.add_argument(
        "--ma-inter-trial-seconds",
        type=float,
        default=None,
        help="Override arithmetic inter-trial blank duration",
    )
    parser.add_argument(
        "--ma-response-timeout-seconds",
        type=float,
        default=None,
        help="Override arithmetic response timeout",
    )
    parser.add_argument(
        "--ma-windowed",
        action="store_true",
        help="Run arithmetic task in a window instead of fullscreen",
    )
    parser.add_argument(
        "--ma-no-gui",
        action="store_true",
        help="Disable GUI cursor support for arithmetic window",
    )
    parser.add_argument(
        "--lc-trials-file",
        default=None,
        help="Override the learning-cycle condition CSV path",
    )
    parser.add_argument(
        "--lc-counterbalance-row",
        type=int,
        default=None,
        help="Force a specific balanced order row for the learning-cycle task",
    )
    parser.add_argument(
        "--lc-windowed",
        action="store_true",
        help="Run the learning-cycle task in a window instead of fullscreen",
    )
    parser.add_argument(
        "--lc-no-gui",
        action="store_true",
        help="Disable GUI cursor support for the learning-cycle window",
    )
    parser.add_argument(
        "--lc-missing-video-seconds",
        type=float,
        default=None,
        help="Placeholder duration when a learning-cycle video file is missing",
    )
    args = parser.parse_args()

    ensure_directories()
    context = None
    try:
        task_map = _build_task_map()

        if args.list:
            print(f"Participant: {args.participant}")
            print(f"Session: {args.session}")
            print("Task order:")

            for index, task in enumerate(TASK_REGISTRY, start=1):
                print(f"{index}. {task.name}")

            print()
            return

        if args.test_stage and not args.test_mode:
            parser.error("--test-stage 只能与 --test-mode 一起使用。")
        if args.test_stage and args.task not in (None, "all", "protocol"):
            parser.error("--test-stage 仅适用于默认 protocol / --task protocol。")

        task_sequence = _resolve_task_sequence(args.task)
        participant_info = collect_participant_info(
            participant_id=args.participant,
            session_id=args.session,
            name=args.name,
            age=args.age,
            skip_dialog=args.skip_subject_dialog,
        )

        context = build_context(
            participant_info=participant_info,
            persist_outputs=not args.test_mode,
        )

        print(
            "Participant info: "
            f"name={participant_info.name}, "
            f"participant_id={participant_info.participant_id}, "
            f"age={participant_info.age}, "
            f"session={participant_info.session_id}"
        )

        if args.test_mode:
            if args.test_stage:
                print(
                    "Test mode enabled: running only one formal stage, shrinking task scale where applicable, and discarding outputs."
                )
            else:
                print("Test mode enabled: skipping practice, shrinking formal tasks, and discarding outputs.")

        for task_name in task_sequence:
            print(f"Running task: {task_name}")
            task_map[task_name](
                context,
                config=_build_task_config(task_name, args),
            )
    except Exception as exc:
        print(f"Task failed: {exc}")
        raise SystemExit(1) from exc
    finally:
        if context is not None:
            context.trigger.close()
            cleanup_context(context)


if __name__ == "__main__":
    main()
