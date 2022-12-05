import pytest


def f(i):
    """
    >>> f(0)
    0
    """
    return i * 10


def g(n=10):
    """
    >>> g(10)
    450

    """
    return sum(f(i) for i in range(n))


@pytest.mark.line_profile.with_args(f, g)
def test_as_mark():

    assert g() == 450
