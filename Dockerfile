# ─────────────────────────────────────────────────────────────────
# Biomark — Production Docker Image
# Breast Cancer Multi-Omics Biomarker Discovery Platform
# ─────────────────────────────────────────────────────────────────
# Build:   docker build -t biomark:latest .
# Run:     docker run -p 8501:8501 biomark:latest
# ─────────────────────────────────────────────────────────────────

FROM python:3.11-slim

LABEL maintainer="Gnanam S <biognanam@gmail.com>"
LABEL description="Biomark — AI-enabled Multi-Omics Biomarker Platform"
LABEL version="2.0.0"

# ── System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# ── Non-root user for security
RUN groupadd -r biomark && useradd -r -g biomark biomark

WORKDIR /app

# ── Copy dependency spec first (layer caching)
COPY requirements.txt requirements.txt

# ── Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Copy application code
COPY . .

# ── Ensure data/reports directories exist with correct permissions
RUN mkdir -p data/sample data/uploads models reports \
    && chown -R biomark:biomark /app

# ── Switch to non-root user
USER biomark

# ── Streamlit configuration
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# ── Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--server.enableCORS=false", \
    "--server.maxUploadSize=200"]
