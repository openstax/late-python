import json
import pytest
import ipdb

from oxlate import Request

def test_get_uri_when_present(mocker):
    request = Request({"uri": "/psychology"})
    assert request.get_uri() == "/psychology"

def test_get_uri_when_absent(mocker):
    request = Request({})
    assert request.get_uri() == None

def test_set_uri(mocker):
    request = Request({"uri": "foo"})
    request.set_uri("bar")
    assert request.to_dict()["uri"] == "bar"

def test_get_cookie_when_header_present(mocker):
    request = Request({
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
    request = Request({
        "headers": {
        }
    })

    assert request.get_cookie(name="howdy") == None

def test_to_dict(mocker):
    request = Request({"blah": "foo"})
    assert request.to_dict() == {"blah": "foo"}

def test_viewer_country_when_header_present(mocker):
    request = Request({
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
    request = Request({
        "headers": {}
    })

    assert request.viewer_country() == None
