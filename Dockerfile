FROM python:3.13-slim

# Install uv from astral image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set workdir
WORKDIR /app

# Copy dependency files first (better build cache)
COPY pyproject.toml uv.lock* ./

# Install deps
RUN uv sync --frozen --no-cache

# Copy source code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with uv
CMD ["uv", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
