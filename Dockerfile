# ---- Stage 1: Build dependencies ----
FROM python:3.11-slim as builder

WORKDIR /app

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --only main

# ---- Stage 2: Create the final application image ----
FROM python:3.11-slim

WORKDIR /app

# Set environment variables correctly (FIXED SECTION)
# This was misspelled as PYTHONTWRITEBYTECODE before
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"
# This is the most important fix: ensure the venv is in the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv ./.venv

# Copy the application source code from your local 'src' folder
# to the '/app/src' directory inside the container.
COPY ./src /app/src

# The default command now points to 'src.main:app'
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]