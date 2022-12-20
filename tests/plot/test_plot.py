import matplotlib.pyplot as plt
import numpy as np

from smpl import plot


def gompertz(n, a, b):
    return -a * n * np.log(b * n)


def solution_gompertz(t, a, b, c):
    return 1 / b * np.exp(np.exp(-t * a) * c)


# @pytest.mark.line_profile.with_args(plot.function)
def test_em():
    for a in [1, 2]:
        for b in [1, 2]:
            plot.function(
                gompertz,
                a,
                b,
                xaxis="$N$",
                yaxis="$\\dot N$",
                xmin=0,
                xmax=5,
                init=False,
            )
    plt.show(block=False)
    plt.close()

    for a in [1, 2]:
        for b in [1, 2]:
            for c in [1, 2]:
                plot.function(
                    solution_gompertz,
                    a,
                    b,
                    c,
                    xaxis="$N$",
                    yaxis="$\\dot N$",
                    xmin=0,
                    xmax=5,
                    init=False,
                )
    plt.show(block=False)
    plt.close()
