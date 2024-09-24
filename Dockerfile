# Create a docker image that will eventually be deployed to run
# your AI agent on Atrium.
# Quoatas:
# - Max Image Size: 5GB
# - Max request size: 10MB
# - Max request timeout: 10 minutes
# - Max concurrent connections: 100
FROM python:3.12-slim AS atrium-codeserver

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY main.py .
# COPY .env* ./ 2>/dev/null || true

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
