from datetime import datetime

from util import pluralise


class Validator:
    def __init__(self):
        pass

    @property
    def errors(self):
        raise NotImplementedError()

    @property
    def valid(self):
        return not self.errors


class StringValidator(Validator):
    """Most validators work with strings so this super class holds common functionality."""
    def __init__(self, string):
        super().__init__()
        self.string = string


class Length(StringValidator):
    """Check the string is exactly the given length."""
    def __init__(self, string, length):
        super().__init__(string)
        self.length = length

    @property
    def errors(self):
        if len(self.string) != self.length:
            return ('Expected string of length {}, got string of length {}'.format(self.length, len(self.string)), )
        return ()


class NotBlank(StringValidator):
    """Check the given string does not consist only of spaces"""
    @property
    def errors(self):
        if all((ch == ' ' for ch in self.string)):
            return ("Expected non-blank field but got all spaces", )
        return ()


class Blank(StringValidator):
    """Check the given string consists only of spaces."""
    @property
    def errors(self):
        if not all((ch == ' ' for ch in self.string)):
            return ("Expected all spaces but got '{}'".format(self.string), )
        return ()


class Literals(StringValidator):
    """Check the given string is in literals."""
    def __init__(self, string, literals):
        super().__init__(string)
        self.literals = literals

    @property
    def errors(self):
        if self.string not in self.literals:
            return ("Expected {literals} but got '{string}'"
                    .format(literals=pluralise(self.literals, "'{}'".format(self.literals[0]),
                                               'one of {}'.format(self.literals)),
                            string=self.string), )
        return ()


class JustifiedString(StringValidator):
    """Check that a string is correctly justified either right or left."""
    def __init__(self, string, left_justified):
        super().__init__(string)
        self.left_justified = left_justified

    @property
    def errors(self):
        if self.left_justified and self.string[0] == ' ':
            return ("Expected left-justified string but got a space at the start: '{}'".format(self.string), )
        elif not self.left_justified and self.string[-1] == ' ':
            return ("Expected right-justified string but got a space at the end: '{}'".format(self.string), )
        return ()


class Integer(StringValidator):
    """Check that every character in the string is a digit."""
    @property
    def errors(self):
        if not self.string.isdigit():
            return ("Expected all digits but got '{}'".format(self.string), )
        return ()


class Date(StringValidator):
    """Check that the string is a date in the format 'DDMMYY'."""
    @property
    def errors(self):
        try:
            datetime.strptime(self.string, '%d%m%y')
        except ValueError as err:
            return ("Expected a date in the format 'DDMMYY' but got '{}'".format(self.string), )
        return ()
