# Core versions we want to pin against
ARG PYTHON_VERSION=3.13
ARG POETRY_VERSION=2.1.3

FROM mirror.gcr.io/python:${PYTHON_VERSION}-slim AS builder
ARG POETRY_VERSION

# Since this is a build image, it is root user
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_ROOT_USER_ACTION=ignore \
    POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock .
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"
RUN poetry install --no-cache

FROM gcr.io/distroless/python3:nonroot
#FROM python:3.13-slim
ARG PYTHON_VERSION

# Copy in just the python dependencies needed
COPY --from=builder /usr/local/lib/python${PYTHON_VERSION}/site-packages/ /usr/local/lib/python${PYTHON_VERSION}/site-packages/
COPY server.py /app/server.py
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION}/site-packages \
    FLASK_ENV=development
#RUN chmod -v 0755 /app/server.py
CMD ["/app/server.py"]
#CMD ["python", "/app/server.py"]
EXPOSE 6500
