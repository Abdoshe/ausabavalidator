class Error:
    """A location.Location and an error string."""
    def __init__(self, location, string):
        self.location = location
        self.string = string

    def __str__(self):
        return '<Error: {}: {}>'.format(self.location, self.string)

    def __eq__(self, other):
        if not isinstance(other, Error):
            return NotImplemented
        return self.location == other.location and self.string == other.string

    def __ne__(self, other):
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return equal

    def __lt__(self, other):
        if not isinstance(other, Error):
            return NotImplemented
        return self.location < other.location

    def __gt__(self, other):
        if not isinstance(other, Error):
            return NotImplemented
        return self.location > other.location
