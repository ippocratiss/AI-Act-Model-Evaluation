# LLM auditing and the EU AI Act 

Hands-on evaluation of AI systems against the requirements of the EU AI Act (Regulation (EU) 2024/1689). Each project takes a real system, tests it with evidence (metrics with error bars, thresholds set in advance), turns the failures into rated findings, and maps them to the relevant articles.

Author: Ippocratis Saltas, PhD

## Projects

| Folder | System | What it tests | Main articles |
|---|---|---|---|
| [`CV-screener_auditing/`](CV-screener_auditing/) | An LLM that scores CVs for a Data Scientist role (hiring is high-risk under Annex III) | Accuracy, calibration, and fairness by gender, age and nationality, using matched "twin" CVs that differ in one attribute only | Art. 10, 14, 15 |
| [`agent_auditing/`](agent_auditing/) | An LLM agent that triages financial-crime alerts using tools | Correct decisions, required process, forbidden actions, stability, resistance to a hidden instruction; a general framework for any agent | Art. 9, 12, 14, 15 |

Each folder has its own README with requirements, instructions and results.

## Results at a glance

**CV screener** (`gemma3:1b`, 50 candidates × 8 twins, 3 replies per CV):
- Accuracy 0.742 against a target of 0.85, and calibration error 0.118 against a limit of 0.05: both fail.
- The model scored 52-year-old candidates 3.9 ± 0.8 points lower than 28-year-olds with the same CV (4.9σ). The four-fifths rule did not flag it once its error was counted, which shows why a single rule is not enough.
- No measurable gap by nationality, and a smaller one by gender.

**Agent validation** (`gemma3:1b` and `gemma3:4b`, 40 alerts × 3 repeats):
- Opinion for both: not ready for production.
- The two models fail in opposite ways. The 1B model escalates almost everything and the 4B model escalates only the sanctions alerts. Neither applies the payment and country rules.
- A larger model fixed the process (sanctions check always done, stable answers) but not the decisions. The recommendation is to run the required rules in code.

## The common method

Every project asks the same questions of a system:

| Question | Example metrics | Article |
|---|---|---|
| Right answer? | accuracy, precision, recall (TPR), F1, false positive rate, ECE | Art. 15 |
| Fair? | disparate impact, TPR gap, score gap (with error) | Art. 10 |
| Right way? | required-tool recall, format error rate | Art. 9, 14 |
| Within limits? | violation rate of forbidden actions | Art. 14 |
| Stable and robust? | agreement across repeats, attack success rate, flip rate | Art. 15 |

Then: failed checks become findings rated by likelihood × impact, each with an article, a recommendation and an owner, and the report ends with a validation opinion. Results are compared with trivial baselines, and every number is read together with its error.

## Why synthetic data

Real CVs and real bank alerts are confidential and have no known correct answers. Synthetic cases let me fix the correct answer by construction, vary one thing at a time, and let anyone rerun the work. The limits of this choice are stated in each report.

## Limitations

- Synthetic data and small test sets: read every result together with its error.
- Results hold only for the tested models, prompts and settings.
- Thresholds are illustrative, not legal limits.
- These are technical evaluations. They are evidence for a conformity assessment (Art. 43), not a replacement for one, and not legal advice.

## Running the projects

Each project runs locally with [Ollama](https://ollama.com) and Python (Jupyter notebooks). See the README in each folder for the exact steps.
