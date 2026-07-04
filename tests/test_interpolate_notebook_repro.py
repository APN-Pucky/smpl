import warnings

import numpy as np

import smpl.interpolate as interp


def test_bivariatespline_notebook_repro():
    xvalues = np.linspace(-10, 10, 10)
    yvalues = xvalues * 2
    xx = xvalues
    yy = yvalues
    xx = np.append(xx, xx)
    yy = np.append(yy, -yy)
    zz = xx**2 + yy**2

    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        interp.interpolate(xx, yy, zz, interpolator="bivariatespline")
