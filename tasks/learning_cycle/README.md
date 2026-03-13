# Learning Cycle

This task implements the video-learning loop for the experiment.

## Current Structure

The task is fixed to 6 trials. Each trial runs:

1. pretest knowledge questionnaire placeholder
2. video playback
3. post-video subjective rating placeholder
4. post-video performance-check placeholder

The current version already handles:

- trial ordering
- video start/end EEG trigger emission through the centralized trigger layer
- placeholder questionnaire interfaces
- trial log and event log writing

The questionnaire content itself is intentionally left for later integration.

## Trial Design

The default condition table is:

- [learning_cycle_trials.csv](/Users/liujiany/work/CognitiveLoad/code_exp/stimuli/conditions/learning_cycle_trials.csv)

It expects 6 rows:

- 2 topics
- each topic has one `low`, one `medium`, and one `high` load video

Default topics in the template:

- `傅立叶变换`
- `统计基础`

## Order Control

Trial order is not run in the raw CSV order. The task applies a balanced
Latin-square order based on `participant_id`, or an explicit counterbalance row
if one is passed through the launcher.

This gives a reproducible order assignment and controls sequence effects better
than a simple shuffle.

## Video and Questionnaire Interfaces

- `video_file` is resolved relative to `code_exp/stimuli/videos/`
- `pretest_form`, `rating_form`, and `posttest_form` are resolved relative to
  `code_exp/stimuli/questionnaires/`

If a video file is missing, the task does not crash. It shows a short placeholder
screen instead, which is useful before the real materials are ready.

## Outputs

The task writes:

- `learning_cycle_trial_log.csv`
- `learning_cycle_events.csv`
- `learning_cycle_order.csv`
- `learning_cycle_config.json`

## Configuration

Most defaults are in:

- [settings.py](/Users/liujiany/work/CognitiveLoad/code_exp/config/settings.py)

Useful items:

- `LEARNING_CYCLE_TRIALS_FILE`
- `LEARNING_CYCLE_EXPECTED_TRIALS`
- `LEARNING_CYCLE_MISSING_VIDEO_SECONDS`
- `LEARNING_CYCLE_FULLSCREEN`
- `LEARNING_CYCLE_ALLOW_GUI`

## Run

```bash
python code_exp/launcher.py --task learning_cycle --participant sub01 --session 001
```

Useful overrides:

```bash
python code_exp/launcher.py \
  --task learning_cycle \
  --participant sub01 \
  --session 001 \
  --lc-windowed \
  --lc-counterbalance-row 2
```
