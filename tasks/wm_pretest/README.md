# Working Memory Pretest

This task wraps two existing PsychoPy experiments from the reference folder:

- `digit_span-master_new/digit_span_lastrun.py`
- `corsi_blocks-master_new/corsi_blocks_lastrun.py`

## Behavior

- A single `wm_pretest` entry point runs the two tests in sequence.
- The original PsychoPy test interfaces are preserved.
- Participant and session IDs are injected from `code_exp`.
- Output files are redirected into `code_exp/data/raw_beh/.../wm_pretest/`.

## Environment

Recommended:

- Python 3.10
- PsychoPy `2025.1.1`

Current generated scripts were exported by PsychoPy Builder `2025.1.1`. Other
versions may still work, but timing or component compatibility should not be
assumed.

## macOS note

The wrapper in `code_exp` bypasses `ioHub` for these two reference tasks and
creates standard keyboard devices instead. This avoids the common
`ioHub startup failed` issue on some macOS setups.

The tradeoff is that keyboard timing here is not the highest-precision route.
For a pretest interface this is usually acceptable. If you later need stricter
timing validation, revisit the original Builder scripts or move final data
collection to the validated acquisition machine.

## Install

Option 1:

- Use the Python interpreter bundled with the PsychoPy desktop app.

Option 2:

- Create a dedicated environment and install PsychoPy manually.

Example:

```bash
python -m venv .venv
source .venv/bin/activate
pip install psychopy==2025.1.1
```

If PTB audio support causes startup issues on the current machine, override:

```bash
export PSYCHOPY_AUDIO_LIB=pygame
```

## Run

```bash
python code_exp/launcher.py --task wm_pretest --participant sub01 --session 001
```
