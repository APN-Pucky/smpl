import pytest


def f(i):
    return i * 10


def g(n=10):
    return sum(f(i) for i in range(n))


@pytest.mark.line_profile.with_args(f, g)
def test_as_mark():
    assert g() == 450
