"""Simplified statistics."""

import math
import statistics as stat
from math import floor, log10

import numpy as np
import pandas as pd
import scipy
import uncertainties as unc
import uncertainties.unumpy as unp
from numpy import arange, array, hstack, newaxis, prod
from scipy import linalg
from scipy.fft import fft as sfft
from scipy.fft import fftfreq, fftshift

from smpl import doc

unv = unp.nominal_values
usd = unp.std_devs


# Copied from scipy.stats._finite_differences
def central_diff_weights(Np, ndiv=1):
    """
    Return weights for an Np-point central derivative.

    Assumes equally-spaced function points.

    If weights are in the vector w, then
    derivative is w[0] * f(x-ho*dx) + ... + w[-1] * f(x+h0*dx)

    Parameters
    ----------
    Np : int
        Number of points for the central derivative.
    ndiv : int, optional
        Number of divisions. Default is 1.

    Returns
    -------
    w : ndarray
        Weights for an Np-point central derivative. Its size is `Np`.

    Notes
    -----
    Can be inaccurate for a large number of points.

    Examples
    --------
    We can calculate a derivative value of a function.

    >>> def f(x):
    ...     return 2 * x**2 + 3
    >>> x = 3.0 # derivative point
    >>> h = 0.1 # differential step
    >>> Np = 3 # point number for central derivative
    >>> weights = central_diff_weights(Np) # weights for first derivative
    >>> vals = [f(x + (i - Np/2) * h) for i in range(Np)]
    >>> float(sum(w * v for (w, v) in zip(weights, vals))/h)
    11.79999999999998

    This value is close to the analytical solution:
    f'(x) = 4x, so f'(3) = 12

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Finite_difference

    """
    if Np < ndiv + 1:
        raise ValueError("Number of points must be at least the derivative order + 1.")
    if Np % 2 == 0:
        raise ValueError("The number of points must be odd.")

    ho = Np >> 1
    x = arange(-ho, ho + 1.0)
    x = x[:, newaxis]
    X = x**0.0
    for k in range(1, Np):
        X = hstack([X, x**k])
    w = prod(arange(1, ndiv + 1), axis=0) * linalg.inv(X)[ndiv]
    return w


# Copied from scipy.stats._finite_differences
def derivative(func, x0, dx=1.0, n=1, args=(), order=3):
    """
    Find the nth derivative of a function at a point.

    Given a function, use a central difference formula with spacing `dx` to
    compute the nth derivative at `x0`.

    Parameters
    ----------
    func : function
        Input function.
    x0 : float
        The point at which the nth derivative is found.
    dx : float, optional
        Spacing.
    n : int, optional
        Order of the derivative. Default is 1.
    args : tuple, optional
        Arguments
    order : int, optional
        Number of points to use, must be odd.

    Notes
    -----
    Decreasing the step size too small can result in round-off error.

    Examples
    --------
    >>> def f(x):
    ...     return x**3 + x**2
    >>> float(derivative(f, 1.0, dx=1e-6))
    4.9999999999...

    """
    if order < n + 1:
        raise ValueError(
            "'order' (the number of points used to compute the derivative), "
            "must be at least the derivative order 'n' + 1."
        )
    if order % 2 == 0:
        raise ValueError(
            "'order' (the number of points used to compute the derivative) must be odd."
        )
    # pre-computed for n=1 and 2 and low-order for speed.
    if n == 1:
        if order == 3:
            weights = array([-1, 0, 1]) / 2.0
        elif order == 5:
            weights = array([1, -8, 0, 8, -1]) / 12.0
        elif order == 7:
            weights = array([-1, 9, -45, 0, 45, -9, 1]) / 60.0
        elif order == 9:
            weights = array([3, -32, 168, -672, 0, 672, -168, 32, -3]) / 840.0
        else:
            weights = central_diff_weights(order, 1)
    elif n == 2:
        if order == 3:
            weights = array([1, -2.0, 1])
        elif order == 5:
            weights = array([-1, 16, -30, 16, -1]) / 12.0
        elif order == 7:
            weights = array([2, -27, 270, -490, 270, -27, 2]) / 180.0
        elif order == 9:
            weights = (
                array([-9, 128, -1008, 8064, -14350, 8064, -1008, 128, -9]) / 5040.0
            )
        else:
            weights = central_diff_weights(order, 2)
    else:
        weights = central_diff_weights(order, n)
    val = 0.0
    ho = order >> 1
    for k in range(order):
        val += weights[k] * func(x0 + (k - ho) * dx, *args)
    return val / prod((dx,) * n, axis=0)


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
    return round(x, sig - int(floor(log10(abs(x)))) - 1)


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
    mean = np.sum(r) / len(r)
    SSres = np.sum((r) ** 2)
    SStot = np.sum((r - mean) ** 2)
    Rsq = 1 - SSres / SStot
    return Rsq


r2 = R2


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
        chisq = np.sum((r / sigmas) ** 2)
    else:
        chisq = np.sum((r) ** 2)

    return chisq


chi2 = Chi2


def average_deviation(y, f):
    r = np.abs((y - f) / f)
    return mean(r)


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
    return (ydata - np.amin(ydata)) / (np.amax(ydata) - np.amin(ydata))


def novar_mean(n):
    """Return mean of ``n`` with only the uncertainties of ``n`` and no variance."""
    return np.sum(n) / len(n)


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
    return unc.ufloat(unv(k), math.sqrt(usd(k) ** 2 + err))


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
    return x * np.random.normal(mean, std, len(x))


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
    t = y
    sp = fftshift(sfft(np.sin(t)))
    freq = fftshift(fftfreq(t.shape[-1]))
    return freq, sp


def trim_domain(
    f,
    fmin=np.finfo(np.float32).min / 2,
    fmax=np.finfo(np.float32).max / 2,
    steps=10000,
    min_ch=0.0001,
    recursion_limit=10,
):
    """
    Get the domain of the function ``f`` with the ranges removed where the derivative of ``f`` is below ``min_ch``.
    """
    recursion_limit = recursion_limit - 1
    if recursion_limit < 0:
        return fmin, fmax
    test = np.linspace(fmin, fmax, steps)
    try:
        dr = derivative(f, test, dx=1e-06)
    except Exception:
        return 0.0, 0.0
    m1 = np.abs(dr) > min_ch
    bmin = np.argmax(m1)
    m2 = (np.abs(dr) > min_ch)[::-1]
    tbmax = np.argmax(m2)
    xmin = test[bmin]
    xmax = test[::-1][tbmax]
    if bmin == 0 and tbmax == 0 and not m1[0] and not m2[0]:
        # trisect the full domain
        tmin = xmin
        tmax = xmax
        t1a, t1b = trim_domain(
            f,
            tmin + (tmax - tmin) / 3,
            tmax - (tmax - tmin) / 3,
            min_ch=min_ch,
            recursion_limit=recursion_limit,
        )
        if np.isclose(t1a, t1b):
            t2a, t2b = trim_domain(
                f,
                tmin + (tmax - tmin) / 3,
                tmax,
                min_ch=min_ch,
                recursion_limit=recursion_limit,
            )
            if np.isclose(t2a, t2b):
                t3a, t3b = trim_domain(
                    f,
                    tmin,
                    tmax - (tmax - tmin) / 3,
                    min_ch=min_ch,
                    recursion_limit=recursion_limit,
                )
                if np.isclose(t3a, t3b):
                    return 0.0, 0.0
                return t3a, t3b
            return t2a, t2b
        return t1a, t1b
    return xmin, xmax


def get_domain(
    f,
    fmin=np.finfo(np.float32).min / 2,
    fmax=np.finfo(np.float32).max / 2,
    steps=1000,
):
    """
    Return the statistically probed domain of the function ``f``.
    """
    if np.isclose(fmin, fmax, rtol=0.0001, atol=0.00001):
        return 0.0, 0.0

    test = np.linspace(fmin, fmax, steps)

    r = unv(f(test))
    mask = np.isfinite(r)
    tr = test[mask]
    if len(tr) > 0:
        tmin = np.amin(tr)
        tmax = np.amax(tr)
        test_r = np.linspace(tmin, tmax, steps)
        if np.equal(tr.shape, test_r.shape) and np.allclose(test_r, tr):
            return tmin, tmax

    # trisect
    tmin = fmin
    tmax = fmax
    t1a, t1b = get_domain(f, tmin + (tmax - tmin) / 3, tmax - (tmax - tmin) / 3)
    if np.isclose(t1a, t1b):
        t2a, t2b = get_domain(f, tmin + (tmax - tmin) / 3, tmax)
        if np.isclose(t2a, t2b):
            t3a, t3b = get_domain(f, tmin, tmax - (tmax - tmin) / 3)
            if np.isclose(t3a, t3b):
                return 0.0, 0.0
            return t3a, t3b
        return t2a, t2b
    return t1a, t1b


def is_monotone(f, tmin=None, tmax=None, steps=1000):
    """
    Test if function ``f`` is monotone.

    Parameters
    ----------
    f : function
        Function to be tested.
    test : array_like
        Test points.

    Returns
    -------
    bool
        True if function is monotone.

    Examples
    --------
    >>> def f(x):
    ...     return x**2
    >>> is_monotone(f)
    False
    >>> is_monotone(np.exp)
    True
    """
    if tmax is None and tmin is None:
        tmin, tmax = get_domain(f)
    test = np.linspace(tmin, tmax, steps)
    return bool(np.all(f(test[1:]) >= f(test[:-1])))


def get_interesting_domain(f, min_ch=1e-6, maxiter=100):
    """
    Return interesting xmin and xmax of function ``f``.

    Examples
    --------
    >>> def f(x):
    ...     return np.sin(x)
    >>> get_interesting_domain(f)
    (-3.141625000000003, 3.141625000000003)
    """
    omin_x, omax_x = get_domain(f)
    if is_monotone(f, omin_x, omax_x):
        min_x, max_x = trim_domain(f, omin_x, omax_x, min_ch=min_ch)
        # min_x,max_x=omin_x,omax_x
    else:
        tmax_x = scipy.optimize.minimize(
            lambda x: -f(x),
            0.0,
            method="Nelder-Mead",
            bounds=[(omin_x, omax_x)],
            options={"maxiter": maxiter},
        )
        tmin_x = scipy.optimize.minimize(
            f,
            0.0,
            method="Nelder-Mead",
            bounds=[(omin_x, omax_x)],
            options={"maxiter": maxiter},
        )
        if tmax_x.success:
            tmax_x = tmax_x.x[0]
        else:
            tmax_x = 0.0
        if tmin_x.success:
            tmin_x = tmin_x.x[0]
        else:
            tmin_x = 0.0

        if abs(tmax_x) > np.finfo(np.float32).max / 10:
            tmax_x = 0.0
        if abs(tmin_x) > np.finfo(np.float32).max / 10:
            tmin_x = 0.0
        x_min = min(tmax_x, tmin_x)
        x_max = max(tmax_x, tmin_x)
        min_x = (x_max + x_min) / 2 - (x_max - x_min)
        max_x = (x_max + x_min) / 2 + (x_max - x_min)
        if np.isclose(min_x, max_x):
            min_x, max_x = trim_domain(f, omin_x, omax_x, min_ch=min_ch)

    return float(min_x), float(max_x)
