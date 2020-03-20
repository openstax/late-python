import json
import pytest
import ipdb

from oxlate import Response
from .pytest_regex import pytest_regex

def test_basic(mocker):
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

def test_cookies(mocker):
    response = Response()
    response.add_cookie(name="foo", value="bar")
    assert response.to_dict() == {
        'status': 200,
        'headers': {
            'set-cookie': [
                {
                    'key': 'set-cookie',
                    'value': 'foo=bar'
                }
            ]
        }
    }

def test_delete_cookie(mocker):
    response = Response()
    response.delete_cookie(name="foo")
    assert response.to_dict() == {
        'status': 200,
        'headers': {
            'set-cookie': [
                {
                    'key': 'set-cookie',
                    'value': pytest_regex('foo=; Expires=.*')
                }
            ]
        }
    }

def test_more(mocker):
    response = Response(status=201) \
                   .set_status(204) \
                   .set_content_type_json() \
                   .set_body("howdy") \
                   .add_cookie(name="foo", value="bar") \
                   .add_cookie(name="yoyo", value="ma") \
                   .set_header(name="HI", value="THERE")

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
