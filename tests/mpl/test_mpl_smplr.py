import sys

import matplotlib.pyplot as plt
import numpy as np
import pytest

from smpl import plot

pytestmark = pytest.mark.xfail(
    sys.version_info >= (3, 11),
    reason="pytest-mpl image comparison is currently failing on Python 3.11+.",
    strict=False,
)

@pytest.mark.mpl_image_compare(baseline_dir="baseline", remove_text=True)
def test_data():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plot.data(x, y)
    return plt.gcf()


@pytest.mark.mpl_image_compare(baseline_dir="baseline", remove_text=True)
def test_yscale():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plot.data(x, y, yscale="log")
    return plt.gcf()


@pytest.mark.mpl_image_compare(baseline_dir="baseline", remove_text=True)
def test_xscale():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plot.data(x, y, xscale="log")
    return plt.gcf()


@pytest.mark.mpl_image_compare(baseline_dir="baseline", remove_text=True)
def test_grid():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plot.data(x, y, grid=False)
    return plt.gcf()
