from itertools import chain
from component import Component
from records import record_from_line
from util import empties_removed
from validators import Validator


class FileValidator(Validator):
    """Run all the validators in all the records in file.records."""
    # Not in validators.py because it requires knowledge of the File class.
    def __init__(self, file):
        super().__init__()
        self.file = file

    @property
    def errors(self):
        return tuple(({'line': line_num, 'errors': record.errors}
                      for line_num, record in enumerate(self.file.records) if record.errors))


class File(Component):
    def __init__(self, lines, validators=None):
        validators = (validators or ()) + (FileValidator(self), )
        super().__init__(validators=validators)
        self.records = tuple((record_from_line(line) for line in lines))
