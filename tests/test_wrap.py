import line_profiler
import pytest

from smpl import functions, wrap

profiler = line_profiler.LineProfiler()


@profiler
def lin_fun(x, a_0, phi):
    return x * a_0 + phi


@pytest.mark.line_profile.with_args(wrap.get_latex)
def test_wrap():
    print(wrap.get_latex(lin_fun))
    print(wrap.get_latex(functions.linear))
    print(functions.linear.__doc__)
    print(
        wrap.get_latex(
            lambda a, b, c, x: (a + b + c) * x,
        )
    )
