from component import Component
from records import record_type, record_from_line, DescriptiveRecord
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
            record_type_string = tuple(record.fields.values())[2].string  # Will always be the third field.
            try:
                this_sequence_number = int(record_type_string)
            except ValueError:
                return ()  # It will get picked up by the field validator which produces better error info.
            if this_sequence_number != current_sequence_number + 1:
                error = 'Reel sequence number out of order.  Expected {:02d}, got {:02d}'\
                    .format(current_sequence_number + 1, this_sequence_number)
                return ({'line': line_num, 'error': error}, )
            current_sequence_number += 1
        return ()


class File(Component):
    def __init__(self, lines, validators=None):
        validators = validators or ()
        validators += (RecordsValidator(self), ReelSequenceValidator(self))
        super().__init__(validators=validators)
        self.records = tuple((record_from_line(line) for line in lines))
