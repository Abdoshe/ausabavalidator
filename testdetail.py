import string
from rulesdetail import record_type, bsb_number


def test_record_type_valid():
    all_lines = ('1 (remainder of string should not matter)', )
    assert record_type(all_lines, 0) is None


def test_record_type_invalid():
    all_lines = tuple((ch for ch in string.printable if ch != '1'))  # '1' is the right character
    for i, _ in enumerate(all_lines):
        assert record_type(all_lines, i) is not None


def test_bsb_number_valid():
    all_lines = (' 123-456      ', )
    assert bsb_number(all_lines, 0) is None


def test_bsb_number_invalid_hyphen_missing():
    all_lines = (' 123456      ', )
    assert bsb_number(all_lines, 0) is not None


def test_bsb_number_invalid_hyphen_replaced():
    all_lines = (' 123 456      ', )
    assert bsb_number(all_lines, 0) is not None


def test_bsb_number_invalid_non_digit_in_first_triplet():
    all_lines = (' 1a3-456      ', )
    assert bsb_number(all_lines, 0) is not None


def test_bsb_number_invalid_non_digit_in_second_triplet():
    all_lines = (' 123-45x      ', )
    assert bsb_number(all_lines, 0) is not None
