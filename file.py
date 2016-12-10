from component import Component
from records import record_type, record_from_line, DescriptiveRecord, DetailRecord
from validators import Validator


class FileValidator(Validator):
    """Superclass for validators that operate on an entire file."""
    def __init__(self, file):
        super().__init__()
        self.file = file


class RecordsValidator(FileValidator):
    """Run all the validators in all the records in file.records."""
    # Not in validators.py because it requires knowledge of the File class.
    @property
    def errors(self):
        return tuple(({'line': line_num, 'errors': record.errors}
                      for line_num, record in enumerate(self.file.records) if record.errors))


class ReelSequenceValidator(FileValidator):
    """Check that all reel sequence numbers are in sequential order."""
    @property
    def errors(self):
        current_sequence_number = 0
        for line_num, record in enumerate(self.file.records):
            if not isinstance(record, DescriptiveRecord):
                continue
            reel_sequence_string = record.fields['reel sequence'].string
            try:
                this_sequence_number = int(reel_sequence_string)
            except ValueError:
                error = 'Could not read one or more reel sequence numbers.  Expected an integer, got {}'\
                        .format(reel_sequence_string)
                return ({'line': line_num, 'error': error}, )
            if this_sequence_number != current_sequence_number + 1:
                error = 'Reel sequence number out of order.  Expected {:02d}, got {:02d}'\
                    .format(current_sequence_number + 1, this_sequence_number)
                return ({'line': line_num, 'error': error}, )
            current_sequence_number += 1
        return ()


class NetTotalValidator(FileValidator):
    """Check that the total record's net total field does contain the net total for the file."""
    @property
    def errors(self):
        # First check that all
        calculated_total = 0
        for line_num, record in enumerate(self.file.records):
            if not isinstance(record, DetailRecord):
                continue  # Only detail records contain transactions.  We'll check the total record at the end.
            transaction_code = tuple(record.fields.values())[4].string
            amount = int(tuple(record.fields.values())[5].string)
            is_debit = transaction_code == '13'  # all other codes denote credits
            if is_debit:
                calculated_total -= amount
            else:
                calculated_total += amount
        total_record = self.file.records[-1]
        read_total = int(tuple(total_record.fields.values())[3].string)
        if not calculated_total == read_total:
            line_num = len(self.file.records) - 1
            return ({'line': line_num,
                    'error': 'Expected net total of {} but got {}'.format(calculated_total, read_total)}, )
        return ()


class File(Component):
    def __init__(self, lines, validators=None):
        validators = validators or ()
        validators += (RecordsValidator(self), ReelSequenceValidator(self), NetTotalValidator(self))
        super().__init__(validators=validators)
        self.records = tuple((record_from_line(line) for line in lines))
