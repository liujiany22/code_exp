# Learning-Cycle Questionnaires

Put the learning-cycle questionnaire files here.

The learning-cycle condition table resolves these fields relative to this folder:

- `pretest_form`
- `rating_form`
- `posttest_form`

Current support:

- If the referenced CSV contains `item_number`, `question_text`, and `correct_answer`,
  the task will run a real true/false questionnaire using `F = 对` and `J = 错`.
- Implemented timed structure: statement `4s` + response `4s` + rest `1s`.
- After the judgement section, pretest and posttest both continue to a recall prompt.
- If the file does not exist yet, the task falls back to the existing placeholder screen.

`posttest_fourier_protocol.csv` is the first live questionnaire now wired into the
formal learning-cycle flow.
