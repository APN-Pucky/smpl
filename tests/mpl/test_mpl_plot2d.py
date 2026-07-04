import sys

import matplotlib.pyplot as plt
import numpy as np
import pytest

from smpl import plot

if sys.version_info >= (3, 11):
    pytest.skip("Python 3.11+ fails", allow_module_level=True)


@pytest.mark.mpl_image_compare(baseline_dir="baseline", remove_text=True)
def test_style_scatter():
    x = np.linspace(0, 10, 10)
    y = np.sin(x)
    z = np.abs(np.cos(x))
    plot.plot2d(x, y, z, style="scatter")
    return plt.gcf()


@pytest.mark.mpl_image_compare(baseline_dir="baseline", remove_text=True)
def test_style_pcolormesh():
    x = np.linspace(0, 10, 10)
    y = np.sin(x)
    z = np.abs(np.cos(x))
    plot.plot2d(x, y, z, style="pcolormesh")
    return plt.gcf()


@pytest.mark.mpl_image_compare(baseline_dir="baseline", remove_text=True)
def test_style_image():
    x = np.linspace(0, 10, 10)
    y = np.sin(x)
    z = np.abs(np.cos(x))
    plot.plot2d(x, y, z, style="image")
    return plt.gcf()
