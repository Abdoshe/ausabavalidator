import string
from rulesdescriptive import record_type, first_blank_field, reel_sequence_number, financial_institution
from rulesdescriptive import second_blank_field, user_name


def test_first_record_type_correct():
    all_lines = ('0 (remainder of string should not matter)', )
    assert record_type(all_lines, 0) is None


def test_first_record_type_wrong_character():
    all_lines = tuple((ch for ch in string.printable if ch != '0'))  # '0' is the right character
    for i, _ in enumerate(all_lines):
        assert record_type(all_lines, i) is not None


def test_first_blank_field_correct():
    all_lines = ('0' + ' ' * 17, )
    assert first_blank_field(all_lines, 0) is None


def test_first_blank_field_one_short():
    all_lines = ('0' + ' ' * 16 + 'x <-- not a space', )
    assert first_blank_field(all_lines, 0) is not None


def test_reel_sequence_number_correct_one():
    all_lines = ('0' + ' ' * 17 + '01', )
    assert reel_sequence_number(all_lines, 0) is None


def test_reel_sequence_number_correct_multiple():
    all_lines = tuple(('0' + ' ' * 17 + '{:02d}'.format(i) for i in range(1, 100)))
    assert reel_sequence_number(all_lines, len(all_lines) - 1) is None


def test_reel_sequence_number_wrong_one():
    for i in range(100):
        if i == 1:
            continue  # 01 is correct as the first reel sequence number
        all_lines = ('0' + ' ' * 17 + '{:02d}'.format(i), )
        assert reel_sequence_number(all_lines, 0) is not None


def test_reel_sequence_number_wrong_multiple():
    all_lines = tuple(('0' + ' ' * 17 + '{:02d}'.format(i) for i in range(1, 99)))
    all_lines += ('0' + ' ' * 17 + '04', )  # '04' should be '99'
    assert reel_sequence_number(all_lines, len(all_lines) - 1) is not None


def test_financial_institution_correct():
    all_lines = tuple(('0' + ' ' * 19 + code for code in ('WBC', 'CBA', 'BQL')))
    for line_num, _ in enumerate(all_lines):
        assert financial_institution(all_lines, line_num) is None


def test_financial_institution_wrong():
    all_lines = tuple(('0' + ' ' * 19 + code for code in ('not', 'gud', '123')))
    for line_num, _ in enumerate(all_lines):
        assert financial_institution(all_lines, line_num) is not None


def test_second_blank_field_correct():
    all_lines = ('0' + ' ' * 22 + ' ' * 7, )
    assert second_blank_field(all_lines, 0) is None


def test_second_blank_field_one_short_right():
    all_lines = ('0' + ' ' * 22 + ' ' * 6 + 'x <-- not a space', )
    assert second_blank_field(all_lines, 0) is not None


def test_second_blank_field_one_short_left():
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
