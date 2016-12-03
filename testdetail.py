import string
from rulesdetail import TRANSACTION_CODES
from rulesdetail import record_type, bsb_number, account_number, indicator, transaction_code, amount, title
from rulesdetail import lodgement_reference, trace_record_bsb, trace_record_account_number, remitter_name
from rulesdetail import withholding_tax


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


def test_amount_valid():
    all_lines = tuple((' ' * 20 + '{:010d}'.format(i) for i in (1, 100, 10000, 1000000000, 9999999999)))
    for i, _ in enumerate(all_lines):
        assert amount(all_lines, i) is None


def test_amount_invalid():
    all_lines = tuple((' ' * 20 + amount_ for amount_ in ('not an amount', 'blah blah ' '          ')))
    for i, _ in enumerate(all_lines):
        assert amount(all_lines, i) is not None


def test_title_valid_full():
    all_lines = (' ' * 30 + 'x' * 32, )
    assert title(all_lines, 0) is None


def test_title_valid_left_justified():
    all_lines = (' ' * 30 + 'x' * 27 + ' ' * 5, )
    assert title(all_lines, 0) is None


def test_title_invalid_right_justified():
    all_lines = (' ' * 30 + ' ' * 5 + 'x' * 27, )
    assert title(all_lines, 0) is not None


def test_title_invalid_blank():
    all_lines = (' ' * 62, )
    assert title(all_lines, 0) is not None


def test_lodgement_reference_valid_full():
    all_lines = (' ' * 62 + 'x' * 18, )
    assert lodgement_reference(all_lines, 0) is None


def test_lodgement_reference_valid_left_justified():
    all_lines = (' ' * 60 + 'x' * 14 + ' ' * 4, )
    assert lodgement_reference(all_lines, 0) is None


def test_lodgement_reference_invalid_right_justified():
    all_lines = (' ' * 60 + ' ' * 4 + 'x' * 14, )
    assert lodgement_reference(all_lines, 0) is not None


def test_lodgement_reference_invalid_blank():
    all_lines = (' ' * 80, )
    assert lodgement_reference(all_lines, 0) is not None


def test_trace_record_bsb_valid():
    all_lines = (' ' * 80 + '123-456', )
    assert trace_record_bsb(all_lines, 0) is None


def test_trace_record_bsb_invalid_hyphen_missing():
    all_lines = (' ' * 80 + '123456', )
    assert trace_record_bsb(all_lines, 0) is not None


def test_trace_record_bsb_invalid_hyphen_replaced():
    all_lines = (' ' * 80 + '123 456', )
    assert trace_record_bsb(all_lines, 0) is not None


def test_trace_record_bsb_invalid_non_digit_in_first_triplet():
    all_lines = (' ' * 80 + '1a3-456', )
    assert trace_record_bsb(all_lines, 0) is not None


def test_trace_record_bsb_invalid_non_digit_in_second_triplet():
    all_lines = (' 123-45x      ', )
    assert trace_record_bsb(all_lines, 0) is not None


def test_trace_record_account_number_valid_eight_digits_no_hyphen():
    all_lines = (' ' * 87 + ' 12345678', )
    assert trace_record_account_number(all_lines, 0) is None


def test_trace_record_account_number_valid_eight_digits_with_hyphen():
    all_lines = (' ' * 87 + '1234-5678', )
    assert trace_record_account_number(all_lines, 0) is None


def test_trace_record_account_number_valid_nine_digits():
    all_lines = (' ' * 87 + '123456789', )
    assert trace_record_account_number(all_lines, 0) is None


def test_trace_record_account_number_valid_blank():
    all_lines = (' ' * 87 + ' ' * 9, )  # for credit card transactions the account number can be blank
    assert trace_record_account_number(all_lines, 0) is None


def test_trace_record_account_number_valid_employee_benefits_card():
    all_lines = (' ' * 87 + '   999999', )  # for employee benefits card transactions, account number must be '999999'
    assert trace_record_account_number(all_lines, 0) is None


def test_trace_record_account_number_invalid_left_justified():
    all_lines = (' ' * 87 + '123456   ', )
    assert trace_record_account_number(all_lines, 0) is not None


def test_trace_record_account_number_invalid_bad_character():
    all_lines = (' ' * 87 + '   x23456', )
    assert trace_record_account_number(all_lines, 0) is not None


def test_trace_record_account_number_invalid_all_zeroes():
    all_lines = (' ' * 87 + '0' * 9, )
    assert trace_record_account_number(all_lines, 0) is not None


def test_remitter_name_valid():
    all_lines = (' ' * 96 + 'X' * 16, )
    assert remitter_name(all_lines, 0) is None


def test_remitter_name_invalid_blank():
    all_lines = (' ' * 96 + ' ' * 16, )
    assert remitter_name(all_lines, 0) is not None


def test_remitter_name_invalid_right_justified():
    all_lines = (' ' * 96 + ' ' * 15 + 'X', )
    assert remitter_name(all_lines, 0) is not None


def test_withholding_tax_valid_zero():
    all_lines = (' ' * 112 + '0' * 8, )
    assert withholding_tax(all_lines, 0) is None


def test_withholding_tax_valid_non_zero():
    all_lines = (' ' * 112 + '12345678', )
    assert withholding_tax(all_lines, 0) is None


def test_withholding_tax_invalid():
    all_lines = (' ' * 112 + '1234567X', )
    assert withholding_tax(all_lines, 0) is not None
