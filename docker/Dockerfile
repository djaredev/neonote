FROM python:3.13.5-alpine AS backend

WORKDIR /app

ENV UV_NO_CACHE=1

RUN --mount=type=bind,source=./backend/uv.lock,target=uv.lock \
    --mount=type=bind,source=./backend/pyproject.toml,target=pyproject.toml \
    --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv sync --locked --no-install-project --no-dev
#
COPY ./backend /app

ENV PATH="/app/.venv/bin:$PATH"
ENV DATA_DIR="/data"
ENV ENVIRONMENT="prod"

# Temporary environment variables for building the openapi scheme. 
# (Used only during the build stage; in the final image, they must be provded by the user) 
ENV SUPERUSER_USERNAME="admin"
ENV SUPERUSER_EMAIL="admin@localhost.com"
ENV SUPERUSER_PASSWORD="password"

RUN python -c "import neonote.main; import json; print(json.dumps(neonote.main.app.openapi()))" > openapi.json

FROM node:22.14-slim AS node-base
ENV PNPM_HOME="pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
WORKDIR /app

FROM node-base AS sdk

WORKDIR typescript-sdk
COPY ./sdk/typescript-sdk/package.json ./sdk/typescript-sdk/pnpm-lock.yaml .
RUN --mount=type=cache,id=pnpm,target=/pmpm/store pnpm install --frozen-lockfile
COPY ./sdk/typescript-sdk/ .
COPY --from=backend /app/openapi.json /app
RUN pnpm run openapi-ts && pnpm run build

FROM node-base AS frontend

RUN mkdir -p frontend && mkdir -p sdk/typescript-sdk
COPY ./frontend/package.json ./frontend/pnpm-lock.yaml /app/frontend
COPY --from=sdk /app/typescript-sdk ./sdk/typescript-sdk
WORKDIR /app/frontend
RUN --mount=type=cache,id=pnpm,target=/pmpm/store pnpm install --frozen-lockfile
COPY ./frontend/ /app/frontend
RUN pnpm run build

FROM backend AS build

COPY --from=frontend /app/frontend/build /app/neonote/frontend/

RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv sync --locked --no-dev --no-editable

# The final image
FROM python:3.13.5-alpine

WORKDIR /neonote

COPY --from=build /app/.venv /neonote/.venv

ENV PATH="/neonote/.venv/bin:$PATH"
ENV DATA_DIR="/data"
ENV ENVIRONMENT="prod"

EXPOSE 1717

CMD ["python", "-m", "neonote"]

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD python -m neonote.scripts.healthcheck
