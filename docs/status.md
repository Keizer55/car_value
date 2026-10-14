# Status

> **2026-10-14** · Deployed at car-value.zikzero.com. The model (2026-02-03) is trained on 2024
> listings; the repo follows the dicetamer project standard since today.

The single source of project status. The README links here and does not repeat it. Update it in the
same commit that closes or opens a milestone.

## Milestones

| | Milestone | Closed | How it was verified |
| --- | --- | --- | --- |
| ✅ | Dataset: ~16,800 listings from 2024, 40 models, cleaned with a domain rule (72 rows dropped, 0.4 %) | before 2026-02-03 | `notebooks/auto_ml_sklearn.ipynb` |
| ✅ | Model: GradientBoosting tuned with Optuna. Test (3,351 listings): MAE 2,396 €, RMSE 3,572 €, R² 0.796, MAPE 13.9 % | 2026-02-03 | Same notebook; artifact in `models/2026-02-03/` |
| ✅ | Streamlit app deployed with Docker on Coolify | date not recorded | car-value.zikzero.com |
| ✅ | Dependencies regenerated from a direct list: 111 → 49 packages, 0 known advisories; Streamlit 1.55 → 1.66 | 2026-10-14 | 60 predictions identical to the old environment; Docker image healthy |
| ✅ | Project standard: CLAUDE.md, docs index, status, decisions, security module, deploy guide, smoke tests | 2026-10-14 | `/project-audit car_value` from dicetamer |

`✅` done · `🚧` in progress · `🔲` pending

## Open

1. **Retrain with current listings.** 2024 was a year of new-car shortage; prices have probably
   moved. Needs a new scrape (the scraper config is not in the repo).
2. **Sidebar shows file names instead of the `st.navigation` titles** (`app.py` defines "🚗 Predictor 📉"
   etc.). Same on Streamlit 1.55 and 1.66; not investigated yet.
3. **Measure what horsepower and other features add** (CV-E05 was never measured).
4. Replace the `Styler.applymap` call in `app/streamlit/utils/ui_components.py` with `Styler.map`
   (pandas deprecation warning; harmless today).

## Parked

- **Second Python environment for PyCaret** (`requirements-venv_auto_ml_pycaret.txt`, Python 3.11):
  kept for the old notebooks only; scikit-learn + Optuna reached the same level (CV-E03).
