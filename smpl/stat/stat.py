import numpy as np
import uncertainties as unc
import uncertainties.unumpy as unp

unv=unp.nominal_values
usd=unp.std_devs
def unv_lambda(f):
    """
    Returns a function which applies :func:`unv` on the result of ``f``
    """
    return lambda *a : unv(f(*a))

# mathe Funktionen
def poisson_dist(N):
    """
    Return ``N`` with added poissonian uncertainties.
    """
    return unp.uarray(N,np.sqrt(N))

def normalize(ydata):
    """
    Return normalized ``ydata`` .
    """
    return (ydata-np.amin(ydata))/(np.amax(ydata)-np.amin(ydata))
def novar_mean(f):
    """
    Return mean of ``n`` with only the uncertainties of ``n`` and no variance.
    """
    return np.sum(f)/len(f)
def mean(n):
    """
    Return mean of ``n`` with combined error of variance and unvertainties of ``n``.
    """
    # find the mean value and add uncertainties
    k = np.mean(n)
    err = stat.variance(unv(n))
    return unc.ufloat(unv(k), math.sqrt(usd(k)**2 + err))

