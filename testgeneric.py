from rulesgeneric import line_length


def test_line_length_correct():
    all_lines = ('012345678901234567890123456789012345678901234567890123456789'
                 '012345678901234567890123456789012345678901234567890123456789', )
    assert line_length(all_lines, 0) is None


def test_line_length_short_one():
    all_lines = ('012345678901234567890123456789012345678901234567890123456789'
                 '01234567890123456789012345678901234567890123456789012345678', )
    assert line_length(all_lines, 0) is not None


def test_line_length_short_empty():
    all_lines = ('', )
    assert line_length(all_lines, 0) is not None


def test_line_length_short_space():
    all_lines = (' ', )
    assert line_length(all_lines, 0) is not None


def test_line_length_short_newline():
    all_lines = ('\n', )
    assert line_length(all_lines, 0) is not None


def test_line_length_long_one_digit():
    all_lines = ('012345678901234567890123456789012345678901234567890123456789'
                 '0123456789012345678901234567890123456789012345678901234567899', )
    assert line_length(all_lines, 0) is not None


def test_line_length_long_one_space():
    all_lines = ('012345678901234567890123456789012345678901234567890123456789'
                 '012345678901234567890123456789012345678901234567890123456789 ', )
    assert line_length(all_lines, 0) is not None
    
    
def test_line_length_long_one_newline():
    all_lines = ('012345678901234567890123456789012345678901234567890123456789'
                 '012345678901234567890123456789012345678901234567890123456789\n', )
    assert line_length(all_lines, 0) is not None
