import json
import pytest
import ipdb

from oxlate import Headers

def test_simple_add(mocker):
    headers = Headers()
    headers.add(name="foo", value="bar")
    assert headers.to_dict() == {
        "foo": [
            {
                'key': 'foo',
                'value': 'bar'
            }
        ]
    }

def test_simple_add_overwrite(mocker):
    headers = Headers()
    headers.add(name="foo", value="bar")
    headers.add(name="foo", value="howdy")
    assert headers.to_dict() == {
        "foo": [
            {
                'key': 'foo',
                'value': 'howdy'
            }
        ]
    }

def test_add_allowing_duplicates(mocker):
    headers = Headers()
    headers.add(name="Set-Cookie", value="bar", adjust_case_to_allow_duplicates=True)
    headers.add(name="Set-Cookie", value="howdy", adjust_case_to_allow_duplicates=True)
    headers.add(name="Set-Cookie", value="yoyo", adjust_case_to_allow_duplicates=True)
    assert headers.to_dict() == {
        "Set-Cookie": [
            {
                'key': 'Set-Cookie',
                'value': 'bar'
            }
        ],
        "set-cookie": [
            {
                'key': 'set-cookie',
                'value': 'howdy'
            }
        ],
        "set-cookiE": [
            {
                'key': 'set-cookiE',
                'value': 'yoyo'
            }
        ]
    }

def test_add_allowing_duplicates_but_none_left(mocker):
    headers = Headers()
    headers.add(name="a", value="bar", adjust_case_to_allow_duplicates=True)
    headers.add(name="A", value="howdy", adjust_case_to_allow_duplicates=True)

    with pytest.raises(RuntimeError, match=r".*no more case variants.*"):
        headers.add(name="a", value="yoyo", adjust_case_to_allow_duplicates=True)


