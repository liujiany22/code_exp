# Windows Handoff

This document summarizes the current state of `code_exp` and the recommended
next steps when moving the experiment workflow to Windows.

## Goal

Continue development and validation of the cognitive load experiment on a
Windows machine, especially the PsychoPy-based `wm_pretest` task and later EEG
integration with `NeusenW32`.

## Current Project State

- `code_exp/launcher.py`
  - Unified entry point for all tasks.
  - Supported tasks:
    - `resting_state`
    - `wm_pretest`
    - `mental_arithmetic`
    - `learning_cycle`

- `code_exp/tasks/resting_state/task.py`
  - Implemented and runnable.
  - Uses a PsychoPy guidance interface.
  - Defaults to 180s eyes-open and 180s eyes-closed.
  - Supports configurable eyes-open / eyes-closed timing and cycle count.
  - Writes `resting_state_events.csv`.
  - Uses the centralized trigger interface.

- `code_exp/tasks/wm_pretest/task.py`
  - Wraps two existing PsychoPy generated tasks:
    - `code_exp/cognitiveabilitytest/digit_span-master_new/digit_span_lastrun.py`
    - `code_exp/cognitiveabilitytest/corsi_blocks-master_new/corsi_blocks_lastrun.py`
  - Injects participant/session info.
  - Redirects outputs into `code_exp/data/raw_beh/.../wm_pretest/`.
  - Emits only task-boundary triggers, not trial-level triggers.
  - Includes macOS-specific compatibility code for `ioHub` and window handling.

- `code_exp/tasks/mental_arithmetic/task.py`
  - Implemented as a PsychoPy Q-value-based arithmetic task.
  - Randomly generates `QE`, `QM`, and `QH` addition problems.
  - Writes behavior, events, generated-problem, and config snapshot files.
  - Validates timing, difficulty levels, and Q-rule configuration at startup.
  - Keeps EEG trigger points as code comments/placeholders only; no real EEG send.
  - Parameters can be changed in `code_exp/config/settings.py` or via launcher overrides.

- `code_exp/tasks/learning_cycle/task.py`
  - Implemented as a PsychoPy 6-trial video-learning task.
  - Uses a balanced Latin-square order across the 6 trial items.
  - Expects two topics with one low, one medium, and one high load video each.
  - Keeps questionnaire phases as placeholders for later integration.
  - Sends centralized task/video trigger events and writes trial/order/event logs.

- `code_exp/eeg/trigger.py`
  - Centralized trigger abstraction.
  - Current mode is `dummy`.
  - Can broadcast one event to EEG serial trigger output and optional EyeLink message output.
  - Real `NeusenW32` protocol details still need hardware validation.
  - EyeLink support is a PyLink-based message-only skeleton by default.
  - Calibration, validation, drift correction, and recording can remain under the EyeLink operator workflow.

## Why Move to Windows

- macOS produced multiple PsychoPy runtime issues:
  - `ioHub startup failed`
  - Objective-C / pyglet bridge errors
  - Fullscreen and frame-rate measurement instability
- The EEG acquisition path will likely be easier to validate on Windows anyway.

## Recommended Windows Environment

Preferred:

- Windows 10 or 11
- Python 3.10
- PsychoPy `2025.1.1` if available in the chosen setup

Two practical options:

1. PsychoPy Standalone
   - Simplest for GUI task execution.
   - Good first choice for validating the reference PsychoPy tasks.

2. Dedicated Python environment
   - Example:
   - `py -3.10 -m venv .venv`
   - `.venv\\Scripts\\activate`
   - `python -m pip install -U pip setuptools wheel`
   - `python -m pip install psychopy`

Avoid:

- Reusing the previous macOS Anaconda Python 3.13 setup.

## Files To Copy

Copy the whole `code_exp/` directory, including:

- `code_exp/cognitiveabilitytest/`
- `code_exp/config/`
- `code_exp/tasks/`
- `code_exp/eeg/`
- `code_exp/common/`

The reference tasks must remain under:

- `code_exp/cognitiveabilitytest/digit_span-master_new/`
- `code_exp/cognitiveabilitytest/corsi_blocks-master_new/`

because `code_exp/config/settings.py` points there.

## First Commands To Run On Windows

List tasks:

```bash
python code_exp/launcher.py --list
```

Validate resting state:

```bash
python code_exp/launcher.py --task resting_state --auto-advance --eyes-open 3 --eyes-closed 3 --cycles 1
```

Validate working-memory pretest:

```bash
python code_exp/launcher.py --task wm_pretest --participant sub01 --session 001
```

Validate mental arithmetic:

```bash
python code_exp/launcher.py --task mental_arithmetic --participant sub01 --session 001
```

Validate learning cycle:

```bash
python code_exp/launcher.py --task learning_cycle --participant sub01 --session 001 --lc-windowed
```

## Important Constraints

- `wm_pretest` currently preserves the original PsychoPy task interfaces.
- Only start/end triggers are emitted for `digit_span` and `corsi_blocks`.
- If trial-level EEG synchronization is needed later, the reference PsychoPy
  tasks should be copied into a maintained experiment folder and edited there.

## Suggested Next Steps On Windows

1. Confirm `resting_state` runs and writes output.
2. Confirm `wm_pretest` runs through both tasks without macOS-specific issues.
3. Confirm `mental_arithmetic` generates and runs QE/QM/QH trials.
4. Confirm `learning_cycle` loads the 6-trial schedule, shows placeholders, and records video start/end events.
5. If `wm_pretest` works, remove or ignore the macOS compatibility path.
6. After behavior tasks are stable, implement the real trigger backend in:
   - `code_exp/eeg/trigger.py`
   - `code_exp/config/settings.py`
7. If EyeLink is used, validate the message-only path on Windows and decide whether `EYELINK_INITIALIZE_CONTEXT=1` is needed.

## Paste-Ready Note For A Windows Agent

```text
Project root: code_exp

Current status:
- resting_state is implemented and runnable
- wm_pretest wraps two PsychoPy-generated tasks:
  - code_exp/cognitiveabilitytest/digit_span-master_new/digit_span_lastrun.py
  - code_exp/cognitiveabilitytest/corsi_blocks-master_new/corsi_blocks_lastrun.py
- mental_arithmetic is implemented as a Q-value-based arithmetic task
- it generates QE/QM/QH arithmetic trials at runtime
- it keeps EEG trigger placeholders only and does not send real markers
- learning_cycle is implemented as a 6-trial video-learning task
- it uses a balanced order over two topics x three load levels
- questionnaire phases are placeholders and should be replaced later
- trigger layer is centralized in code_exp/eeg/trigger.py and currently runs in dummy mode
- it can optionally mirror the same events to EyeLink message output
- its EyeLink path is message-only by default and does not own calibration or EDF lifecycle
- real NeusenW32 trigger communication still needs hardware validation

Known macOS issues that motivated the move:
- ioHub startup failed
- ObjC/pyglet windowing errors
- unstable fullscreen/frame-rate behavior

What to do first on Windows:
1. Set up Python 3.10 or PsychoPy Standalone
2. Run `python code_exp/launcher.py --task resting_state --auto-advance --eyes-open 3 --eyes-closed 3 --cycles 1`
3. Run `python code_exp/launcher.py --task wm_pretest --participant sub01 --session 001`
4. Run `python code_exp/launcher.py --task mental_arithmetic --participant sub01 --session 001`
5. Run `python code_exp/launcher.py --task learning_cycle --participant sub01 --session 001 --lc-windowed`
6. If wm_pretest, mental_arithmetic, and learning_cycle work, continue to the EEG trigger backend

Files most relevant now:
- code_exp/launcher.py
- code_exp/config/settings.py
- code_exp/eeg/trigger.py
- code_exp/tasks/resting_state/task.py
- code_exp/tasks/wm_pretest/task.py
- code_exp/tasks/mental_arithmetic/task.py
- code_exp/tasks/learning_cycle/task.py
```
