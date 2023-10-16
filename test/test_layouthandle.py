from hamrep import layouthandle
import pytest


def test_to_matrix():
    l = ['a', 1,
         'b', 2,
         'c', 3]
    m = layouthandle.to_matrix(l, 2)
    o = [['a', 1], ['b', 2], ['c', 3]]

    assert m == o

    with pytest.raises(Exception) as excinfo:
        layouthandle.to_matrix(l, 4)
    assert str(excinfo.value) == "Number of columns 4 not allowed! 6 % 4 != 0 (2)"
