from datetime import datetime
import guess
from record import DESCRIPTIVE_RECORD


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


def user_name(all_lines, line_num):
    # characters 30-55
    line = all_lines[line_num]
    name = line[30:56]
    if name.isspace():
        return 'Characters 30-55 must not be all blank in a descriptive record'
    if name[0] == ' ':
        return 'User name must be left justified but there is a space at character 30'
    # Remaining specification depends on the financial institution so not much more we can do here
    return None


def acpa_number(all_lines, line_num):
    # characters 56-61
    line = all_lines[line_num]
    number = line[56:62]
    if not number.isdigit():
        return 'Characters 56-61 must contain an ACPA identification number, instead got {}'.format(number)
    return None


def description(all_lines, line_num):
    # characters 62-73
    line = all_lines[line_num]
    desc = line[62:74]
    if desc.isspace():
        return 'Characters 62-73 must not be all blank in a descriptive record'
    if desc[0] == ' ':
        return 'Description must be left justified but there is a space at character 62'
    return None


def date(all_lines, line_num):
    # characters 74-79
    line = all_lines[line_num]
    date_string = line[74:80]
    bad_format_error = 'Characters 74-79 must be a date in the format DDMMYY, instead were {}'.format(date_string)
    if not date_string.isdigit():
        return bad_format_error
    try:
        datetime.strptime(date_string, '%d%m%y')
    except ValueError as err:
        return bad_format_error
    return None


all_descriptive_rules = (record_type, first_blank_field, reel_sequence_number, financial_institution,
                         second_blank_field, user_name, acpa_number, description, date)
