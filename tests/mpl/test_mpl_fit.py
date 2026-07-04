import sys

import matplotlib.pyplot as plt
import numpy as np
import pytest
from uncertainties import unumpy as unp

from smpl import plot

pytestmark = pytest.mark.xfail(
    sys.version_info >= (3, 11),
    reason="pytest-mpl image comparison is currently failing on Python 3.11+.",
    strict=False,
)

@pytest.mark.mpl_image_compare(baseline_dir="baseline", remove_text=True)
def test_fit_str():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plot.fit("b*sin(x*c)", x, y)
    return plt.gcf()


@pytest.mark.mpl_image_compare(baseline_dir="baseline", remove_text=True)
def test_fit_lambda():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plot.fit(lambda a, b, c: b * unp.sin(a * c), x, y)
    return plt.gcf()
