from collections import namedtuple

# all_lines contains the entire file contents as a sequence of strings
# line_num contains this field's line number (doubles as an index into all_lines)
LineData = namedtuple('LineData', 'all_lines line_num')


def pluralise(seq, singular, plural):
    """Convenience function to choose between singular and plural depending on whether seq has multiple items."""
    return plural if len(seq) >= 2 else singular


def length_from_range(range_):
    return (range_[1] - range_[0]) + 1


def slice_inclusive_range(seq, range_):
    return seq[range_[0]:range_[1] + 1]


def empties_removed(seq):
    return tuple((item for item in seq if item))
