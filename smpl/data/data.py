from smpl import doc
from smpl import util
from smpl import stat
import uncertainties.unumpy as unp
import numpy as np

default = {
           'frange': [None, "Limit the fit to given range. First integer is the lowest and second the highest index.", ],
           'fselector': [None, "Function that takes ``x`` and ``y`` as parameters and returns an array mask in order to limit the data points for fitting. Alternatively a mask for selecting elements from datax and datay.", ],
           'sortbyx': [True, "Enable sorting the x and y data so that x is sorted.", ],
           'bins': [0, "Number of bins for histogram", ],
           'binunc': [stat.poisson_dist, "Number of bins for histogram", ],
           'xerror': [True, "enable xerrors"],
           'yerror': [True, "enable yerrors"],
           }


unv = unp.nominal_values
usd = unp.std_devs

# @doc.insert_str("\tDefault kwargs\n\n\t")
@doc.append_str(doc.table(default, init=False))
@doc.append_str(doc.table({"data_kwargs": ["default", "description"]}, bottom=False))
def data_kwargs(kwargs):
    """Set default data_kwargs if not set.

    """
    for k, v in default.items():
        if not k in kwargs:
            kwargs[k] = v[0]
    return kwargs


def __data_split(datax, datay, **kwargs):
    """
    Splits datax and datay into (x,y,xerr,yerr).
    Does not apply filters `frange` and `fselector`.

    Parameters
    ----------
    **kwargs : optional
        see :func:`data_kwargs`.
    """
    if kwargs['bins'] > 0:
        N, bins = np.histogram(unv(datax), bins=kwargs['bins'])
        y = kwargs['binunc'](N)
        yerr = usd(y)
        yerr = yerr if np.any(np.abs(yerr) > 0) else None
        return bins[0:-1] - (bins[0]-bins[1])/2, unv(y), None, yerr
    if util.has("sortbyx", kwargs) and kwargs['sortbyx']:
        ind = np.argsort(unv(datax))
    else:
        ind = np.array(range(len(datax)))
    x = unv(datax)[ind]
    y = unv(datay)[ind]
    xerr = usd(datax)[ind]
    yerr = usd(datay)[ind]
    xerr = xerr if np.any(np.abs(xerr) > 0) else None
    yerr = yerr if np.any(np.abs(yerr) > 0) else None
    if util.has("xerror", kwargs) and not kwargs['xerror']:
        xerr = None
    if util.has("yerror", kwargs) and not kwargs['yerror']:
        yerr = None
    return x, y, xerr, yerr


def _data_split(datax, datay, **kwargs):
    """
    Applies `fselector` and calls :func:`data_split`
    """
    if util.has('fselector', kwargs):
        sel = kwargs['fselector']
        if callable(sel):
            return __data_split(datax[sel(datax, datay)], datay[sel(datax, datay)], **kwargs)
        else:
            return __data_split(datax[sel], datay[sel], **kwargs)
    return __data_split(datax, datay, **kwargs)


def filtered_data_split(datax, datay, **kwargs):
    """
    Splits datax and datay into (x,y,xerr,yerr).
    Applies filters `fselector` and `frange`.

    Returns
    -------
    (x,y,xerr,yerr) : tuple
        four arrays with specified values.

    Parameters
    ----------
    **kwargs : optional
        see :func:`data_kwargs`.
    """
    kwargs = data_kwargs(kwargs)
    x, y, xerr, yerr = _data_split(datax, datay, **kwargs)
    if util.has('frange', kwargs):
        x = x[kwargs['frange'][0]:kwargs['frange'][1]]
        y = y[kwargs['frange'][0]:kwargs['frange'][1]]
        if not yerr is None:
            yerr = yerr[kwargs['frange'][0]:kwargs['frange'][1]]
        if not xerr is None:
            xerr = xerr[kwargs['frange'][0]:kwargs['frange'][1]]

    return x, y, xerr, yerr