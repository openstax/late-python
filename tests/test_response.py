from oxlate import Response, ResponseCookie

import json
import pytest

from .pytest_regex import pytest_regex
import ipdb

def test_basic():
    response = Response(body="Hi")
    assert response.to_dict() == {
        'status': 200,
        'body': 'Hi',
        'headers': {
            'Content-Type': [
                {
                    'key': 'Content-Type',
                    'value': 'text/plain'
                }
            ]
        }
    }

def test_more(mocker):
    response = Response(status=201) \
                   .set_status(204) \
                   .set_content_type_json() \
                   .set_body("howdy")
    response.get_headers() \
            .set_response_cookie(ResponseCookie(name="foo", value="bar")) \
            .set_response_cookie(ResponseCookie(name="yoyo", value="ma")) \
            .set(name="HI", value="THERE")

    assert response.to_dict() == {
        'status': 204,
        'body': '"howdy"',
        'headers': {
            'Content-Type': [
                {
                    'key': 'Content-Type',
                    'value': 'application/json'
                }
            ],
            'set-cookie': [
                {
                    'key': 'set-cookie',
                    'value': 'foo=bar'
                }
            ],
            'set-cookiE': [
                {
                    'key': 'set-cookiE',
                    'value': 'yoyo=ma'
                }
            ],
            'HI': [
                {
                    'key': 'HI',
                    'value': 'THERE'
                }
            ]
        }
    }

def test_redirect_to(mocker):
    response = Response.redirect_to("http://www.example.com")

    assert response.to_dict() == {
        'status': 302,
        'statusDescription': 'Found',
        'headers': {
            'Location': [{
                'key': 'Location',
                'value': "http://www.example.com"
            }]
        }
    }

def test_set_header(mocker):
    response = Response().set_header('Foo', 'Bar')

    assert response.to_dict()['headers'] == {
        'Foo': [{
            'key': 'Foo',
            'value': 'Bar'
        }]
    }

def test_set_noindex(mocker):
    response = Response().set_noindex()

    assert response.to_dict()['headers'] == {
        'X-Robots-Tag': [{
            'key': 'X-Robots-Tag',
            'value': 'noindex'
        }]
    }

def test_set_cors(mocker):
    response = Response().set_cors(origin='*', methods='GET, HEAD')

    assert response.to_dict()['headers'] == {
        'Access-Control-Allow-Origin': [{
            'key': 'Access-Control-Allow-Origin',
            'value': '*'
        }],
        'Access-Control-Allow-Methods': [{
            'key': 'Access-Control-Allow-Methods',
            'value': 'GET, HEAD'
        }]
    }
