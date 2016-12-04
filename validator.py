from file import File


def read_file(filename):
    with open(filename) as f:
        string_all_lines = f.readlines()
    return tuple((line.rstrip('\n') for line in string_all_lines))


def get_all_errors(lines):
    return File(lines).errors


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
