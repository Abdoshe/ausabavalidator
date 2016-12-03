import guess
from record import DESCRIPTIVE_RECORD
import string


def record_type(all_lines, line_num):
    # character 0
    line = all_lines[line_num]
    if line[0] != '0':
        return "The zeroth character in a descriptive record must be '0', was '{}'".format(line[0])
    return None


def first_blank_field(all_lines, line_num):
    # characters 1-17
    line = all_lines[line_num]
    if line[1:18] != ' ' * 17:
        return 'Characters 1-17 must be blank in a descriptive record'
    return None


def reel_sequence_number(all_lines, line_num):
    # characters 18-19
    current_sequence_number = 0
    for i, line in enumerate(all_lines):
        if guess.record_type(all_lines, i) != DESCRIPTIVE_RECORD:
            continue
        sequence_string = line[18:20]
        if not sequence_string.isdigit():
            return 'Reel sequence number at line {} is not a valid integer, should be two digits, was {}'.format(i, sequence_string)
        this_sequence_number = int(sequence_string)
        if this_sequence_number != current_sequence_number + 1:
            return 'Reel sequence numbers out of order.  Was expecting next (at line {}) to be {}, was instead {}'\
                .format(i, current_sequence_number + 1, this_sequence_number)
        current_sequence_number = this_sequence_number
    return None


def financial_institution(all_lines, line_num):
    # characters 20-22
    line = all_lines[line_num]
    institution = line[20:23]
    if institution not in ('WBC', 'CBA', 'BQL'):
        return 'Invalid financial institution: {} (probably a false positive, yet to add most banks'.format(institution)
    return None


def second_blank_field(all_lines, line_num):
    # characters 23-29
    line = all_lines[line_num]
    if line[23:30] != ' ' * 7:
        return 'Characters 23-29 must be blank in a descriptive record'
    return None


all_descriptive_rules = (record_type, first_blank_field, reel_sequence_number, financial_institution,
                         second_blank_field)
