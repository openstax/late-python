FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.local/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY . /code/

RUN python setup.py develop

# Install the unit test and distribution libraries
RUN pip install pytest pytest-mock ipdb setuptools wheel twine keyring --user

ENTRYPOINT ["/code/docker/entrypoint"]
