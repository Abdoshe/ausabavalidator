def record_type(all_lines, line_num):
    # character 0
    line = all_lines[line_num]
    if line[0] != '1':
        return "The zeroth character in a detail record must be '1', was '{}'".format(line[0])
    return None


def bsb_number(all_lines, line_num):
    # characters 1-7
    line = all_lines[line_num]
    bsb = line[1:8]
    if not (bsb[:3].isdigit() and bsb[4:].isdigit()):
        return 'The first three and last three characters of the BSB number must be digits, BSB given was: {}'\
            .format(bsb)
    if not bsb[3] == '-':
        return 'The fourth character of the BSB number must be -, instead was {}'.format(bsb[3])
    return None


all_detail_rules = (record_type, bsb_number)