FROM mcr.microsoft.com/devcontainers/python:1-3.13-bookworm

# UV 0.12.19
ARG UV_VERSION="0.12.19"
RUN if [ "${UV_VERSION}" != "none" ]; then su vscode -c "umask 0002 && pip3 install uv==${UV_VERSION}"; fi

# OPENCODE
ARG OPENCODE_VERSION="1.18.33"
RUN rm -f /etc/apt/sources.list.d/yarn.list; \
    apt-get update; \
    apt-get install -y --no-install-recommends npm; \
    npm install -g opencode-ai@${OPENCODE_VERSION}; \
    npm cache clean --force; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*


USER vscode

# Protobuf 32.1
ENV PB_REL="https://github.com/protocolbuffers/protobuf/releases"
RUN curl --output /tmp/protoc-32.1-linux-x86_64.zip -LO $PB_REL/download/v32.1/protoc-32.1-linux-x86_64.zip
RUN unzip /tmp/protoc-32.1-linux-x86_64.zip -d $HOME/.local

ENV HOME=/home/vscode
ENV PATH="$PATH:$HOME/.local/bin"