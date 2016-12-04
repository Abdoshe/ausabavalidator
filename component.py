from itertools import chain


class Component:
    def __init__(self, validators=None):
        self.validators = () if validators is None else validators

    @property
    def errors(self):
        return tuple(chain(*(validator.errors for validator in self.validators)))

    @property
    def valid(self):
        return not self.errors



