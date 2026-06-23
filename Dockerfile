FROM python:3.11-slim

# Everything happens inside /app within the container.
WORKDIR /app

# Install uv, our fast package manager.
RUN pip install uv

# Copy ONLY dependency files first (for build-cache efficiency), then install.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Now copy the application code.
COPY src ./src
COPY scripts ./scripts

# Tell the container how to start the app when it runs.
CMD ["uv", "run", "uvicorn", "supportgenie.api:app", "--host", "0.0.0.0", "--port", "8080"]