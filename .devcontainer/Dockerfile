FROM python:3.9-slim

RUN apt-get update \
    && apt-get install -y \
    git \
    libopencv-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 devcontainer \
    && useradd --uid 1000 --gid 1000 -m -s /bin/bash devcontainer

RUN pip install --upgrade pip \
    pip install --no-cache-dir \
    flask \
    numpy \
    opencv-python \
    opencv-python-headless
