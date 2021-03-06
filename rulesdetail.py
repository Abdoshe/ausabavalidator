import string

TRANSACTION_CODES = ('13', ) + tuple((str(i) for i in range(50, 58)))


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


def account_number(all_lines, line_num):
    # characters 8-16
    line = all_lines[line_num]
    account = line[8:17]
    good_chars = string.digits + ' -'
    if not all((ch in good_chars for ch in account)):
        return 'Account number can only contain digits, hyphens, and spaces, instead was {}'.format(account)
    if not account.isspace() and account[-1] == ' ':
        return 'If not completely blank, account number must be right-justified and padded with spaces, '\
               'instead was: {}'.format(account)
    if all((ch == '0' for ch in account)):
        return 'Account number can not be all zeroes'
    return None


def indicator(all_lines, line_num):
    # character 17
    line = all_lines[line_num]
    indicator_ = line[17]
    good_chars = ' NWXY'
    if not indicator_ in good_chars:
        return 'Indicator must be one of {}, instead was {}'.format(good_chars, indicator_)


def transaction_code(all_lines, line_num):
    # characters 18-19
    line = all_lines[line_num]
    code = line[18:20]
    if code not in TRANSACTION_CODES:
        return 'Transaction code must be one of {}, instead was {}'.format(TRANSACTION_CODES, code)
    return None


def amount(all_lines, line_num):
    # characters 20-29
    line = all_lines[line_num]
    amount_ = line[20:30]
    if not amount_.isdigit():
        return 'Amount must be all digits, instead was {}'.format(amount_)
    return None


def title(all_lines, line_num):
    # characters 30-61
    line = all_lines[line_num]
    title_ = line[30:62]
    if title_.isspace():
        return 'Account title must not be blank'
    if title_[0] == ' ':
        return 'Account title must be left-justified'
    return None


def lodgement_reference(all_lines, line_num):
    # characters 62-79
    line = all_lines[line_num]
    reference = line[62:80]
    if reference.isspace():
        return 'Lodgement reference cannot be blank'
    if reference[0] == ' ':
        return 'Lodgement reference must be left-justified'
    return None


def trace_record_bsb(all_lines, line_num):
    # characters 80-86
    line = all_lines[line_num]
    trace = line[80:87]
    if not (trace[:3].isdigit() and trace[4:].isdigit()):
        return 'The first three and last three characters of the trace record must be digits, trace record given was: '\
                '{}'.format(trace)
    if not trace[3] == '-':
        return 'The fourth character of the trace record must be -, instead was {}'.format(trace[3])
    return None


def trace_record_account_number(all_lines, line_num):
    # characters 87-95
    line = all_lines[line_num]
    account = line[87:96]
    good_chars = string.digits + ' -'
    if not all((ch in good_chars for ch in account)):
        return 'Account number can only contain digits, hyphens, and spaces, instead was {}'.format(account)
    if not account.isspace() and account[-1] == ' ':
        return 'If not completely blank, account number must be right-justified and padded with spaces, ' \
               'instead was: {}'.format(account)
    if all((ch == '0' for ch in account)):
        return 'Account number can not be all zeroes'
    return None


def remitter_name(all_lines, line_num):
    # characters 96-111
    line = all_lines[line_num]
    name = line[96:112]
    if name.isspace():
        return 'Remitter name cannot be blank'
    if name[0] == ' ':
        return 'Remitter name must be left justified'
    return None


def withholding_tax(all_lines, line_num):
    # characters 112-119
    line = all_lines[line_num]
    tax = line[112:120]
    if not tax.isdigit():
        return 'Withholding tax must be all digits, instead was {}'.format(tax)
    return None


all_detail_rules = (record_type, bsb_number, account_number, indicator, transaction_code, amount, title,
                    lodgement_reference, trace_record_bsb, trace_record_account_number, remitter_name, withholding_tax)
