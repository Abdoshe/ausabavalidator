import string
from rulesdetail import record_type


def test_record_type_valid():
    all_lines = ('1 (remainder of string should not matter)', )
    assert record_type(all_lines, 0) is None


def test_record_type_invalid():
    all_lines = tuple((ch for ch in string.printable if ch != '1'))  # '1' is the right character
    for i, _ in enumerate(all_lines):
        assert record_type(all_lines, i) is not None
