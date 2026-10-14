# Decisions

One entry per decision where there were alternatives, written when it is taken. If a decision
changes, the old entry stays and the new one links to it. Entries before 2026-10-14 were
reconstructed from the notebooks and the dicetamer entry; `≤` means the date is a bound, not
recorded. The IDs (`CV-Enn`) are the ones used in the project's entry of the dicetamer knowledge
base (`dicetamer/docs/docs_projects/projects/car-value.md`).

**Evidence**: A measured · B observed · C reasoned, not compared.

| Date | ID | Decision | Alternatives | Why | What would reopen it | Evid. |
| --- | --- | --- | --- | --- | --- | --- |
| 2024 | CV-E01 | Scrape through the Zyte proxy with random waits (5.5–20.8 s), save raw HTML and parse it later | Direct requests | No blocking; the dataset can be rebuilt without downloading again | Zyte cost or terms change | C |
| ≤ 2026-02-03 | CV-E02 | Drop outliers with a domain rule: CNG cars (60, too few) and listings > 200 % of the median new-car price for their brand and segment | IQR cut | Compares each car with its own brand and segment; drops only 72 rows (0.4 %) | A retrain with a very different market | B |
| ≤ 2026-02-03 | CV-E03 | scikit-learn + Optuna for the production model | PyCaret AutoML | Similar level (PyCaret R² 0.75–0.82 per fold, one at 0.56 from outliers; sklearn R² 0.796 on test), and no second Python environment | A tool that clearly beats the 0.796 | B |
| 2026-02-03 | CV-E04 | GradientBoosting | LightGBM, RandomForest, ExtraTrees, HistGradientBoosting (30 Optuna trials each) | All between R² 0.792 and 0.798; GradientBoosting best CV RMSE (3,648 €). The ceiling is in the data, not the model | New features or data | A |
| 2026-02-03 | CV-E05 | Six features, without horsepower | With horsepower (`cv`) | Not measured | Measuring it (open in `status.md`) | C |
| ≤ 2026-09-19 | CV-E06 | Show a value curve by year plus a brand comparison | A single price | One number hides depreciation, which was the original question | — | C |
| 2026-10-14 | — | Lock app dependencies from `requirements-venv_app.in` with `uv pip compile`; pin `scikit-learn` 1.8.0 and `pandas` 2.3.3 | Keep the `pip freeze` of the dev venv | Freeze had 111 packages, 18 duplicates, dev tools and 11 packages with advisories; the lock has 49 and none. The two pins protect the pickles | A retrain (then upgrade both) | A |
| 2026-10-14 | — | Follow the dicetamer project standard (modules: security, tests-python, deploy-coolify) | Own structure | Same shape as the other repos; the dicetamer audit can read it | The standard getting in the way here | C |
