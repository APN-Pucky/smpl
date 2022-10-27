import numpy as np
import uncertainties as unc
import uncertainties.unumpy as unp
from smpl import doc
import scipy
from scipy.fft import fft as sfft,fftfreq,fftshift
import math
import statistics as stat
import pandas as pd
from math import log10, floor
from scipy.misc import derivative

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
        chisq = np.sum((r/sigmas)**2)
    else:
        chisq = np.sum((r)**2)

    return chisq

chi2 = Chi2

def average_deviation(y,f):
    r= np.abs((y-f)/f)
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

def trim_domain(f,    
    fmin = np.finfo(np.float32).min/2,
    fmax = np.finfo(np.float32).max/2,
    steps=10000,
    min_ch=0.0001,
    recursion_limit=100
               ):
    """
    Get the domain of the function ``f`` with the ranges removed where the derivative of ``f`` is below ``min_ch``.
    """
    recursion_limit = recursion_limit - 1
    if recursion_limit < 0:
        return fmin,fmax
    test = np.linspace(fmin,fmax,steps)
    try:
        dr = derivative(f,test,dx=1e-06)
    except: 
        return 0.,0.
    m1 = np.abs(dr)>min_ch
    bmin=np.argmax(m1)
    m2=(np.abs(dr)>min_ch)[::-1]
    tbmax=np.argmax(m2)
    xmin = test[bmin]
    xmax=test[::-1][tbmax]
    if bmin == 0 and tbmax ==0 and not m1[0] and not m2[0]:
        # trisect the full domain
        tmin = xmin
        tmax = xmax
        t1a,t1b = trim_domain(f,tmin+ (tmax-tmin)/3,tmax -(tmax-tmin)/3,min_ch=min_ch,recursion_limit=recursion_limit)
        if np.isclose(t1a,t1b):
            t2a,t2b = trim_domain(f,tmin + (tmax-tmin)/3,tmax,min_ch=min_ch,recursion_limit=recursion_limit)
            if np.isclose(t2a,t2b):
                t3a,t3b = trim_domain(f,tmin ,tmax- (tmax-tmin)/3,min_ch=min_ch,recursion_limit=recursion_limit)
                if np.isclose(t3a,t3b):
                    return 0.,0. 
                else:
                    return t3a,t3b    
            else:
                return t2a,t2b
        else:
            return t1a,t1b
    return xmin,xmax

def get_domain(f,
    fmin = np.finfo(np.float32).min/2,
    fmax = np.finfo(np.float32).max/2,
    steps=1000,
):
    """
    Return the statistically probed domain of the function ``f``.
    """
    if np.isclose(fmin,fmax,rtol=0.0001,atol=0.00001):
        return 0.,0.
    
    test = np.linspace(fmin,fmax,steps)
    
    r = unv(f(test))
    mask = np.isfinite(r)        
    tr = test[mask]
    if len(tr)>0:
        tmin = np.amin(tr)
        tmax = np.amax(tr)
        test_r = np.linspace(tmin,tmax,steps)
        if np.equal(tr.shape , test_r.shape) and np.allclose(test_r,tr):
            return tmin,tmax
    
    # trisect
    tmin = fmin
    tmax = fmax
    t1a,t1b = get_domain(f,tmin+ (tmax-tmin)/3,tmax -(tmax-tmin)/3)
    if np.isclose(t1a,t1b):
        t2a,t2b = get_domain(f,tmin + (tmax-tmin)/3,tmax)
        if np.isclose(t2a,t2b):
            t3a,t3b = get_domain(f,tmin ,tmax- (tmax-tmin)/3)
            if np.isclose(t3a,t3b):
                return 0.,0. 
            else:
                return t3a,t3b    
        else:
            return t2a,t2b
    else:
        return t1a,t1b

def is_monotone(f,tmin=None,tmax=None,steps=1000):
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
        tmin,tmax = get_domain(f)
    test = np.linspace(tmin,tmax,steps)
    return np.all(f(test[1:])>=f(test[:-1]))

def get_interesting_domain(f,min_ch = 1e-6):
    """
    Return interesting xmin and xmax of function ``f``.

    Examples
    --------
    >>> def f(x):
    ...     return np.sin(x)
    >>> get_interesting_domain(f)
    (-3.141625000000003, 3.141625000000003)
    """
    omin_x,omax_x = get_domain(f)
    if is_monotone(f,omin_x,omax_x):
        min_x,max_x=trim_domain(f,omin_x,omax_x,min_ch = min_ch)
        #min_x,max_x=omin_x,omax_x
    else:
        tmax_x= scipy.optimize.minimize(lambda x: -f(x),0.,method='Nelder-Mead',bounds=[(omin_x,omax_x)])
        tmin_x= scipy.optimize.minimize(f,0.,method='Nelder-Mead',bounds=[(omin_x,omax_x)])
        if tmax_x.success:
            tmax_x = tmax_x.x[0]
        else:
            tmax_x =0.
        if tmin_x.success:
            tmin_x = tmin_x.x[0]
        else:
            tmin_x =0.
        
        if abs(tmax_x) > np.finfo(np.float32).max/10:
            tmax_x = 0.
        if abs(tmin_x) > np.finfo(np.float32).max/10:
            tmin_x = 0.
        x_min = min(tmax_x,tmin_x)
        x_max = max(tmax_x,tmin_x)
        min_x = ((x_max+x_min)/2-(x_max-x_min))
        max_x = ((x_max+x_min)/2+(x_max-x_min))
        if np.isclose(min_x,max_x):
            min_x,max_x=trim_domain(f,omin_x,omax_x,min_ch = min_ch)
            
            
    return min_x,max_x