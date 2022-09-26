# test_guess.py
# Unit tests for the compareWords function

import pytest
from wordle import compareWords


def test_length():
    with pytest.raises(Exception):
        compareWords("abcde", "abc")


def test_none():
    assert compareWords("abcde", "xxxxx") == [1, 1, 1, 1, 1]


def test_green():
    assert compareWords("abcde", "axxxx") == [3, 1, 1, 1, 1]
    assert compareWords("abcde", "axxxe") == [3, 1, 1, 1, 3]
    assert compareWords("abcde", "abcde") == [3, 3, 3, 3, 3]


def test_yellow():
    assert compareWords("abcde", "xxxxa") == [1, 1, 1, 1, 2]
    assert compareWords("abcde", "exxxa") == [2, 1, 1, 1, 2]
    assert compareWords("abcde", "bcdea") == [2, 2, 2, 2, 2]


def test_repeats_guess():
    assert compareWords("abcde", "xxxbb") == [1, 1, 1, 2, 1]
    assert compareWords("abcde", "bxxxx") == [2, 1, 1, 1, 1]
    assert compareWords("abcde", "bbxxx") == [1, 3, 1, 1, 1]
    assert compareWords("abcde", "xbbxx") == [1, 3, 1, 1, 1]


def test_repeats_solution():
    assert compareWords("radar", "axxxx") == [2, 1, 1, 1, 1]
    assert compareWords("radar", "aaxxx") == [2, 3, 1, 1, 1]
    assert compareWords("radar", "xaaxx") == [1, 3, 2, 1, 1]
    assert compareWords("radar", "xaxax") == [1, 3, 1, 3, 1]
    assert compareWords("radar", "xaaax") == [1, 3, 1, 3, 1]
    assert compareWords("radar", "rarax") == [3, 3, 2, 3, 1]
    assert compareWords("radar", "rrraa") == [3, 2, 1, 3, 2]
    assert compareWords("radar", "radar") == [3, 3, 3, 3, 3]
