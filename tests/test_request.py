import json
import pytest
import ipdb

from oxlate import Request

def new_request(fragment):
    data = {
        "uri": "/foo",
        "headers": {
            "cloudfront-viewer-country": [
                {
                    "key": "CloudFront-Viewer-Country",
                    "value": "US"
                }
            ],
            "cookie": [
                {
                    "key": "cookie",
                    "value": "somename=put_a_cookie_value_here"
                }
            ],
        }
    }

    data.update(fragment)
    return Request(data)

def test_get_uri_when_present(mocker):
    request = new_request({"uri": "/psychology"})
    assert request.get_uri() == "/psychology"

def test_get_uri_when_absent(mocker):
    request = Request({})
    assert request.get_uri() == None

def test_set_uri(mocker):
    request = new_request({"uri": "foo"})
    request.set_uri("bar")
    assert request.to_dict()["uri"] == "bar"

def test_get_cookie_when_header_present(mocker):
    request = new_request({
        "headers": {
            "cookie": [
                {
                    "key": "cookie",
                    "value": "somename=blah; other=foo"
                }
            ],
        }
    })

    assert request.get_cookie(name="somename") == "blah"
    assert request.get_cookie(name="other") == "foo"
    assert request.get_cookie(name="howdy") == None

def test_get_cookie_when_header_absent(mocker):
    request = new_request({"headers": {}})

    assert request.get_cookie(name="howdy") == None

def test_to_dict(mocker):
    request = Request({"blah": "foo"})
    assert request.to_dict() == {"blah": "foo"}

def test_viewer_country_when_header_present(mocker):
    request = new_request({
        "headers": {
            "cloudfront-viewer-country": [
                {
                    "key": "CloudFront-Viewer-Country",
                    "value": "US"
                }
            ]
        }
    })

    assert request.viewer_country() == "US"

def test_viewer_country_when_header_absent(mocker):
    request = new_request({"headers": {}})
    assert request.viewer_country() == None
