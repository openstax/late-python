import json
import pytest
import ipdb

from oxlate import Response

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
            'Set-Cookie': [
                {
                    'key': 'Set-Cookie',
                    'value': 'foo=bar'
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
            'Set-Cookie': [
                {
                    'key': 'Set-Cookie',
                    'value': 'foo=bar'
                }
            ],
            'set-cookie': [
                {
                    'key': 'set-cookie',
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
