# Deploying on Coolify

Structure from `umami-infra/README.md` (dicetamer project standard, module `deploy-coolify`).

## 1. What is deployed

One container: the Streamlit app, served at **https://car-value.zikzero.com**. No database, no
volumes, no background jobs. The model and the filter options are baked into the image.

## 2. Architecture

```
Internet ─► Traefik (Coolify) ─► car-value container :8501 (Streamlit, starlette/uvicorn since 1.66)
                                    ├── models/2026-02-03/auto_ml_sklearn.pkl
                                    └── data/processed/df_auto_filters.pkl
```

## 3. What is stored where

| Data | Where | Backup |
| --- | --- | --- |
| Model and filter options | In the image, from git (`models/`, `data/processed/df_auto_filters.pkl`) | Git |
| Visitor analytics | Microsoft Clarity (only after cookie consent) | Not ours |
| Anything else | Nothing is persisted | — |

## 4. Prerequisites

- The zikzero Coolify server, with `car-value.zikzero.com` pointing to it.
- The repo connected to Coolify (github.com/Keizer55/car_value).

## 5. Environment variables

| Variable | Defined in | Required | Note |
| --- | --- | --- | --- |
| `CLARITY_PROJECT_ID` | Coolify → Environment Variables | No | Microsoft Clarity project id. Public by design (it ends up in the browser). Without it, analytics are simply off |

`.env.example` lists the same variable. Values live in Coolify, never in the repo. The app also reads
`app/streamlit/.streamlit/secrets.toml` if present; that file is gitignored and dockerignored, so it
never reaches the image built by Coolify.

## 6. Deploy

| Setting | Value |
| --- | --- |
| Build pack | Dockerfile |
| Base directory | `/` (the build context must be the repo root) |
| Dockerfile location | `/app/streamlit/Dockerfile` |
| Port exposed | 8501 |
| Healthcheck | Defined in the Dockerfile: `curl -f http://localhost:8501/_stcore/health` |

The image runs as an unprivileged user (`app`) on a pinned `python:3.13.12-slim`.

## 7. Validation after deploying

- [ ] Coolify shows the container as healthy.
- [ ] https://car-value.zikzero.com loads the predictor page.
- [ ] Pressing **Predict** with the defaults (SEAT, petrol, segment B, hatchback, 20,000 km, 2 years)
      shows an initial value of **20,667 €** — the same number `tests/test_smoke.py` checks.
- [ ] The cookie banner appears in a private window, and Clarity loads only after accepting.

## 8. Backups

Nothing to back up: the container is stateless and everything it serves comes from git.

## 9. Updates

- **Dependencies**: edit `requirements-venv_app.in`, regenerate the lock (see `CLAUDE.md`), run
  `pytest`, build the image locally (`docker build -t car-value-app -f app/streamlit/Dockerfile .`),
  then push. Keep `scikit-learn` and `pandas` pinned unless the model is retrained.
- **Model**: add a new `models/<date>/` folder, point `MODEL_PATH` in
  `app/streamlit/utils/config.py` to it, update the reference value in `tests/test_smoke.py`.
- **Rolling back**: redeploy the previous commit from Coolify.

## Pending confirmation

- Whether Coolify redeploys automatically on every push to `main` (assumed in the update steps above).
- The exact Coolify settings in section 6 were reconstructed from the Dockerfile and its comments,
  not read from the Coolify UI.
