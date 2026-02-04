# Use official Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# When building with context set to the repo root, copy only what we need
# Keep the same repo-relative layout expected by the app/config.
COPY app/streamlit/ /app/app/streamlit/

# Shared code and model artifacts
COPY src/ /app/src/
COPY models/ /app/models/

# Data artifact used to populate UI selectors (safe, reduced)
COPY data/processed/df_auto_filters.pkl /app/data/processed/df_auto_filters.pkl

# Install dependencies
COPY requirements-venv_app.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install curl for healthcheck
RUN apt-get update \
	&& apt-get install -y curl libgomp1 \
	&& rm -rf /var/lib/apt/lists/*

# Expose Streamlit default port
EXPOSE 8501

# Healthcheck for Streamlit app
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
	CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
CMD ["streamlit", "run", "app/streamlit/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
