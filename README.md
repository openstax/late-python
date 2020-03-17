# late-python

[![Build Status](https://travis-ci.org/openstax/late-python.svg?branch=master)](https://travis-ci.org/openstax/late-python)

A Python package with OpenStax Lambda@Edge ("lAMBDA at eDGE") utilities.

## Usage

...

## Development

All development is done inside a docker container.  From your host running Docker, in this directory run:

```
$> docker-compose up -d
%> ./docker/bash
```

This will drop you into the running container

## Run tests

From within the container, you can run tests with:

```
$ /code> python -m pytest
```

For debugging, you can use `ipdb`, e.g.

```
import ipdb; ipdb.set_trace()
```

When running tests with the debugger make sure to use the `-s` option to prevent pytest from capturing output.

`$> python -m pytest -s tests -k 'test_decrypts'`

Note that `pytest` is also on the `PATH` so you can call it directly.

## Distributing

...

