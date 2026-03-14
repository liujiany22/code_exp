from __future__ import annotations

import argparse

from config.settings import ensure_directories
from common.data_io import build_context
from tasks import TASK_REGISTRY
from tasks.learning_cycle.task import LearningCycleConfig
from tasks.mental_arithmetic.task import MentalArithmeticConfig
from tasks.resting_state.task import RestingStateConfig
from tasks.wm_pretest.task import WMPretestConfig


def main() -> None:
    parser = argparse.ArgumentParser(description="Cognitive load experiment launcher")
    parser.add_argument("--list", action="store_true", help="List registered tasks")
    parser.add_argument(
        "--task",
        choices=["resting_state", "wm_pretest", "mental_arithmetic", "learning_cycle"],
        help="Run a single task",
    )
    parser.add_argument(
        "--participant",
        default="pilot",
        help="Participant identifier",
    )
    parser.add_argument(
        "--session",
        default="001",
        help="Session identifier",
    )
    parser.add_argument(
        "--auto-advance",
        action="store_true",
        help="Skip manual Enter prompts for scripted tests",
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
        if args.list or not args.task:
            print(f"Participant: {args.participant}")
            print(f"Session: {args.session}")
            print("Task order:")

            for index, task in enumerate(TASK_REGISTRY, start=1):
                print(f"{index}. {task.name}")

            print()

        task_map = {
            "resting_state": TASK_REGISTRY[0].runner,
            "wm_pretest": TASK_REGISTRY[1].runner,
            "mental_arithmetic": TASK_REGISTRY[2].runner,
            "learning_cycle": TASK_REGISTRY[3].runner,
        }

        if not args.task:
            print("Framework ready. Use --task to run a task.")
            return

        context = build_context(
            participant_id=args.participant,
            session_id=args.session,
        )

        if args.task == "resting_state":
            config = RestingStateConfig(
                eyes_open_seconds=args.eyes_open
                if args.eyes_open is not None
                else RestingStateConfig.eyes_open_seconds,
                eyes_closed_seconds=args.eyes_closed
                if args.eyes_closed is not None
                else RestingStateConfig.eyes_closed_seconds,
                cycles=args.cycles if args.cycles is not None else RestingStateConfig.cycles,
                auto_advance=args.auto_advance,
            )
            task_map[args.task](context, config=config)
        else:
            if args.task == "wm_pretest":
                task_map[args.task](
                    context,
                    config=WMPretestConfig(auto_advance=args.auto_advance),
                )
            elif args.task == "mental_arithmetic":
                default_config = MentalArithmeticConfig()
                task_map[args.task](
                    context,
                    config=MentalArithmeticConfig(
                        fullscreen=(
                            False if args.ma_windowed else default_config.fullscreen
                        ),
                        allow_gui=(
                            False if args.ma_no_gui else default_config.allow_gui
                        ),
                        force_mouse_visible=default_config.force_mouse_visible,
                        window_size=default_config.window_size,
                        background_color=default_config.background_color,
                        text_color=default_config.text_color,
                        font=default_config.font,
                        fixation_seconds=(
                            default_config.fixation_seconds
                            if args.ma_fixation_seconds is None
                            else args.ma_fixation_seconds
                        ),
                        inter_trial_seconds=(
                            default_config.inter_trial_seconds
                            if args.ma_inter_trial_seconds is None
                            else args.ma_inter_trial_seconds
                        ),
                        response_timeout_seconds=(
                            default_config.response_timeout_seconds
                            if args.ma_response_timeout_seconds is None
                            else args.ma_response_timeout_seconds
                        ),
                        random_seed=(
                            default_config.random_seed
                            if args.ma_seed is None
                            else args.ma_seed
                        ),
                        trial_counts={
                            "QE": (
                                default_config.trial_counts["QE"]
                                if args.ma_qe_count is None
                                else args.ma_qe_count
                            ),
                            "QM": (
                                default_config.trial_counts["QM"]
                                if args.ma_qm_count is None
                                else args.ma_qm_count
                            ),
                            "QH": (
                                default_config.trial_counts["QH"]
                                if args.ma_qh_count is None
                                else args.ma_qh_count
                            ),
                        },
                        difficulty_rule_specs=default_config.difficulty_rule_specs,
                        auto_advance=args.auto_advance,
                    ),
                )
            elif args.task == "learning_cycle":
                default_config = LearningCycleConfig()
                task_map[args.task](
                    context,
                    config=LearningCycleConfig(
                        trials_file=(
                            default_config.trials_file
                            if args.lc_trials_file is None
                            else args.lc_trials_file
                        ),
                        questionnaire_dir=default_config.questionnaire_dir,
                        fullscreen=(
                            False if args.lc_windowed else default_config.fullscreen
                        ),
                        allow_gui=(
                            False if args.lc_no_gui else default_config.allow_gui
                        ),
                        force_mouse_visible=default_config.force_mouse_visible,
                        window_size=default_config.window_size,
                        background_color=default_config.background_color,
                        text_color=default_config.text_color,
                        font=default_config.font,
                        expected_trials=default_config.expected_trials,
                        missing_video_seconds=(
                            default_config.missing_video_seconds
                            if args.lc_missing_video_seconds is None
                            else args.lc_missing_video_seconds
                        ),
                        post_phase_blank_seconds=default_config.post_phase_blank_seconds,
                        counterbalance_row=args.lc_counterbalance_row,
                        auto_advance=args.auto_advance,
                    ),
                )
            else:
                task_map[args.task](context)
    except Exception as exc:
        print(f"Task failed: {exc}")
        raise SystemExit(1) from exc
    finally:
        if context is not None:
            context.trigger.close()


if __name__ == "__main__":
    main()
