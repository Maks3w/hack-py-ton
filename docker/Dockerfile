FROM python:3.13.4-slim as production

# e.g., using a hash from a previous release
COPY --from=ghcr.io/astral-sh/uv@sha256:2381d6aa60c326b71fd40023f921a0a3b8f91b14d5db6b90402e65a635053709 /uv /uvx /bin/

EXPOSE 8000

WORKDIR /project/src/

COPY src/uv.lock src/pyproject.toml ./
RUN uv sync --frozen --no-install-project

COPY docker/bin/* /usr/local/bin/
ADD src/ ./
RUN uv sync --frozen

USER www-data
