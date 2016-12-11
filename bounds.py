from bitarray import bitarray
from util import pluralise


# monkey-patch bitarray to allow setting the nth bit
def bitarray_set_ith_value(self, i, value):
    """Set the ith bit to value, extending the bit array if i is out of bounds."""
    try:
        self.pop(i)
    except IndexError:
        short_by = i - self.length()
        self.extend([0] * short_by)
    self.insert(i, value)

bitarray.set = bitarray_set_ith_value


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
        """
        The bounds as users expect them: a closed rather than half-open interval, indexed from 1 rather than 0.
        """
        return self.start + 1, self.end

    @property
    def display_string(self):
        """self.display_tuple formatted for users."""
        return pluralise(set(self.display_tuple), str(self.display_tuple[0]), '{}-{}'.format(*self.display_tuple))

    def to_bitset(self):
        """Calculate the bitset matching self.start and self.end."""
        return bitarray([0] * self.start + [1] * (self.end - self.start))

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

    def __lt__(self, other):
        if not isinstance(other, Bounds):
            return NotImplemented
        if self.start == other.start:
            return self.end < other.end
        return self.start < other.start

    def __gt__(self, other):
        if not isinstance(other, Bounds):
            return NotImplemented
        if self.start == other.start:
            return self.end > other.end
        return self.start > other.start

    def __str__(self):
        return '<Bounds: {}>'.format(self.display_string)

    def __hash__(self):
        return hash((self.start, self.end))


class BoundsSet:
    @classmethod
    def from_bitset(cls, bitset):
        return cls(BoundsSet.bounds_tuple_from_bitset(bitset))

    @classmethod
    def bounds_tuple_from_bitset(cls, bitset):
        bounds_list = []
        in_bounds = False
        start = None  # starting index of the Bounds we're currently in
        for i, value in enumerate(bitset):
            if not in_bounds and value:
                in_bounds = True
                start = i
            elif in_bounds and not value:
                in_bounds = False
                bounds_list.append(Bounds(start, i))
                start = None
        if start is not None:
            # we must've ended inside a bounds so add it to the list
            bounds_list.append(Bounds(start, bitset.length()))
        return tuple(bounds_list)

    def __init__(self, bounds_seq=None):
        bounds_seq = bounds_seq or ()
        self.set = set(bounds_seq)
        self._canonicalise()

    def to_bitset(self):
        bitset = bitarray()
        for bounds in self.set:
            for i in range(bounds.start, bounds.end):
                bitset.set(i, True)
        return bitset

    def _canonicalise(self):
        """Merge overlapping Bounds objects in self.set."""
        bitset = self.to_bitset()
        self.set = set(BoundsSet.bounds_tuple_from_bitset(bitset))

    def _union(self, other):
        """The union of the two sets."""
        bitset_a, bitset_b = sorted((self.to_bitset(), other.to_bitset()), key=lambda bs: bs.length())
        if bitset_a.length() < bitset_b.length():
            difference = bitset_b.length() - bitset_a.length()
            bitset_a += bitarray([0] * difference)
        return BoundsSet.from_bitset(bitset_a | bitset_b)

    def __or__(self, other):
        if not isinstance(other, BoundsSet):
            return NotImplemented
        return self._union(other)

    def __str__(self):
        tuple_str = str(tuple((bounds.display_string for bounds in sorted(self.set))))
        tuple_str_no_quotes = ''.join((ch for ch in tuple_str if ch != "'"))
        return '<BoundsSet: {}>'.format(tuple_str_no_quotes)
