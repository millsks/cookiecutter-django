FROM python:3.13-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential curl ca-certificates gcc libpq-dev \
  && rm -rf /var/lib/apt/lists/*
# Ensure pip is up to date
RUN python -m pip install --upgrade pip
# Install tooling: cookiecutter, pixi, pre-commit
RUN pip install cookiecutter pixi pre-commit
WORKDIR /workspace
# Default entrypoint to allow script execution
ENTRYPOINT ["/bin/bash", "-lc"]
