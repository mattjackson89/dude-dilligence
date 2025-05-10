FROM python:3.13.3-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Download the latest installer
ADD https://astral.sh/uv/0.5.30/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

# Copy all files needed for package installation
COPY app/ /app/app/
COPY dude_diligence/ /app/dude_diligence/

# Copy project files
COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --frozen --group app 

# Set Python path for imports
ENV PYTHONPATH="/app:/app/dude_diligence/:$PYTHONPATH"

# Configure environment variables
ENV GRADIO_SERVER_NAME="0.0.0.0" \
    GRADIO_SERVER_PORT=7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:7860/ || exit 1

# Expose Gradio interface port
EXPOSE 7860

# Run the application
CMD ["uv", "run", "python", "-m", "app.main"] 