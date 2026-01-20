FROM mcr.microsoft.com/devcontainers/python:1-3.13-bookworm

# Poetry 2.1.4
ARG POETRY_VERSION="2.1.4"
RUN if [ "${POETRY_VERSION}" != "none" ]; then su vscode -c "umask 0002 && pip3 install poetry==${POETRY_VERSION} poetry-plugin-export"; fi

# UV 0.9.2
ARG UV_VERSION="0.9.2"
RUN if [ "${UV_VERSION}" != "none" ]; then su vscode -c "umask 0002 && pip3 install uv==${UV_VERSION}"; fi

USER vscode
# Protobuf 32.1
ENV PB_REL="https://github.com/protocolbuffers/protobuf/releases"
RUN curl --output /tmp/protoc-32.1-linux-x86_64.zip -LO $PB_REL/download/v32.1/protoc-32.1-linux-x86_64.zip
RUN unzip /tmp/protoc-32.1-linux-x86_64.zip -d $HOME/.local
ENV HOME=/home/vscode
ENV PATH="$PATH:$HOME/.local/bin"