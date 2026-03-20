# Mental Arithmetic

This task now uses the planned comparison paradigm:

- black addition problem
- short `+` break
- blue candidate answer
- left / right mouse judgment

It is no longer the earlier keyboard-input answer task.

## Difficulty Levels

- `QE`: easy, `Q < 2`
- `QM`: medium, `2 <= Q < 4`
- `QH`: hard, `Q >= 4`

Current Q-value rule:

- `Q = digit_complexity + carry_count`
- `digit_complexity = digits(left_operand) + digits(right_operand) - 2`
- `carry_count` = number of carry operations in the addition

The generated materials are addition problems because the requested Q-value rule
is defined around carry operations.

## Formal Timing Structure

Default formal structure:

- `3` blocks
- `25` trials per block
- `30s` rest after block 1 and block 2

Each trial runs as:

1. black arithmetic problem display: `6s`
2. central `+` break: `1s`
3. blue candidate answer judgment: `4s`
4. central `+` break: `1s`

Participant response:

- left mouse button: the blue number equals the correct answer
- right mouse button: the blue number does not equal the correct answer

## Logs

The main behavior log now includes at least:

- `BlockNumber`
- `TrialNumber`
- `DifficultyLevel`
- `Question`
- `CorrectAnswer`
- `ProbeAnswer`
- `ProbeMatches`
- `CorrectResponse`
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

EEG trigger points are still placeholders in this task; real EEG sending is not
yet enabled here.

## Configuration

Most editable parameters live in:

- `code_exp/config/settings.py`

Important parameters:

- `MENTAL_ARITHMETIC_BLOCK_COUNT`
- `MENTAL_ARITHMETIC_TRIALS_PER_BLOCK`
- `MENTAL_ARITHMETIC_BLOCK_REST_SECONDS`
- `MENTAL_ARITHMETIC_FIXATION_SECONDS`
- `MENTAL_ARITHMETIC_PRE_RESPONSE_BLANK_SECONDS`
- `MENTAL_ARITHMETIC_RESPONSE_TIMEOUT_SECONDS`
- `MENTAL_ARITHMETIC_INTER_TRIAL_SECONDS`
- `MENTAL_ARITHMETIC_TRIALS_PER_LEVEL`
- `MENTAL_ARITHMETIC_Q_RULES`

The task validates these settings at startup, so invalid counts, timings, or
malformed `digit_pairs` fail early with a clear error.

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
