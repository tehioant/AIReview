ARG PREFECT_VERSION=3.1.5
ARG POETRY_VERSION=1.8.3

FROM prefecthq/prefect:${PREFECT_VERSION}-python3.11-kubernetes
LABEL io.prefect.version=${PREFECT_VERSION}

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

WORKDIR /opt/prefect/flows
COPY pyproject.toml poetry.lock ./

RUN poetry export --only prefect --without-hashes --format=requirements.txt --output=requirements.txt && \
    pip install -r requirements.txt

COPY ./src/aireview /opt/prefect/flows/aireview