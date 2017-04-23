"""
Write some tests!
"""

import pytest

from rdoclient import RandomOrgClient

from scripts.generate import generate_password
from scripts.generate import (
    _chunks, _validate_count, _roll_dice, _concatenate_remainder
)

import config


# ========== simple add function for sanity check ==========

def add_function(x):
    return x + 1


def test_add_function_pass():
    assert add_function(4) == 5

# ==========================================================


def get_roc(api_key):
    """
    Get instance of RandomOrgClient for testing.

    :param api_key: API key to fetch API client
    :return: instance of ROC
    """

    try:
        return RandomOrgClient(api_key=config.API_KEY)

    except (ValueError, AttributeError) as e:
        print(e)

    finally:
        print('API key {0} not working...'.format(api_key))
        raise ValueError


def test__concatenate_remainder():

    pw_length = _concatenate_remainder(get_roc, config.CHARACTERS, 20)

    assert pw_length is not None


@pytest.mark.xfail
def test__generate_password():

    pw = generate_password()

    assert pw is not None


def test__roll_dice_is_list():

    r5 = _roll_dice()
    r4 = _roll_dice()

    # Test if roll result type is a list
    assert type(r5) is list
    assert type(r4) is list

    # Test for emptiness of various lists
    assert not [] is True  # This one is weird and confusing
    assert not []
    assert [1, 2, 3, 4, 5]
    assert r5, r4


@pytest.mark.parametrize('execution_number', range(1))
def test__roll_dice(execution_number):

    r = _roll_dice()

    total = sum(r)

    assert total >= 25

    # This test will fail ~7% of the time, so it's considered brittle
    for i in {1, 2, 3, 4, 5, 6}:
        assert i in r


def test__chunks():

    inlist = [1, 2, 3, 4, 5]
    results = _chunks(inlist, 1)

    assert results is not None


def test__validate_count():

    v1 = 4
    v2 = 5

    c1 = _validate_count(v1)
    c2 = _validate_count(v2)

    assert c1 == 4
    assert c2 == 5


def test__validate_count_throws_correct_exception():

    with pytest.raises(Exception):
        v3 = 6
        _validate_count(v3)
