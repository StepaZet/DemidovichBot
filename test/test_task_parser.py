import unittest
from providers.task_provider import _get_task_numbers_from_query


def test_finds_single_number():
    text = "1"
    assert _get_task_numbers_from_query(text) == ["1"]


def test_finds_multiple_numbers():
    text = "1 2 3"
    assert _get_task_numbers_from_query(text) == ["1", "2", "3"]


def test_finds_multiple_numbers_with_dots():
    text = "1.1 2.2 3.3"
    assert _get_task_numbers_from_query(text) == ["1.1", "2.2", "3.3"]


def test_finds_multiple_numbers_with_dots_and_commas():
    text = "1.1,2.2,3.3"
    assert _get_task_numbers_from_query(text) == ["1.1", "2.2", "3.3"]


def test_finds_range():
    text = "1-3"
    assert _get_task_numbers_from_query(text) == ["1", "2", "3"]


def test_returns_only_first_10_numbers():
    text = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15"
    expected = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    assert _get_task_numbers_from_query(text) == expected
    text = "1-15"
    assert _get_task_numbers_from_query(text) == expected


if __name__ == '__main__':
    unittest.main()
