# late-python

[![Build Status](https://travis-ci.org/openstax/late-python.svg?branch=master)](https://travis-ci.org/openstax/late-python)

A Python package with OpenStax Lambda@Edge ("lAMBDA at eDGE") utilities.

## Usage

```python
from oxlate import Event, Request, Response

def lambda_handler(event, context):
    request = Event(event).request()

    request.get_uri()
    request.set_uri("something") # used when changing the request mid-flight
    request.get_cookie("auth")
    request.viewer_country()  # requires 'cloudfront-viewer-country' header forwarding


    response = Response(status=302) \
                   .set_header(name='Location', value='https://openstax.org')

    return response.to_dict()
```

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

