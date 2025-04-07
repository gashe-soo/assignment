# syntax=docker/dockerfile:1

###############################################
# Builder Stage: Install dependencies & build #
###############################################
FROM python:3.13.1-alpine AS builder

RUN apk update && apk add --no-cache \
    build-base \
    curl \
    python3-dev \
    musl-dev \
    libffi-dev \
    openssl-dev

ENV POETRY_VERSION=2.0.1
RUN curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy dependency definitions to leverage Docker cache
COPY pyproject.toml poetry.lock* /app/

# Configure Poetry to create the virtual environment in the project directory
RUN poetry config virtualenvs.in-project true && \
    poetry install --without dev --no-interaction --no-ansi --no-root

# Copy the rest of your application code
COPY . /app

#######################################
# Final Stage: Minimal Runtime Image  #
#######################################
FROM python:3.13.1-alpine AS final

# Install runtime dependencies (MariaDB client libraries)
RUN apk update && apk add --no-cache mariadb-dev

WORKDIR /app

# Copy the built application and virtual environment from the builder stage
COPY --from=builder /app /app

# Set PATH to include the Poetry-managed virtual environment binaries
ENV PATH="/app/.venv/bin:$PATH"

# Expose the port on which the FastAPI app will run
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
