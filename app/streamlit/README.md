# Streamlit App

This folder contains the frontend code for the Car Value Predictor using Streamlit.
It depends on the core logic defined in `src/` and the trained models in `models/`.

The **full training dataset is not included** in the repository. The app runs using the persisted model artifact under `models/`.

## Prerequisites
- Recommended Python: 3.13 (or match `venv_app`)

## Setup & Run

### 1. Local Python Environment

Create and install environment (PowerShell, run from **repository root**):

```powershell
# Create venv (adjust python path if needed)
python -m venv venv_app
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv_app\Scripts\Activate.ps1

# Install utils
python -m pip install --upgrade pip
python -m pip install -r requirements-venv_app.txt
```

Run the app (from the **repository root**):

```powershell
# Activate the virtual environment (PowerShell)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv_app\Scripts\Activate.ps1
streamlit run app/streamlit/app.py
```

> **Note:** We run from the repo root so that `src` imports work correctly (e.g., `from src.inference import predict`).

### 2. Docker

You can also run the app in a container. The Dockerfile is located in this folder but must be built from the root context.

**Build:**
```bash
# Run from repo root
docker build -t car-value-app -f app/streamlit/Dockerfile .
```

**Run:**
```bash
docker run -p 8501:8501 car-value-app
```
Then open http://localhost:8501

## Folder Structure

```
app/streamlit/
├── app.py                    # Main entry point with st.navigation()
├── pages/
│   ├── predictor.py         # Main prediction interface
│   └── context.py           # Project information page
├── utils/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration and constants
│   ├── data_processing.py   # Data manipulation and brand comparison logic
│   ├── visualizations.py    # Chart creation functions
│   ├── ui_components.py     # UI rendering components (tables, filters, buttons)
│   ├── ui_theme.py          # Theme and styling utilities
│   ├── prediction_logic.py  # Business logic and validations
│   └── chart_renderers.py   # High-level chart rendering
├── assets/
│   ├── fonts/               # Custom fonts for UI
│   │   ├── futuristic_1/   # Play font family
│   │   └── russo_one/      # Russo One font
│   └── icons/               # Favicon and images
├── .streamlit/
│   └── config.toml          # Streamlit theme configuration
└── Dockerfile               # Container definition
```

### Architecture

The app uses **Streamlit's multi-page navigation** (`st.navigation()`) to organize functionality:

- **app.py**: Navigation hub that defines pages with custom titles and icons
- **pages/**: Individual page modules for different sections of the app
- **utils/**: Reusable utility modules with clear separation of concerns:
  - UI components (sidebar, buttons, tables, brand comparison)
  - UI theme (styling and theme utilities)
  - Business logic (calculations, validations)
  - Chart rendering (comparative analysis, depreciation charts)
  - Data processing (formatting, transformations, brand comparison calculations)
  - Visualizations (low-level chart creation)

## Configuration

- The app reads configuration from `app/streamlit/utils/config.py`
- Model path: `models/2026-02-03/auto_ml_sklearn.pkl`
- Theme settings: `.streamlit/config.toml`
- It loads the model from `src.inference.predict` (defaulting to the latest configured model)

## Analytics (Microsoft Clarity)

Microsoft Clarity is **optional**. The app will only inject the tracking script if a project ID is configured.

Configuration options (checked in this order):
- `CLARITY_PROJECT_ID` in Streamlit secrets
- `CLARITY_PROJECT_ID` as an environment variable

### Local development

Create `app/streamlit/.streamlit/secrets.toml` (do not commit it):

```toml
CLARITY_PROJECT_ID = "<your-clarity-project-id>"
```

### Coolify

In your Coolify application settings:
- Add an environment variable (or secret) named `CLARITY_PROJECT_ID`
- Redeploy the app

If `CLARITY_PROJECT_ID` is not set, Clarity tracking is disabled.

