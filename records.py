from collections import OrderedDict
from component import Component
from fields import FieldSpec, Field, BlankField, JustifiedField, IntegerField, DateField
from validators import Validator, Length, NotBlank, Integer, Literals


class FieldsValidator(Validator):
    """Run all the validators in all the fields in record.fields."""
    # Not in validators.py because it requires knowledge of the Record class.
    def __init__(self, record):
        super().__init__()
        self.record = record

    @property
    def errors(self):
        return ({'pos': spec.display_bounds, 'field': spec.name, 'errors': field.errors}
                for spec, field in self.record.fields.items() if field.errors)


class Record(Component):
    def __init__(self, line, field_specs, validators=None):
        entire_record_validators = (Length(line, 120), FieldsValidator(self))
        record_type_validators = (Integer(line[0]), Literals(line[0], ('0', '1', '7')))
        validators = validators or ()
        validators += entire_record_validators + record_type_validators
        super().__init__(validators=validators)

        self.field_specs = field_specs
        self.fields = OrderedDict()
        for spec in self.field_specs:
            start, end = spec.bounds
            self.fields[spec] = spec.field(line[start:end])


class DescriptiveRecord(Record):
    def __init__(self, line):
        field_specs = (FieldSpec('record type', (0, 1), IntegerField, ()),
                       FieldSpec('first blank field', (1, 18), BlankField, ()),
                       FieldSpec('reel sequence', (18, 20), IntegerField, ()),
                       FieldSpec('financial institution', (20, 23), Field, ()),
                       FieldSpec('second blank field', (23, 30), BlankField, ()),
                       FieldSpec('user name', (30, 56), JustifiedField, ()),
                       FieldSpec('APCA number', (56, 62), IntegerField, ()),
                       FieldSpec('description', (62, 74), JustifiedField, ()),
                       FieldSpec('date', (74, 80), DateField, ()),
                       FieldSpec('third blank field', (80, 120), BlankField, ()))

        # Validators require access to the substring and bounds so it's simpler to add them in a loop afterwards.
        for spec in field_specs:
            start, end = spec.bounds
            substring = line[start:end]
            spec.validators += (Length(substring, end - start), )

            if spec.name in ('user name', 'description'):
                spec.validators += (NotBlank(substring), )

        super().__init__(line, field_specs, validators=None)


class DetailRecord(Record):
    def __init__(self, line):
        field_specs = ()
        super().__init__(line, field_specs, validators=None)


class TotalRecord(Record):
    def __init__(self, line):
        field_specs = ()
        super().__init__(line, field_specs, validators=None)


def record_type(line):
    types = {'0': 'descriptive', '1': 'detail', '7': 'total'}
    type_ = types.get(line[0], None)
    return type_


def record_from_line(line):
    type_ = record_type(line)
    return {'descriptive': DescriptiveRecord(line),
            'detail': DetailRecord(line),
            'total': TotalRecord(line),
            None: Record(line, ())}[type_]
