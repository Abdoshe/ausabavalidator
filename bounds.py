class Bounds:
    """A range."""
    def __init__(self, start, end):
        """
        start: inclusive
        end: exclusive
        """
        self.start = start
        self.end = end

    @property
    def display(self):
        """The bounds as users expect them: a closed rather than half-open interval, indexed from 1 rather than 0."""
        return self.start + 1, self.end

    def __iter__(self):
        return iter((self.start, self.end))
