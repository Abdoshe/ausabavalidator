from util import pluralise


class Bounds:
    """A range that does not contain negative values."""
    def __init__(self, start, end):
        """
        start: inclusive
        end: exclusive
        """
        if start < 0 or end < 0:
            raise ValueError('start and end must be greater than zero, got {} and {}'.format(start, end))
        self.start = start
        self.end = end

    @property
    def display_tuple(self):
        """The bounds as users expect them: a closed rather than half-open interval, indexed from 1 rather than 0."""
        return self.start + 1, self.end

    @property
    def display_string(self):
        """self.display_tuple formatted for users."""
        return pluralise(self.display_tuple, str(self.display_tuple[0]), '{}-{}'.format(*self.display_tuple))

    def __iter__(self):
        return iter((self.start, self.end))

    def __len__(self):
        return self.end - self.start

    def __eq__(self, other):
        if not isinstance(other, Bounds):
            return NotImplemented
        return self.start == other.start and self.end == other.end

    def __ne__(self, other):
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return equal

    def __str__(self):
        return '<Bounds: {}>'.format(self.display_string)
