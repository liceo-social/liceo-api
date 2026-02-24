########################
####  DEPENDENCIES  ####
########################
FROM python:3.13-slim AS builder
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    PYTHONFAULTHANDLER=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
RUN apt update && apt install -y build-essential
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-dev --locked --no-editable --no-install-project
RUN sed -i 's/app\/.venv\/bin\/python/usr\/local\/bin\/python/g' /app/.venv/bin/uvicorn

######################
####  PRODUCTION  ####
######################
FROM python:3.13-slim
COPY ./src /app
COPY --from=builder --chmod=+x /app/.venv/bin/uvicorn /usr/local/bin
COPY --from=builder /app/.venv/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
WORKDIR /app
ENV PATH=$PATH:/usr/local/bin \
    PYTHONPATH=/usr/local/lib/python3.13/site-packages
CMD [ "uvicorn", "main:main_docker", "--host", "0.0.0.0", "--port", "8000"]

