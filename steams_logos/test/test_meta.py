import pytest

from steams_logos.meta import load_from_json


def test_load_from_data():
    r = load_from_json('replaces')
    assert 'baseball' in r.keys()
