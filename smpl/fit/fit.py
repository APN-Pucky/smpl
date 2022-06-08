import numpy as np
import warnings
from scipy import optimize
from scipy.odr.odrpack import ODR, Model, RealData
import uncertainties as unc
import uncertainties.unumpy as unp
from smpl import debug
from smpl import functions
from smpl import stat
from smpl import util
from smpl import wrap
from smpl import doc
from smpl import data
from numpy.linalg import LinAlgError
from tqdm import tqdm

unv = unp.nominal_values
usd = unp.std_devs

default = {
           'params': [None, "Initial fit parameters", ],
           #'frange': [None, "Limit the fit to given range. First integer is the lowest and second the highest index.", ],
           #'fselector': [None, "Function that takes ``x`` and ``y`` as parameters and returns an array mask in order to limit the data points for fitting. Alternatively a mask for selecting elements from datax and datay.", ],
           'fixed_params': [True, "Enable fixing parameters by choosing the same-named variables from ``kwargs``.", ],
           #'sortbyx': [True, "Enable sorting the x and y data so that x is sorted.", ],
           'maxfev': [10000, "Maximum function evaluations during fitting.", ],
           'epsfcn': [0.0001, "Suitable step length for jacobian approximation.", ],
           'xvar': [None, "Variable in fit function parameters that corresponds to the x axis. If it is None the last of the alphabetical sorted parameters is used.", ],
           #'bins': [0, "Number of bins for histogram", ],
           #'binunc': [stat.poisson_dist, "Number of bins for histogram", ],
           'autotqdm': [True, "Auto fitting display tqdm", ],
           #'xerror': [True, "enable xerrors"],
           #'yerror': [True, "enable yerrors"],
           }

# @doc.insert_str("\tDefault kwargs\n\n\t")

@doc.append_doc(data.data_kwargs)
@doc.append_str("\t")
@doc.append_str(doc.table(default, init=False))
@doc.append_str(doc.table({"fit_kwargs": ["default", "description"]}, bottom=False))
def fit_kwargs(kwargs):
    """Set default fit_kwargs if not set.

    """
    kwargs = data.data_kwargs(kwargs)
    for k, v in default.items():
        if not k in kwargs:
            kwargs[k] = v[0]
    return kwargs


# @append_doc(default_kwargs)
def auto(datax, datay, funcs=None, **kwargs):
    """
    Automatically loop over functions and fit the best one.

    Parameters
    ----------
    funcs : function array
        functions to consider as fit. Default all ``smpl.functions``.
    **kwargs : optional
        see :func:`fit_kwargs`.

    Returns
    -------
    The best fit function and it's parameters and a ``lambda`` where the parameters are already applied to the function.

    """
    kwargs = fit_kwargs(kwargs)
    min_sq = None
    best_f = None
    best_ff = None

    if funcs is None:
        funcs = functions.__dict__.values()
    for f in tqdm(funcs, disable=not kwargs['autotqdm']):
        if callable(f):
            try:
                ff = fit(datax, datay, f, **kwargs)
                fy = f(datax, *ff)
            except (ValueError, LinAlgError) as ve:
                debug.msg(ve)
                continue
            sum_sq = np.sum((fy - datay)**2) + np.sum((fy + usd(fy) -
                                                       datay)**2) + np.sum((fy - usd(fy) - datay)**2)
            if min_sq is None or sum_sq < min_sq:
                min_sq = sum_sq
                best_f = f
                best_ff = ff
    # if not best_f is None:
    #    fit(datax,datay,best_f,**kwargs)
    return best_f, best_ff, lambda x: best_f(x, *best_ff)


def fit(datax, datay, function, **kwargs):
    """
    Returns a fit of ``function`` to ``datax`` and ``datay``.

    Parameters
    ----------
    datax : array_like
        X data either as ``unp.uarray`` or ``np.array`` or ``list``
    datay : array_like
        Y data either as ``unp.uarray`` or ``np.array`` or ``list``
    function : func
        Fit function with parameters: ``x``, ``params``
    **kwargs : optional
        see :func:`fit_kwargs`.

    """
    kwargs = fit_kwargs(kwargs)
    x, y, xerr, yerr = fit_split(datax, datay, **kwargs)
    params = None
    if util.has('params', kwargs):
        params = kwargs['params']

    fixed = {}
    vnames = wrap.get_varnames(function, kwargs['xvar'])
    Ntot = len(vnames)-1
    if util.has("fixed_params", kwargs) and kwargs['fixed_params']:
        for i in range(1, len(vnames)):
            if util.has(vnames[i], kwargs):
                fixed[i] = kwargs[vnames[i]]
    # Count parameters for function
    if params is None:
        N = len(vnames)
        params = [1 for i in range(N-1)]
    tmp_params = []
    for i, pi in enumerate(params):
        if not util.has(i+1, fixed):
            tmp_params += [pi]
    params = tmp_params
    N = len(params)

    def tmp(*x):
        tmp_x = []
        j = 1
        # print(x)
        for i in range(1, Ntot+1):
            # print(i," ",j)
            if not util.has(i, fixed):
                tmp_x += [x[j]]
                # print(x[j])
                j = j+1
            else:
                tmp_x += [fixed[i]]

        # print(Ntot)
        # print(tmp_x)
        return unv(wrap.get_lambda(function, kwargs['xvar'])(x[0], *tmp_x))
    if xerr is not None:
        fit = _fit_odr(x, y, tmp, params=params, xerr=xerr, yerr=yerr)
    else:
        fit = _fit_curvefit(x, y, tmp, params=params, yerr=yerr)

    rfit = []
    j = 0
    for i in range(1, Ntot+1):
        if not util.has(i, fixed):
            rfit += [fit[j]]
            j = j+1
        else:
            rfit += [fixed[i]]

    return rfit


# fittet ein dataset mit gegebenen x und y werten, eine funktion und ggf. anfangswerten und y-Fehler
# gibt die passenden parameter der funktion, sowie dessen unsicherheiten zurueck
#
# https://stackoverflow.com/questionsquestions/14581358/getting-standard-errors-on-fitted-parameters-using-the-optimize-leastsq-method-i#
# Updated on 4/6/2016
# User: https://stackoverflow.com/users/1476240/pedro-m-duarte
def _fit_curvefit(datax, datay, function, params=None, yerr=None, **kwargs):
    try:
        pfit, pcov = \
            optimize.curve_fit(function, datax, datay, p0=params,
                               sigma=yerr, epsfcn=util.get("epsfcn", kwargs, 0.0001), **kwargs, maxfev=util.get("maxfev", kwargs, 10000))
    except RuntimeError as e:
        debug.msg(str(e))
        return params
    error = []
    for i in range(len(pfit)):
        try:
            error.append(np.absolute(pcov[i][i])**0.5)
        except Exception as e:
            warnings.warn(str(e))
            error.append(0.00)
    return unc.correlated_values(pfit, pcov)


def _fit_odr(datax, datay, function, params=None, yerr=None, xerr=None):
    model = Model(lambda p, x: function(x, *p))
    realdata = RealData(datax, datay, sy=yerr, sx=xerr)
    odr = ODR(realdata, model, beta0=params)
    out = odr.run()
    # This was the old wrong way! Now use correct co. matrix through unc-package!
    # Note Issues on scipy odr and curve_fit, regarding different definitions/namings of standard deviation or error and covaraince matrix
    # https://github.com/scipy/scipy/issues/6842
    # https://github.com/scipy/scipy/pull/12207
    # https://stackoverflow.com/questions/62460399/comparison-of-curve-fit-and-scipy-odr-absolute-sigma
    return unc.correlated_values(out.beta, out.cov_beta)


def data_split(datax, datay, **kwargs):
    """
    Split data + errors
    """
    return data.__data_split(datax,datay,**kwargs)

def fit_split(datax, datay, **kwargs):
    """
    Splits datax and datay into (x,y,xerr,yerr).

    Parameters
    ----------
    **kwargs : optional
        see :func:`fit_kwargs`.
    """
    kwargs = fit_kwargs(kwargs)
    return data.filtered_data_split(datax,datay,**kwargs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
