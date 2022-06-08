import numpy as np
import uncertainties as unc
import uncertainties.unumpy as unp
from smpl import doc
import scipy
import math
import statistics as stat
import pandas as pd


unv = unp.nominal_values
usd = unp.std_devs


def unv_lambda(f):
    """Returns a function which applies :func:`unv` on the result of ``f``."""
    return lambda *a: unv(f(*a))


def poisson_dist(N):
    """Return ``N`` with added poissonian uncertainties."""
    return unp.uarray(N, np.sqrt(N))


def no_dist(N):
    """Return ``N`` with no uncertainties."""
    return unp.uarray(N, 0)


def normalize(ydata):
    """Return normalized ``ydata``."""
    return (ydata-np.amin(ydata))/(np.amax(ydata)-np.amin(ydata))


def novar_mean(n):
    """Return mean of ``n`` with only the uncertainties of ``n`` and no variance."""
    return np.sum(n)/len(n)


def mean(n):
    """Return mean of ``n`` with combined error of variance and unvertainties of ``n``."""
    # find the mean value and add uncertainties
    if isinstance(n, pd.core.series.Series):
        n = n.to_numpy()
    k = np.mean(n)
    err = stat.variance(unv(n))
    return unc.ufloat(unv(k), math.sqrt(usd(k)**2 + err))


def noisy(x, mean=0, std=1):
    """Add gaussian noise to ``x``."""
    return x+np.random.normal(mean, std, len(x))


@doc.insert_eq()
def fft(y):
    """
    $F(y)$
    """
    N = len(y)
    fft = scipy.fftpack.fft(y)
    return 2 * abs(fft[:N//2]) / N
