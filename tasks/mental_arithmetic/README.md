# Mental Arithmetic

This module now implements a discrete arithmetic task with Q-value-based
difficulty levels for this project.

It is no longer the previous long-block serial subtraction version.

## Difficulty Levels

- `QE`: easy, `Q < 2`
- `QM`: medium, `2 <= Q < 4`
- `QH`: hard, `Q >= 4`

Current Q-value rule:

- `Q = digit_complexity + carry_count`
- `digit_complexity = digits(left_operand) + digits(right_operand) - 2`
- `carry_count` = number of carry operations in the addition

The generated questions are currently addition problems, because the requested
Q-value rule is defined around carry operations.

## Trial Flow

Each trial currently runs as:

1. fixation
2. arithmetic question display
3. numeric keyboard response
4. brief blank inter-trial interval

At the start of the task, an instruction page explains the input method.

## Logs

The main behavior log contains at least:

- `TrialNumber`
- `DifficultyLevel`
- `Question`
- `CorrectAnswer`
- `ParticipantAnswer`
- `ResponseTime`
- `QValue`

Additional columns are also written:

- `CarryCount`
- `ParticipantCorrect`

The task also writes:

- `mental_arithmetic_events.csv`
- `mental_arithmetic_generated_problems.csv`
- `mental_arithmetic_config.json`

EEG trigger points are kept in the code as comments/placeholders only. This
task does not currently send real EEG markers.

## Configuration

Most editable parameters live in:

- `code_exp/config/settings.py`

Important parameters:

- `MENTAL_ARITHMETIC_TRIALS_PER_LEVEL`
- `MENTAL_ARITHMETIC_Q_RULES`
- `MENTAL_ARITHMETIC_FIXATION_SECONDS`
- `MENTAL_ARITHMETIC_INTER_TRIAL_SECONDS`
- `MENTAL_ARITHMETIC_RESPONSE_TIMEOUT_SECONDS`
- `MENTAL_ARITHMETIC_RANDOM_SEED`

The task now validates these settings at startup, so invalid difficulty names,
negative timings, or malformed `digit_pairs` fail early with a clear error.

## Run

```bash
python code_exp/launcher.py --task mental_arithmetic --participant sub01 --session 001
```

Useful overrides:

```bash
python code_exp/launcher.py \
  --task mental_arithmetic \
  --ma-qe-count 4 \
  --ma-qm-count 4 \
  --ma-qh-count 4 \
  --ma-seed 42 \
  --ma-windowed
```
