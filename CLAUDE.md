# CLAUDE.md

Read this first. It exists so a task can start from one file instead of a sweep of the repo, and it
holds only what is expensive to discover and slow to change. Anything a single `grep` answers is left
out on purpose.

Follows the project standard in `dicetamer/standard/` (modules: security, tests-python,
deploy-coolify).

## What this project is

Estimates the value of a used car in Spain and how it depreciates over the years. About 16,800
listings from 2024 (40 popular models) were scraped, cleaned with a domain rule and used to train a
scikit-learn GradientBoosting pipeline on six features. A public Streamlit app
(car-value.zikzero.com) draws the value curve by year and compares brands instead of giving one
number. Deployed with Docker on Coolify.

## The rule that outranks every other rule

**The model and the filter options are pickles.** `models/2026-02-03/auto_ml_sklearn.pkl` (joblib)
and `data/processed/df_auto_filters.pkl` (pandas) only load reliably with the versions they were saved
with, so `scikit-learn==1.8.0` and `pandas==2.3.3` stay pinned in `requirements-venv_app.in`. Upgrade
them only together with a retrain, and check that `tests/test_smoke.py` still gets the reference
prediction.

## Hard rules

- **Language**: docs and code in English; commits in English.
- **The inference contract is fixed**: `km`, `fuel_type`, `age`, `brand`, `segment`, `body_type`, in
  that order (`src/inference/predict.py` reindexes to it). A new feature means a retrain and a new
  model folder, not an edit of the old one.
- **Models are versioned by date** in `models/<date>/`; switching means changing `MODEL_PATH` in
  `app/streamlit/utils/config.py`. Never overwrite a model file in place.
- **Logic lives in `src/`; the app only presents.** Notebooks and the app import the same modules.
- **Dependencies**: edit `requirements-venv_app.in`, then regenerate the lock with
  `uv pip compile requirements-venv_app.in --python-version 3.13 --upgrade -o requirements-venv_app.txt`.
  Never `pip freeze` into it (that is how it reached 111 packages in UTF-16).
- **Secrets never reach Claude or git**: `.env` and `config/api_keys.yaml` (Zyte key for the scraper)
  are gitignored and denied in `.claude/settings.json`; `app/streamlit/.streamlit/secrets.toml` is
  gitignored and dockerignored. The only runtime variable is `CLARITY_PROJECT_ID`, public by design.
- **Security**: before committing changes to the Dockerfile, analytics, cookies or anything that takes
  user input, run `/security-review`. The full-repo audit runs from dicetamer
  (`/security-audit car_value`).
- **Status lives in `docs/status.md`** and decisions in `docs/decisions.md`; update them in the same
  commit that changes them. Dates are absolute.

## Where things live

| Want to… | Open |
| --- | --- |
| Change what the model receives or returns | `src/inference/predict.py` |
| Switch the model or a feature toggle (analytics, consent, font) | `app/streamlit/utils/config.py` |
| Change the predictor page flow | `app/streamlit/pages/predictor.py`, `app/streamlit/utils/prediction_logic.py` |
| Change sidebar inputs | `app/streamlit/utils/ui_components.py` |
| Change charts and the brand comparison | `app/streamlit/utils/visualizations.py`, `chart_renderers.py`, `data_processing.py` |
| Change analytics or cookie consent | `app/streamlit/utils/analytics.py`, `cookie_consent.py` |
| Rebuild the dataset from raw HTML | `src/features/build_dataset.py` (raw data not in the repo) |
| Scrape listings | `src/scraping/scraper.py` (needs `config/`, not in the repo) |
| Train | `notebooks/auto_ml_sklearn.ipynb` |
| Build or deploy the image | `app/streamlit/Dockerfile`, `docs/deploy.md` |

## Commands

| For | Command |
| --- | --- |
| Run locally | `.\venv_app\Scripts\python.exe -m streamlit run app/streamlit/app.py` (from the repo root) |
| Tests | `.\venv_app\Scripts\python.exe -m pytest` (needs `requirements-dev.txt`) |
| Docker image | `docker build -t car-value-app -f app/streamlit/Dockerfile .` (context = repo root) |
| Install the secret scan (once per clone) | `pip install pre-commit && pre-commit install` |

## Traps that have already cost time here

- **Run Streamlit from the repo root.** Asset paths (`app/streamlit/assets/...`) and the model path
  are relative to it; running from `app/streamlit/` breaks the icon, fonts and imports.
- **The sidebar shows file names** ("app", "context", "predictor"…) instead of the `st.navigation`
  titles, with Streamlit 1.55 and 1.66 alike. Known, not yet investigated (`docs/status.md`).
- **`ui_theme.py` styles Streamlit's own markup** (`st.metric`, written for 1.52). After a Streamlit
  upgrade, check the predictor metrics still look right; they did on 1.66.
- **`scripts/patch_streamlit_iframe_policy.py` edits the installed Streamlit package** to silence
  console warnings. Local only; the Docker image does not run it.
- **Streamlit 1.66 replaced tornado with starlette/uvicorn.** `/_stcore/health` still works, so the
  Docker healthcheck and Coolify are unaffected.
- **The model is a sklearn Pipeline**: older docs and the portfolio say LightGBM, but the model in
  production is GradientBoosting (LightGBM tied in the comparison, see `docs/decisions.md`).

## Docs: read it when

| Document | Read it when |
| --- | --- |
| [`docs/README.md`](docs/README.md) | You need any other document |
| [`docs/status.md`](docs/status.md) | Deciding what to do next |
| [`docs/decisions.md`](docs/decisions.md) | Something looks odd: there is probably a reason |
| [`docs/how-it-works.md`](docs/how-it-works.md) | Touching inference or caching |
| [`docs/deploy.md`](docs/deploy.md) | Deploying, or changing the Dockerfile |
