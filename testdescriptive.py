import string
from rulesdescriptive import record_type, first_blank_field, reel_sequence_number, financial_institution
from rulesdescriptive import second_blank_field, user_name, acpa_number, description, date, last_blank_field


def test_record_type_valid():
    all_lines = ('0 (remainder of string should not matter)', )
    assert record_type(all_lines, 0) is None


def test_record_type_invalid():
    all_lines = tuple((ch for ch in string.printable if ch != '0'))  # '0' is the right character
    for i, _ in enumerate(all_lines):
        assert record_type(all_lines, i) is not None


def test_first_blank_field_valid():
    all_lines = ('0' + ' ' * 17, )
    assert first_blank_field(all_lines, 0) is None


def test_first_blank_field_invalid_one_short():
    all_lines = ('0' + ' ' * 16 + 'x <-- not a space', )
    assert first_blank_field(all_lines, 0) is not None


def test_reel_sequence_number_valid_one():
    all_lines = ('0' + ' ' * 17 + '01', )
    assert reel_sequence_number(all_lines, 0) is None


def test_reel_sequence_number_valid_multiple():
    all_lines = tuple(('0' + ' ' * 17 + '{:02d}'.format(i) for i in range(1, 100)))
    assert reel_sequence_number(all_lines, len(all_lines) - 1) is None


def test_reel_sequence_number_invalid_one():
    for i in range(100):
        if i == 1:
            continue  # 01 is correct as the first reel sequence number
        all_lines = ('0' + ' ' * 17 + '{:02d}'.format(i), )
        assert reel_sequence_number(all_lines, 0) is not None


def test_reel_sequence_number_invalid_multiple():
    all_lines = tuple(('0' + ' ' * 17 + '{:02d}'.format(i) for i in range(1, 99)))
    all_lines += ('0' + ' ' * 17 + '04', )  # '04' should be '99'
    assert reel_sequence_number(all_lines, len(all_lines) - 1) is not None


def test_financial_institution_valid():
    all_lines = tuple(('0' + ' ' * 19 + code for code in ('WBC', 'CBA', 'BQL')))
    for line_num, _ in enumerate(all_lines):
        assert financial_institution(all_lines, line_num) is None


def test_financial_institution_invalid():
    all_lines = tuple(('0' + ' ' * 19 + code for code in ('not', 'gud', '123')))
    for line_num, _ in enumerate(all_lines):
        assert financial_institution(all_lines, line_num) is not None


def test_second_blank_field_valid():
    all_lines = ('0' + ' ' * 22 + ' ' * 7, )
    assert second_blank_field(all_lines, 0) is None


def test_second_blank_field_invalid_one_short_right():
    all_lines = ('0' + ' ' * 22 + ' ' * 6 + 'x <-- not a space', )
    assert second_blank_field(all_lines, 0) is not None


def test_second_blank_field_invalid_one_short_left():
    all_lines = ('0' + ' ' * 22 + 'x' + ' ' * 6, )  # the 'x' should be a ' '
    assert second_blank_field(all_lines, 0) is not None


def test_user_name_valid_filled():
    all_lines = (' ' * 30 + 'COMPANYNAMEHEREXXXXXXXXXXX', )
    assert user_name(all_lines, 0) is None


def test_user_name_valid_left_justified():
    all_lines = (' ' * 30 + 'COMPANYNAMEHERE           ', )
    assert user_name(all_lines, 0) is None


def test_user_name_invalid_all_blank():
    all_lines = (' ' * 60, )
    assert user_name(all_lines, 0) is not None


def test_user_name_invalid_not_left_justified():
    all_lines = (' ' * 50 + 'name  ', )
    assert user_name(all_lines, 0) is not None


def test_acpa_number_valid():
    all_lines = (' ' * 56 + '123456', )
    assert acpa_number(all_lines, 0) is None


def test_acpa_number_invalid_space_padded():
    all_lines = (' ' * 56 + '  3456', )
    assert acpa_number(all_lines, 0) is not None


def test_acpa_number_invalid_non_digits():
    all_lines = (' ' * 56 + 'ABC123', )
    assert acpa_number(all_lines, 0) is not None


def test_description_valid_filled():
    all_lines = (' ' * 62 + 'PAYROLLXXXXX', )
    assert description(all_lines, 0) is None


def test_description_valid_left_justified():
    all_lines = (' ' * 62 + 'PAYROLL     ', )
    assert description(all_lines, 0) is None


def test_description_invalid_all_blank():
    all_lines = (' ' * 74, )
    assert description(all_lines, 0) is not None


def test_description_invalid_not_left_justified():
    all_lines = (' ' * 62 + '     PAYROLL', )
    assert description(all_lines, 0) is not None


def test_date_valid():
    all_lines = (' ' * 74 + '010116', )
    assert date(all_lines, 0) is None


def test_date_invalid_bad_date():
    all_lines = (' ' * 74 + '400116', )
    assert date(all_lines, 0) is not None


def test_date_invalid_wrong_format():
    all_lines = (' ' * 74 + '01-01-16', )
    assert date(all_lines, 0) is not None


def test_last_blank_field_valid():
    all_lines = (' ' * 120, )
    assert last_blank_field(all_lines, 0) is None


def test_last_blank_field_invalid():
    all_lines = (' ' * 90 + 'x' + ' ' * 29, )
    assert last_blank_field(all_lines, 0)
