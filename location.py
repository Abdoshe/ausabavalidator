from bounds import Bounds
from util import pluralise


class Location:
    """A line number and a bounds.Bounds."""
    def __init__(self, bounds, line_num=None):
        self.line_num = line_num
        # If bounds is a sequence, convert it to a Bounds.
        if not isinstance(bounds, Bounds):
            bounds = Bounds(bounds[0], bounds[1])
        self.bounds = bounds

    def __eq__(self, other):
        if not isinstance(other, Location):
            return NotImplemented
        return self.line_num == other.line_num and self.bounds == other.bounds

    def __ne__(self, other):
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return equal

    def __lt__(self, other):
        if not isinstance(other, Location):
            return NotImplemented
        if self.line_num < other.line_num:
            return True
        elif self.line_num > other.line_num:
            return False
        # line numbers are the same so check starting columns
        if self.bounds.start < other.bounds.start:
            return True
        elif self.bounds.start > other.bounds.start:
            return False
        # line numbers and start columns are the same so check end columns
        if self.bounds.end < other.bounds.end:
            return True
        return False

    def __gt__(self, other):
        if not isinstance(other, Location):
            return NotImplemented
        return self.__ne__(other) and not self.__lt__(other)

    def __str__(self):
        start, end = self.bounds.display_tuple
        return '<Location: line {}, {}>'.format(self.line_num, pluralise(set(self.bounds.display_tuple),
                                                                         'column {}'.format(self.bounds.display_string),
                                                                         'columns {}'.format(self.bounds.display_string)))
