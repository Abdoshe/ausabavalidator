from bounds import Bounds
from util import pluralise


class Location:
    """A line number and a range."""
    def __init__(self, line_num, bounds):
        self.line_num = line_num
        # If bounds is a sequence, convert it to a Bounds.
        if not isinstance(bounds, Bounds):
            bounds = Bounds(bounds[0], bounds[1])
        self.bounds = bounds

    def __eq__(self, other):
        return self.line_num == other.line_num and self.bounds == other.bounds

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        start, end = self.bounds.display_tuple
        return '<Location: line {}, {}>'.format(self.line_num, pluralise(set(self.bounds.display_tuple),
                                                                         'column {}'.format(self.bounds.display_string),
                                                                         'columns {}'.format(self.bounds.display_string)))
