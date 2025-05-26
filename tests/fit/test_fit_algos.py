import matplotlib.pyplot as plt
import numpy as np
import pytest
import uncertainties.unumpy as unp

from smpl import fit
from smpl import functions as f
from smpl.fit import Fitter


def _test_fit_linear(fitter, datax, datay):
    fit.fit(
        datax,
        datay,
        fmt=".",
        function=f.linear,
        units=["l", "b"],
        sigmas=1,
        lpos=2,
        residue=True,
        residue_err=False,
        xaxis="t",
        yaxis="s",
        show=False,
        fitter=fitter,
    )
    plt.close()


def _test_fit_exponential(fitter, datax, datay):
    fit.fit(
        datax,
        datay,
        fmt=".",
        function=f.exp,
        units=["l", "b"],
        sigmas=1,
        lpos=2,
        residue=True,
        residue_err=False,
        xaxis="t",
        yaxis="s",
        b=0,
        show=False,
        fitter=fitter,
    )
    plt.close()


def _test_fit(fitter):
    data = np.loadtxt("tests/test_linear.txt")
    datax, datay = data[:, 0], data[:, 1]
    _test_fit_linear(fitter, datax, datay)
    _test_fit_exponential(fitter, datax, datay)

    datax, datay = unp.uarray(data[:, 0], data[:, 2]), data[:, 1]
    _test_fit_linear(fitter, datax, datay)
    _test_fit_exponential(fitter, datax, datay)

    datax, datay = data[:, 0], unp.uarray(data[:, 1], data[:, 3])
    _test_fit_linear(fitter, datax, datay)
    _test_fit_exponential(fitter, datax, datay)

    datax, datay = (
        unp.uarray(data[:, 0], data[:, 2]),
        unp.uarray(data[:, 1], data[:, 3]),
    )
    _test_fit_linear(fitter, datax, datay)
    _test_fit_exponential(fitter, datax, datay)


def _test_fit_algos():
    _test_fit(Fitter.MINUIT_LEASTSQUARES)
    _test_fit(Fitter.SCIPY_CURVEFIT)
    _test_fit(Fitter.SCIPY_ODR)


@pytest.mark.line_profile.with_args(
    fit.fit,
    fit._fit_minuit_leastsquares,
    fit._fit_curvefit,
    fit._fit_odr,
    _test_fit,
    _test_fit_algos,
)
def test_fit_algos():
    _test_fit_algos()
