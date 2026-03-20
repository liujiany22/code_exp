# Full Protocol

This task orchestrates the current end-to-end experiment flow:

- practice segment
- formal segment
- placeholder guidance screens between major stages
- resting state, digit span, Corsi blocks, mental arithmetic, and video learning

## Run

```bash
python code_exp/launcher.py --participant sub01 --session 001
```

For a shortened dry run:

```bash
python code_exp/launcher.py --participant test --session 001 --test-mode --auto-advance
```

## Notes

- The protocol currently keeps several guidance screens as placeholders, matching the requested workflow.
- Practice digit span and Corsi demos use pilot mode plus a wrapper-level timeout.
- Formal learning-cycle execution currently runs as two groups with a configurable inter-group rest.
