ARG PYTHON_VERSION=3.9.2-buster

# Python base image
FROM python:${PYTHON_VERSION} AS lana-store-python39-base

WORKDIR /wheels

COPY requirements.txt requirements_dev.txt ./

RUN set -x \
    # Generating wheels
    && pip install --upgrade pip \
    && pip wheel -r /wheels/requirements_dev.txt \
    # Cleaning up image
    && rm -rf /root/.cache


# Application development image
FROM python:${PYTHON_VERSION} AS lana-store-dev

COPY --from=lana-store-python39-base /wheels /wheels

RUN set -x \
    # Installing dependencies
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /wheels/requirements_dev.txt -f /wheels \
    # Cleaning up image
    && rm -rf /wheels \
    && rm -rf /root/.cache

WORKDIR /app

COPY . ./

CMD [ "uvicorn", "--reload", "--host", "0.0.0.0", "--port", "8000", "lana_store.main:app" ]
