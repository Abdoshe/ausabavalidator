def record_type(all_lines, line_num):
    # character 0
    line = all_lines[line_num]
    if line[0] != '1':
        return "The zeroth character in a detail record must be '1', was '{}'".format(line[0])
    return None


all_detail_rules = (record_type, )