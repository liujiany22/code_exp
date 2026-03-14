# code_exp

Starter framework for the cognitive load experiment program.

## Structure

- `launcher.py`: entry point for the whole experiment
- `config/`: global settings and EEG event codes
- `eeg/`: trigger interface and trigger test
- `common/`: shared data and UI helpers
- `tasks/`: task-level modules
- `stimuli/`: videos, images, and condition tables
- `data/`: output folders for behavior data and logs

## Next implementation steps

1. Replace the dummy trigger with the real NeusenW32 trigger interface.
2. Decide whether `wm_pretest` needs trial-level EEG markers.
3. Replace the learning-cycle questionnaire placeholders with the real forms.
4. Validate the PsychoPy tasks on the final Windows collection machine.

## Current status

- The trigger layer is centralized in `eeg/trigger.py`.
- `dummy` mode is the default and is safe before the EEG hardware link is ready.
- The trigger layer can now broadcast the same event to EEG and optional EyeLink message output.
- The EyeLink path is message-only by default, so calibration and recording can stay under the eye-tracker operator workflow.
- The resting-state task now uses a PsychoPy guidance interface and defaults to 180s eyes-open plus 180s eyes-closed.
- The working-memory pretest can wrap the reference `digit span` and `corsi blocks` PsychoPy tasks.
- The mental arithmetic task is implemented as a Q-value-based arithmetic task with QE/QM/QH random generation.
- The learning-cycle task is implemented with a 6-trial video schedule, balanced order control, questionnaire placeholders, and video start/end triggers.

## Run resting state

```bash
python code_exp/launcher.py --task resting_state --auto-advance --eyes-open 3 --eyes-closed 3
```

Default resting-state timing is 180 seconds for eyes open and 180 seconds for eyes closed.

For hardware use, configure `TRIGGER_MODE` / `TRIGGER_PORT` for EEG and set
`EYELINK_ENABLED=1` if EyeLink message logging should run in parallel. Set
`EYELINK_INITIALIZE_CONTEXT=1` only if you want this program to also send
`screen_pixel_coords`, `DISPLAY_COORDS`, and `calibration_type`.

## Run working-memory pretest

```bash
python code_exp/launcher.py --task wm_pretest --participant sub01 --session 001
```

Environment notes for PsychoPy are in
`tasks/wm_pretest/README.md`.

## Run mental arithmetic

```bash
python code_exp/launcher.py --task mental_arithmetic --participant sub01 --session 001
```

Task notes are in
`tasks/mental_arithmetic/README.md`.

## Run learning cycle

```bash
python code_exp/launcher.py --task learning_cycle --participant sub01 --session 001
```

Task notes are in
`tasks/learning_cycle/README.md`.
