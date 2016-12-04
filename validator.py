from itertools import chain
import guess
from rulesgeneric import all_generic_rules
from rulesdescriptive import all_descriptive_rules
from rulesdetail import all_detail_rules
from record import DESCRIPTIVE_RECORD, DETAIL_RECORD, TOTAL_RECORD


def nones_removed(seq):
    return (item for item in seq if item is not None)


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
        record_type = guess.record_type(all_lines, line_num)
        ruleset = {DESCRIPTIVE_RECORD: all_descriptive_rules,
                   DETAIL_RECORD: all_detail_rules,
                   TOTAL_RECORD: ()}[record_type]
        errors += get_ruleset_errors(all_lines, line_num, ruleset)
        if errors:
            error_dict[line_num] = errors
    return error_dict


def main():
    print("******** Warning: we're not checking for bad characters, a Valid response does not mean the file will "\
          "definitely be accepted by a particular financial institution ********")
    errors = get_all_errors(read_file('sample.aba'))
    if not errors:
        print('Valid')
    else:
        print('Errors detected: {}'.format(errors))


if __name__ == '__main__':
    main()
