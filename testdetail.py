import string
from rulesdetail import TRANSACTION_CODES
from rulesdetail import record_type, bsb_number, account_number, indicator, transaction_code


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


def test_account_number_valid_eight_digits_no_hyphen():
    all_lines = (' ' * 8 + ' 12345678', )
    assert account_number(all_lines, 0) is None


def test_account_number_valid_eight_digits_with_hyphen():
    all_lines = (' ' * 8 + '1234-5678', )
    assert account_number(all_lines, 0) is None


def test_account_number_valid_nine_digits():
    all_lines = (' ' * 8 + '123456789', )
    assert account_number(all_lines, 0) is None


def test_account_number_valid_blank():
    all_lines = (' ' * 8 + ' ' * 9, )  # for credit card transactions the account number can be blank
    assert account_number(all_lines, 0) is None


def test_account_number_valid_employee_benefits_card():
    all_lines = (' ' * 8 + '   999999', )  # for employee benefits card transactions, account number must be '999999'
    assert account_number(all_lines, 0) is None


def test_account_number_invalid_left_justified():
    all_lines = (' ' * 8 + '123456   ', )
    assert account_number(all_lines, 0) is not None


def test_account_number_invalid_bad_character():
    all_lines = (' ' * 8 + '   x23456', )
    assert account_number(all_lines, 0) is not None


def test_account_number_invalid_all_zeroes():
    all_lines = (' ' * 8 + '0' * 9, )
    assert account_number(all_lines, 0) is not None


def test_indicator_valid():
    good_chars = ' NWXY'
    all_lines = tuple((' ' * 17 + ch for ch in good_chars))
    for i, _ in enumerate(all_lines):
        assert indicator(all_lines, i) is None


def test_indicator_invalid():
    good_chars = ' NWXY'
    all_lines = tuple((' ' * 17 + ch for ch in string.printable if ch not in good_chars))
    for i, _ in enumerate(all_lines):
        assert indicator(all_lines, i) is not None


def test_transaction_code_valid():
    all_lines = tuple((' ' * 18 + code for code in TRANSACTION_CODES))
    for i, _ in enumerate(all_lines):
        assert transaction_code(all_lines, i) is None


def test_transaction_code_invalid():
    all_lines = tuple((' ' * 18 + code for code in ('  ', 'ab', '12', ')(')))
    for i, _ in enumerate(all_lines):
        assert transaction_code(all_lines, i) is not None
