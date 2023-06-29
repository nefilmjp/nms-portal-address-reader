FROM python:3.9-slim

RUN apt-get update \
    && apt-get install -y libopencv-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip \
    && pip install --no-cache-dir pipenv \
    && pipenv install
