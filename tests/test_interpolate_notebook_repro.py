import warnings

import numpy as np

import smpl.data as data
import smpl.interpolate as interp
import smpl.plot as plot


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


def test_cubic_flatmesh_scatter_repro():
    xvalues = np.linspace(-10, 10, 5)
    yvalues = np.linspace(-10, 10, 5)
    xx, yy = data.flatmesh(xvalues, yvalues)
    zz = xx**2 + yy**2 + 10 * xx + 10 * yy

    plot.plot2d(
        xx,
        yy,
        zz,
        fill_missing=False,
        style="scatter",
        logz=False,
        title="interpolate data",
    )

    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        f = interp.interpolate(xx, yy, zz)

    xvalues = np.linspace(-10, 10, 11)
    yvalues = np.linspace(-10, 10, 11)
    xx, yy = data.flatmesh(xvalues, yvalues)

    plot.plot2d(
        xx,
        yy,
        f(xx, yy),
        fill_missing=False,
        style="scatter",
        logz=False,
        title="interpolated data",
    )
