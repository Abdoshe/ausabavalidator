# This module houses functions for guessing at what a line or field is supposed to be.
from record import DESCRIPTIVE_RECORD, DETAIL_RECORD, TOTAL_RECORD


def record_type(all_lines, line_num):
    line = all_lines[line_num]
    return {'0': DESCRIPTIVE_RECORD,
            '1': DETAIL_RECORD,
            '7': TOTAL_RECORD}[line[0]]
