from string import digits
from component import Component
from bounds import Bounds
from validators import Blank, JustifiedString, Integer, Date, BSB, Literals, NotLiterals, Characters, IntegerNonZero


class Field(Component):
    def __init__(self, string, spec, validators=None):
        super().__init__(validators=validators)
        self.string = string
        self.spec = spec  # The FieldSpec instance used to create this field


class BlankField(Field):
    def __init__(self, string, spec, validators=None):
        super().__init__(string, spec, validators=validators)
        self.validators += (Blank(string),)


class LiteralsField(Field):
    def __init__(self, string, spec, literals, validators=None):
        super().__init__(string, spec, validators=validators)
        self.literals = literals
        self.validators += (Literals(string, literals),)


class JustifiedField(Field):
    def __init__(self, string, spec, left_justified=True, validators=None):
        super().__init__(string, spec, validators=validators)
        self.left_justified = left_justified
        self.validators += (JustifiedString(string, left_justified), )


class IntegerField(Field):
    def __init__(self, string, spec, validators=None):
        super().__init__(string, spec, validators=validators)
        self.validators += (Integer(string),)


class DateField(Field):
    def __init__(self, string, spec, validators=None):
        super().__init__(string, spec, validators=validators)
        self.validators += (Date(string), )


class BSBField(Field):
    def __init__(self, string, spec, validators=None):
        super().__init__(string, spec, validators=validators)
        self.validators += (BSB(string), )


class AccountNumberField(Field):
    def __init__(self, string, spec, validators=None):
        super().__init__(string, spec, validators=validators)
        self.validators += (NotLiterals(string, '0' * len(string)),
                            Characters(string, digits + '- '))


class AmountField(Field):
    def __init__(self, string, spec, validators=None):
        super().__init__(string, spec, validators=validators)
        self.validators += (IntegerNonZero(string), )


class FieldSpec:
    def __init__(self, name, bounds, class_, validators, *args):
        """
        Holds the info needed to create a specific field.

        name: the display name of this field type
        bounds: a Bounds instance
        class_: the subclass of Field that should be used
        validators: a tuple of validators
        """
        self.name = name
        self.bounds = bounds
        self.class_ = class_
        self.validators = validators
        self.args = args

    def field(self, string):
        """Create a field from this FieldSpec containing the given string."""
        if self.args:
            return self.class_(string, self, *self.args, validators=self.validators)
        return self.class_(string, self, validators=self.validators)

    def __str__(self):
        return '<FieldSpec: {} of class {}>'.format(self.name, self.class_)
