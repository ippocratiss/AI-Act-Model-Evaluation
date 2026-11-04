# Auditing an LLM CV screener under the EU AI Act

A small, reproducible audit of an LLM that shortlists job candidates. CV screening is a high-risk use of AI under the EU AI Act (Annex III, point 4(a)). The notebook measures the properties that Articles 10 and 15 require providers to examine: **accuracy, non-discrimination, calibrated confidence and robustness**, and writes the results into a report.

## How it works

1. **Synthetic CVs with matched twins.** Each candidate appears in 8 versions that differ only in gender, age and nationality (expressed through the name and the graduation year). The hidden truth (qualified or not) is identical for all twins, so any difference in the model's decisions is caused by the attribute alone.
2. **The model scores each CV** using fixed scoring rules and returns JSON (`score`, `confidence`). Each CV is sent several times. The decision rule (shortlist if score ≥ `CUTOFF`) is applied by the notebook, not by the model.
3. **The decisions are compared with the truth** and each result is checked against an illustrative PASS/FAIL threshold.

## What it measures

| Area | Metrics |
|---|---|
| Accuracy | accuracy, precision, recall, F1, confusion matrix, cut-off sweep |
| Fairness | disparate impact, TPR (recall) gap, score gap, each with a bootstrap 1σ error |
| Calibration | ECE, reliability plot, calibration per group |
| Robustness | the same audit on perturbed data (typos, hidden instructions, other job field) and on different prompts |

## Quick start

```bash
pip install pandas numpy matplotlib scikit-learn requests tqdm jupyter
python gen_data.py            # creates cvs.csv (or use the one provided)
```

Choose a model in the Settings cell of `audit.ipynb`:
- **Local (free, no limits):** install [Ollama](https://ollama.com), pull a model (for example `ollama pull gemma3:4b`) and set `MODEL`.
- **Hosted API:** set `URL` and `MODEL`, and put the key in an environment variable (`export GROQ_KEY=...`). Never put a key in the notebook.

Then run the notebook from top to bottom. The last cell writes `report.md` and `calibration.png`.

## Files

| File | Content |
|---|---|
| `audit.ipynb` | the audit |
| `gen_data.py` | generator of the synthetic CVs |
| `cvs.csv` | the dataset (2,400 CVs: 300 candidates × 8 twins) |
| `report.md` | example report generated from a real run |
| `replies.csv` | the model's raw replies from that run |

## Headline results (from `report.md`)

- Model: **[model name]**, prompt version **[version]**, cut-off **[value]**.
- Accuracy **[value]**, precision **[value]**, recall **[value]**.
- Fairness: **[main finding, with its ± error]**.
- Calibration: ECE **[value]**, **[over/under]**confident.
- Prompt wording alone changed **[metric]** from **[a]** to **[b]**.

## Mapping to the AI Act

| Article | Requirement | Where it is tested |
|---|---|---|
| Art. 9 | risk management | risk register (see report) |
| Art. 10 | data governance, bias | fairness section |
| Art. 14 | human oversight | calibration (can reviewers trust the confidence?) |
| Art. 15 | accuracy, robustness | accuracy, calibration and robustness sections |
| Art. 72 | post-market monitoring | re-running the notebook on new data |

## Limitations

- Synthetic data. The CVs are structured summaries, not free text, so extraction from real CVs is not tested.
- Results hold for this model, prompt and cut-off only. Prompt wording can change them substantially.
- Small samples: gaps of about one error or less cannot be told apart from noise.
- A technical audit, not a conformity assessment under Art. 43. Thresholds are illustrative, not legal limits.

## Author

Ippocratis Saltas
