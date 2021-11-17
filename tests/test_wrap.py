
from smpl import wrap
from smpl import functions


def test(x, a_0, phi):
    return x*a_0 + phi


print(wrap.get_latex(test))
print(wrap.get_latex(functions.linear))
print(functions.linear.__doc__)
