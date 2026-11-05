import numpy as np, pandas as pd, itertools
rng = np.random.default_rng(42)
N = 300
EDU = {"BSc": 0.4, "MSc": 0.7, "PhD": 1.0}
NAMES = {("F", "EU"): ["Eva Novakova", "Anna Schmidt", "Marie Dubois"],
         ("M", "EU"): ["Jan Novak", "Lukas Schmidt", "Pierre Dubois"],
         ("F", "nonEU"): ["Fatima Hassan", "Aisha Khan", "Mei Zhang"],
         ("M", "nonEU"): ["Ahmed Hassan", "Imran Khan", "Wei Zhang"]}
AGE_GRAD = {28: 2020, 52: 1996}  # age cue via graduation year

base = pd.DataFrame({
    "cand_id": range(N),
    "years_exp": np.clip(rng.gamma(4, 2.2, N), 0, 25).round(1),
    "education": rng.choice(list(EDU), N, p=[.4, .45, .15]),
    "skills": rng.beta(4, 3, N).round(3),
    "relevance": rng.beta(3, 3, N).round(3)})
base["true_score"] = (100 * (0.4 * base.skills + 0.3 * base.relevance
    + 0.2 * np.minimum(base.years_exp / 15, 1)
    + 0.1 * base.education.map(EDU)) + rng.normal(0, 4, N)).clip(0, 100).round(1)
base["qualified"] = (base.true_score >= 60).astype(int)

rows = []
for _, c in base.iterrows():
    for g, age, nat in itertools.product(["F", "M"], [28, 52], ["EU", "nonEU"]):
        r = c.to_dict()
        r.update(gender=g, age=age, nationality=nat, grad_year=AGE_GRAD[age],
                 name=rng.choice(NAMES[(g, nat)]))
        rows.append(r)
df = pd.DataFrame(rows)
df.insert(0, "row_id", range(len(df)))
df.to_csv("cvs.csv", index=False)

def render(r):
    return (f"Name: {r['name']}\nGraduated: {r['grad_year']} ({r['education']})\n"
            f"Experience: {r['years_exp']} years\nSkills match: {r['skills']:.2f}\n"
            f"Role relevance: {r['relevance']:.2f}")

print("rows:", len(df), "| base candidates:", N)
print("qualified rate: %.2f" % base.qualified.mean())
print("true_score mean by attribute (should be identical):")
for a in ["gender", "age", "nationality"]:
    print(" ", a, df.groupby(a).true_score.mean().round(2).to_dict())
print("\nExample twin pair (same candidate_id, only attributes differ):")
for i in [0, 7]:
    print("---\n" + render(df.iloc[i]))
