import numpy as np
import uncertainties as unc
import uncertainties.unumpy as unp
from smpl import doc
from scipy.fft import fft as sfft,fftfreq,fftshift
import math
import statistics as stat
import pandas as pd
from math import log10, floor


unv = unp.nominal_values
usd = unp.std_devs

def round_sig(x, sig=2):
    """
    Round to ``sig`` significant digits.

    Parameters
    ----------
    x : float
        Value to round.
    sig : int
        Number of significant digits.

    Returns
    -------
    float
        Rounded value.

    Examples
    --------
    >>> round_sig(1.23456789, sig=2)
    1.2
    >>> round_sig(1.23456789, sig=4)
    1.235
    """
    return round(x, sig-int(floor(log10(abs(x))))-1)


def R2(y, f):
    """
    R2 - Coefficient of determination

    In the best case, the modeled values exactly match the observed values, which results in R2 = 1.
    A baseline model, which always predicts the mean of y, will have R2 = 0.
    Models that have worse predictions than this baseline will have a negative R2.

    References
    ----------

    https://en.wikipedia.org/wiki/Coefficient_of_determination


    """
    r = y - f
    mean = np.sum(r)/len(r)
    SSres = np.sum((r)**2)
    SStot = np.sum((r-mean)**2)
    Rsq = 1 - SSres/SStot
    return Rsq


def Chi2(y, f, sigmas=None):
    """
    Chi2 - Goodness of Fit

    In general, if Chi-squared/Nd is of order 1.0, then the fit is reasonably good.
    Coversely,  if Chi-squared/Nd >> 1.0, then the fit is a poor one.

    References
    ----------

    https://www.phys.hawaii.edu/~varner/PHYS305-Spr12/DataFitting.html

    """
    r = y - f
    if sigmas is not None:
        chisq = np.sum((r/sigmas)**2)
    else:
        chisq = np.sum((r)**2)

    return chisq


def unv_lambda(f):
    """Returns a function which applies :func:`unv` on the result of ``f``."""
    return lambda *a: unv(f(*a))


def poisson_dist(N):
    """
    Return ``N`` with added poissonian uncertainties.

    Parameters
    ----------
    N : float or array_like of floats
        Number of events.

    Returns
    -------
    uncertainties.unumpy.uarray
        Number of events with uncertainties.

    Examples
    --------
    >>> poisson_dist(100)
    array(100.0+/-10.0, dtype=object)
    """
    return unp.uarray(N, np.sqrt(N))


def no_dist(N):
    """Return ``N`` with no uncertainties."""
    return unp.uarray(N, 0)


def normalize(ydata):
    """
    Return normalized ``ydata``.

    Parameters
    ----------
    ydata : array_like
        Data to be normalized.

    Returns
    -------
    array_like
        Normalized data.

    Examples
    --------
    >>> ydata = np.array([1, 2, 3, 4, 5])
    >>> normalize(ydata)
    array([0.  , 0.25, 0.5 , 0.75, 1.  ])
    """
    return (ydata-np.amin(ydata))/(np.amax(ydata)-np.amin(ydata))


def novar_mean(n):
    """Return mean of ``n`` with only the uncertainties of ``n`` and no variance."""
    return np.sum(n)/len(n)


def mean(n):
    """
    Return mean of ``n`` with combined error of variance and unvertainties of ``n``.

    Parameters
    ----------
    n : array_like
        Data to be averaged.

    Returns
    -------
    uncertainties.unumpy.uarray
        Mean of ``n``.

    Examples
    --------    
    >>> n = np.array([1, 2, 3, 4, 5])
    >>> mean(n)
    3.0+/-1.5811388300841898
    """
    # find the mean value and add uncertainties
    if isinstance(n, pd.core.series.Series):
        n = n.to_numpy()
    k = np.mean(n)
    err = stat.variance(unv(n))
    return unc.ufloat(unv(k), math.sqrt(usd(k)**2 + err))


def noisy(x, mean=1, std=0.1):
    """
    Add gaussian noise to ``x``.
    
    Parameters
    ----------
    x : array_like
        Data to be smeared.
    mean : float
        Mean of gaussian noise.
    std : float
        Standard deviation of gaussian noise.

    Returns
    -------
    array_like
        Smeared data.

    Examples
    --------
    >>> x = np.array([1, 2, 3, 4, 5])
    >>> noisy(x,std=0)
    array([1., 2., 3., 4., 5.])
    """
    return x*np.random.normal(mean, std, len(x))


def normal(x, mean=0, std=1):
    return np.random.normal(mean, std, len(x))


@doc.insert_eq()
def fft(y):
    """
    Compute the FFT of ``y``.

    Parameters
    ----------
    y : array_like  
        Data to be transformed.

    Returns
    -------
    array_like

    """
    t=y
    sp = fftshift(sfft(np.sin(t)))
    freq =fftshift(fftfreq(t.shape[-1]))
    return freq,sp
