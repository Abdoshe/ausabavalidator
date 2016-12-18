from bounds import Bounds, BoundsSet


def test_bounds_set_greater_than_true():
    a = BoundsSet((Bounds(3, 7), Bounds(10, 15), Bounds(20, 22)))
    b = BoundsSet((Bounds(3, 7), Bounds(9, 15), Bounds(20, 22)))
    assert a > b


def test_bounds_set_greater_than_false():
    a = BoundsSet((Bounds(3, 7), Bounds(9, 15), Bounds(20, 22)))
    b = BoundsSet((Bounds(3, 7), Bounds(10, 15), Bounds(20, 22)))
    assert not (a > b)


def test_bounds_set_less_than_true():
    a = BoundsSet((Bounds(3, 7), Bounds(9, 15), Bounds(20, 22)))
    b = BoundsSet((Bounds(3, 7), Bounds(10, 15), Bounds(20, 22)))
    assert a < b


def test_bounds_set_less_than_false():
    a = BoundsSet((Bounds(3, 7), Bounds(10, 15), Bounds(20, 22)))
    b = BoundsSet((Bounds(3, 7), Bounds(9, 15), Bounds(20, 22)))
    assert not (a < b)
