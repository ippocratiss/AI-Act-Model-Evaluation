# Risk register and human-oversight checklist

A notebook that turns audit results into two documents an AI governance team can use:

1. a **risk register**: each risk is described, rated, and given a control and an owner (EU AI Act Art. 9, risk management);
2. a **human-oversight checklist**: what a human reviewer must be able to do, with a status for each point (Art. 14, with Art. 12, 26, 72 and 73).

The notebook is pre-filled with the results of the [CV screener audit](../CV-screener_auditing/) (`gemma3:1b`, cut-off 45). You can feed it the results of any audit by changing one settings cell.

## How it works

- **Input:** the audit numbers in section 0 of the notebook: accuracy, calibration error (ECE), fairness gaps with their errors, and optional tests not yet run (prompt injection, drift).
- **Rating:** every risk gets a likelihood and an impact from 1 to 3. Score = likelihood × impact. High is 6 or more, Medium 3 to 4, Low 1 to 2. Likelihood is 3 when the audit measured the problem, 2 when it was not tested (unknown, not safe), and 1 when it was tested and not found.
- **Output:** a sorted register (R1, R2, ...) and a nine-point oversight checklist with the status Met, Partly met, To implement or Gap.

## Result for the CV screener

Five High risks (age gap, accuracy below target, calibration, sensitivity to prompt changes, prompt injection), two Medium (gender gap, drift) and one Low (nationality gap).

## Requirements and usage

- Python 3.9 or newer, `pandas`, `jupyter`
- Open `risk_register.ipynb`, edit section 0 if you have new numbers, and run all cells.
- Outputs: `risk_register.csv`, `oversight_checklist.csv`, `risk_register.md`.

## Limitations

- Thresholds, ratings and owners (roles, not people) are illustrative; choose values you can defend.
- This is a governance aid, not a conformity assessment under Art. 43, and not legal advice.
