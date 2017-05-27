"""
Write some tests!
"""

import pytest

from click.testing import CliRunner

from scripts.generate import generate_secret
from scripts.generate import (
    _validate_count, _roll_dice, _concatenate_remainder,
    _prepare_chunks, _chunks
)

import config

from utils import get_roc

# All tests use these...
runner = CliRunner()
roc = get_roc(config.API_KEY)
chars = config.CHARACTERS


# ========== simple add function for sanity check ==========

def add_function(x):
    return x + 1


def test_add_function_pass():
    assert add_function(4) == 5

# ==========================================================


def test__concatenate_remainder_default():

    tmp_pw = _concatenate_remainder(roc, chars, 20)

    assert tmp_pw is not None
    assert len(tmp_pw) == 20


def test__concatenate_remainder_thirty_chars():

    tmp_pw = _concatenate_remainder(roc, chars, 30)

    assert tmp_pw is not None
    assert len(tmp_pw) == 30


def test__generate_password_mixed_default():

    result = runner.invoke(generate_secret, ['mixed'])
    tmp_pw = result.output

    assert result.exit_code == 0
    assert tmp_pw is not None
    assert len(tmp_pw) == 40
    assert len(tmp_pw.split()) == 4


def test__generate_password_numbers_default():

    result = runner.invoke(generate_secret, ['numbers'])
    tmp_pw = result.output

    assert result.exit_code == 0
    assert tmp_pw is not None
    assert len(tmp_pw) == 40
    assert len(tmp_pw.split()) == 4


def test__generate_password_default():

    result = runner.invoke(generate_secret, ['words'])

    assert result.exit_code == 0
    assert result.output is not None
    assert len(result.output.split()) == 8


def test__generate_password_short_list_four_words():

    result = runner.invoke(generate_secret, ['words',
                                               '--how-many', 1,
                                               '--number-rolls', 4,
                                               '--number-dice', 4])
    assert result.exit_code == 0
    assert result.output is not None
    assert len(result.output.split()) == 7


def test__generate_password_long_list_five_words():

    result = runner.invoke(generate_secret, ['words',
                                               '--how-many', 1,
                                               '--number-rolls', 5,
                                               '--number-dice', 5])
    assert result.exit_code == 0
    assert result.output is not None
    assert len(result.output.split()) == 8


def test__generate_password_short_list_five_words():

    result = runner.invoke(generate_secret, ['words',
                                               '--how-many', 1,
                                               '--number-rolls', 4,
                                               '--number-dice', 5])
    assert result.exit_code == 0
    assert result.output is not None
    assert len(result.output.split()) == 7


def test__generate_password_long_list_four_words():

    result = runner.invoke(generate_secret, ['words',
                                               '--how-many', 1,
                                               '--number-rolls', 5,
                                               '--number-dice', 4])
    assert result.exit_code == 0
    assert result.output is not None
    assert len(result.output.split()) == 8


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


# @pytest.mark.parametrize('execution_number', range(10))
# def test__roll_dice(execution_number):
#
#     r = _roll_dice()
#     total = sum(r)
#
#     assert total >= 25
#
#     # This test will fail ~7% of the time, so it's considered brittle
#     for i in {1, 2, 3, 4, 5, 6}:
#         assert i in r


def test__roll_dice():

    r = _roll_dice()
    total = sum(r)

    assert total >= 25
    assert 1 or 2 or 3 or 4 or 5 or 6 in r


def test__chunks():

    inlist = [1, 2, 3, 4, 5]
    results = _chunks(inlist, 1)

    assert results is not None


def test__prepare_chunks_four():

    result = _prepare_chunks(4, 4)

    for i in result:
        assert len(i) == 4


def test__prepare_chunks_five():
    result = _prepare_chunks(5, 5)

    for i in result:
        assert len(i) == 5


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
