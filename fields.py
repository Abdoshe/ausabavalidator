from string import digits
from component import Component
from validators import Blank, JustifiedString, Integer, Date, BSB, Literals, NotLiterals, Characters, IntegerNonZero


class Field(Component):
    def __init__(self, string, validators=None):
        super().__init__(validators=validators)
        self.string = string


class BlankField(Field):
    def __init__(self, string, validators=None):
        super().__init__(string, validators=validators)
        self.validators += (Blank(string),)


class LiteralsField(Field):
    def __init__(self, string, literals, validators=None):
        super().__init__(string, validators=validators)
        self.literals = literals
        self.validators += (Literals(string, literals),)


class JustifiedField(Field):
    def __init__(self, string, left_justified=True, validators=None):
        super().__init__(string, validators=validators)
        self.left_justified = left_justified
        self.validators += (JustifiedString(string, left_justified), )


class IntegerField(Field):
    def __init__(self, string, validators=None):
        super().__init__(string, validators=validators)
        self.validators += (Integer(string),)


class DateField(Field):
    def __init__(self, string, validators=None):
        super().__init__(string, validators=validators)
        self.validators += (Date(string), )


class BSBField(Field):
    def __init__(self, string, validators=None):
        super().__init__(string, validators=validators)
        self.validators += (BSB(string), )


class AccountField(Field):
    def __init__(self, string, validators=None):
        super().__init__(string, validators=validators)
        self.validators += (NotLiterals(string, '0' * len(string)),
                            Characters(string, digits + '- '))


class AmountField(Field):
    def __init__(self, string, validators=None):
        super().__init__(string, validators=validators)
        self.validators += (IntegerNonZero(string), )


class FieldSpec:
    def __init__(self, name, bounds, class_, validators, *args):
        """
        Holds the info needed to create a specific field.

        name: the display name of this field type
        bounds: a pair denoting the starting and ending indexes to slice the field out of its line, i.e. [start, end)
        class_: the subclass of Field that should be used
        validators: a tuple of validators
        """
        self.name = name
        self.bounds = bounds
        self.class_ = class_
        self.validators = validators
        self.args = args

    @property
    def display_bounds(self):
        """The bounds as users expect them: a closed rather than half-open interval indexed from 1 rather than 0."""
        return self.bounds[0] + 1, self.bounds[1]

    def field(self, string):
        """Create a field from this FieldSpec containing the given string."""
        if self.args:
            return self.class_(string, *self.args, validators=self.validators)
        return self.class_(string, validators=self.validators)
