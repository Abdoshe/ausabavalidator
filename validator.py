import guess
from rulesgeneric import all_generic_rules
from rulesdescriptive import all_descriptive_rules
from record import DESCRIPTIVE_RECORD, DETAIL_RECORD, TOTAL_RECORD
from itertools import chain


def nones_removed(seq):
    return (item for item in seq if item is not None)


def remove_empties_from_dict(dct):
    empty_keys = []
    for key, value in dct.items():
        if not value:
            empty_keys.append(key)
    for key in empty_keys:
        del dct[key]


def read_file(filename):
    with open(filename) as f:
        string_all_lines = f.readlines()
    return tuple((line.rstrip('\n') for line in string_all_lines))


def get_ruleset_errors(all_lines, line_num, ruleset):
    return tuple(chain(nones_removed((rule(all_lines, line_num) for rule in ruleset))))


def get_all_errors(all_lines):
    error_dict = {}
    for line_num, line in enumerate(all_lines):
        errors = get_ruleset_errors(all_lines, line_num, all_generic_rules)
        if guess.record_type(all_lines, line_num) == DESCRIPTIVE_RECORD:
            errors += get_ruleset_errors(all_lines, line_num, all_descriptive_rules)
        error_dict[line_num] = errors
    remove_empties_from_dict(error_dict)
    return error_dict


def main():
    errors = get_all_errors(read_file('sample.aba'))
    if not errors:
        print('Valid')
    else:
        print('Errors detected: {}'.format(errors))


if __name__ == '__main__':
    main()