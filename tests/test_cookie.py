import json
import pytest
import ipdb
import datetime
import re

from oxlate import Cookie

def test_basic(mocker):
    cookie = Cookie(name="foo", value="bar")
    assert cookie.value() == "foo=bar"

def test_too_many_expires(mocker):
    with pytest.raises(ValueError, match=r".*not specify both.*"):
        Cookie(name="a", value="yoyo", expires_at=datetime.datetime.utcnow(), expires_days_from_now=4)

def test_path_domain(mocker):
    cookie = Cookie(name="foo", value="bar", path="/", domain="openstax.org")
    assert cookie.value() == "foo=bar; Path=/; Domain=openstax.org"

def test_expires_at(mocker):
    cookie = Cookie(name="foo", value="bar", expires_at=datetime.datetime.utcnow())
    assert re.search(r'Expires=.*GMT',cookie.value())

def test_expires_days_from_now(mocker):
    cookie = Cookie(name="foo", value="bar", expires_days_from_now=3)
    expires_at = datetime.datetime.strptime(cookie.value().split("; ")[1].split("=")[1], "%a, %d %b %Y %H:%M:%S GMT")
    delta = expires_at - datetime.datetime.utcnow()
    assert delta.days >= 2
    assert delta.days <= 4
