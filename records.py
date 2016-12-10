from collections import OrderedDict
from component import Component
from bounds import Bounds
from fields import FieldSpec, Field, BlankField, LiteralsField, JustifiedField, IntegerField, DateField, BSBField
from fields import AccountNumberField, AmountField
from validators import Validator, Length, NotBlank, Integer, Literals


class FieldsValidator(Validator):
    """Run all the validators in all the fields in record.fields."""
    # Not in validators.py because it requires knowledge of the Record class.
    def __init__(self, record):
        super().__init__()
        self.record = record

    @property
    def errors(self):
        return ({'pos': field.spec.bounds.display_tuple, 'field': field.spec.name, 'errors': field.errors}
                for field in self.record.fields.values() if field.errors)


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
            self.fields[spec.name] = spec.field(line[start:end])


class DescriptiveRecord(Record):
    def __init__(self, line):
        field_specs = (FieldSpec('record type', Bounds(0, 1), IntegerField, ()),
                       FieldSpec('first blank field', Bounds(1, 18), BlankField, ()),
                       FieldSpec('reel sequence', Bounds(18, 20), IntegerField, ()),
                       FieldSpec('financial institution', Bounds(20, 23), Field, ()),
                       FieldSpec('second blank field', Bounds(23, 30), BlankField, ()),
                       FieldSpec('user name', Bounds(30, 56), JustifiedField, ()),
                       FieldSpec('APCA number', Bounds(56, 62), IntegerField, ()),
                       FieldSpec('description', Bounds(62, 74), JustifiedField, ()),
                       FieldSpec('date', Bounds(74, 80), DateField, ()),
                       FieldSpec('third blank field', Bounds(80, 120), BlankField, ()))

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
        field_specs = (FieldSpec('record type', Bounds(0, 1), IntegerField, ()),
                       FieldSpec('bsb number', Bounds(1, 8), BSBField, ()),
                       FieldSpec('account number', Bounds(8, 17), AccountNumberField, ()),
                       FieldSpec('indicator', Bounds(17, 18), LiteralsField, (), (' ', 'N', 'W', 'X', 'Y')),
                       FieldSpec('transaction code', Bounds(18, 20), LiteralsField, (),
                                 (('13', ) + tuple((str(i) for i in range(50, 58))))),
                       FieldSpec('amount', Bounds(20, 30), AmountField, ()),
                       FieldSpec('account name', Bounds(30, 62), JustifiedField, ()),
                       FieldSpec('lodgement reference', Bounds(62, 80), JustifiedField, ()),
                       FieldSpec('trace bsb number', Bounds(80, 87), BSBField, ()),
                       FieldSpec('trace account number', Bounds(87, 96), AccountNumberField, ()),
                       FieldSpec('remitter name', Bounds(96, 112), JustifiedField, ()),
                       FieldSpec('withholding tax', Bounds(112, 120), IntegerField, ()))
        for spec in field_specs:
            start, end = spec.bounds
            substring = line[start:end]
            spec.validators += (Length(substring, end - start), )
            if spec.name in ('account name', 'lodgement reference', 'remitter name'):
                # TODO: can lodgement reference be blank?  Need to double-check
                spec.validators += (NotBlank(substring), )

        super().__init__(line, field_specs, validators=None)


class TotalRecord(Record):
    def __init__(self, line):
        field_specs = (FieldSpec('record type', Bounds(0, 1), IntegerField, ()),
                       FieldSpec('bsb filler', Bounds(1, 8), LiteralsField, (), ('999-999', )),
                       FieldSpec('first blank field', Bounds(8, 20), BlankField, ()),
                       FieldSpec('net total', Bounds(20, 30), IntegerField, ()),
                       FieldSpec('credit total', Bounds(30, 40), IntegerField, ()),
                       FieldSpec('debit total', Bounds(40, 50), IntegerField, ()),
                       FieldSpec('second blank field', Bounds(50, 74), BlankField, ()),
                       FieldSpec('descriptive record count', Bounds(74, 80), IntegerField, ()),
                       FieldSpec('third blank field', Bounds(80, 120), BlankField, ()))
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
