"""
Write some tests!
"""

import pytest

from generate import determine_length, generate_password, roll_dice
from generate import chunks, validate_count


# simple add function for sanity check
def add_function(x):
    return x + 1


def test_add_function_pass():
    assert add_function(4) == 5


@pytest.mark.xfail
def test_determine_length():

    pw_length = determine_length()

    assert pw_length is not None


@pytest.mark.xfail
def test_generate_password():

    pw = generate_password()

    assert pw is not None


def test_roll_dice_is_list():

    r = roll_dice()

    # Test if roll result type is a list
    assert type(r) is list

    # Test for emptiness of various lists
    assert not [] is True  # This one is weird and confusing
    assert not []
    assert [1, 2, 3, 4, 5]
    assert r


@pytest.mark.parametrize('execution_number', range(100))
def test_roll_dice(execution_number):

    r = roll_dice()

    total = sum(r)

    assert total >= 25

    # This test will fail ~7% of the time, so it's considered brittle
    for i in {1, 2, 3, 4, 5, 6}:
        assert i in r


def test_chunks():

    inlist = [1, 2, 3, 4, 5]
    results = chunks(inlist, 1)

    assert results is not None


def test_validate_count():

    v1 = 4
    v2 = 5

    c1 = validate_count(v1)
    c2 = validate_count(v2)

    assert c1 == 4
    assert c2 == 5


def test_validate_count_throws_correct_exception():

    with pytest.raises(Exception):
        v3 = 6
        validate_count(v3)



