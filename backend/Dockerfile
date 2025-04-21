FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Copy pyproject.toml and README.md
COPY pyproject.toml README.md* ./

# Handle case where README.md might not exist
RUN touch README.md

# Install dependencies with explicit email-validator installation
RUN poetry install --no-interaction --no-ansi --only main --no-root && \
    pip install email-validator==2.1.0

# Copy application code
COPY . .

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 