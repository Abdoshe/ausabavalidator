def line_length(all_lines, line_num):
    line = all_lines[line_num]
    if len(line) != 120:
        return 'Line should be 120 characters long, is {} characters long'.format(len(line))
    return None


all_generic_rules = (line_length, )
