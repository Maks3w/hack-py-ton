FROM python:3.10.1-slim as production

RUN pip install --no-cache-dir pipenv==2020.11.15

ENV HOMEDIR=/project/src/ \
  TERM=vt100 \
  C_FORCE_ROOT=1 \
  PYTHONUNBUFFERED=1 \
  PIPENV_VERBOSE=True \
  SERVER_PORT=8000

EXPOSE $SERVER_PORT

WORKDIR $HOMEDIR

ARG PIPENV_ARGS

COPY src/Pipfile src/Pipfile.lock $HOMEDIR
RUN buildDeps="" \
  && apt-get update && apt-get install --assume-yes --no-install-recommends \
    $buildDeps \
    libmagic1 \
  && pipenv install --system --deploy $PIPENV_ARGS \
  && rm -rf ~/.cache/ \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false -o APT::AutoRemove::SuggestsImportant=false $buildDeps \
  && apt-get clean

COPY docker/bin/* /usr/local/bin/

USER www-data
