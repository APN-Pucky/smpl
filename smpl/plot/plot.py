import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import uncertainties
import uncertainties.unumpy as unp
import sympy
import matplotlib.pylab as pylab
# local imports
from smpl import io
from smpl import util
from smpl import wrap
from smpl import doc
from smpl import fit as ffit


def set_plot_style():
    # fig_size = (8, 6)
    # fig_legendsize = 14
    # fig_labelsize = 12 # ‘xx-small’, ‘x-small’, ‘small’, ‘medium’, ‘large’, ‘x-large’, ‘xx-large’.
    params = {'legend.fontsize': 'x-large',
              'figure.figsize': (8, 6),
              'axes.labelsize': 'x-large',
              'axes.titlesize': 'x-large',
              'xtick.labelsize': 'x-large',
              'ytick.labelsize': 'x-large'}
    pylab.rcParams.update(params)
    matplotlib.rcParams.update(params)
    # matplotlib.rcParams.update({'font.size': fig_labelsize})
    # colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)


unv = unp.nominal_values
usd = unp.std_devs

default = {
    #    'params'        :[None      ,"Initial fit parameters",
    'xlabel': ["", "X axis label", ],
    'ylabel': ["", "Y axis label", ],
    'label': [None, "Legend name of plotted ``data``", ],
    'fmt': ['.', "Format for plotting fit function", ],
    'units': [None, "Units of the fit parameters as strings. Displayed in the Legend", ],
    'save': [None, " File to save the plot", ],
    'lpos': [0, "Legend position", ],
    'tight': [True, "tight_layout", ],
    #          'frange'        :[None      ,"Limit the fit to given range. First integer is the lowest and second the highest index.",],
    'prange': [None, "Limit the plot of the fit to given range", ],
    'sigmas': [0, "Color the array of given ``sigma`` times uncertainty. Only works if the fit function is coded with ``unp``", ],
    'data_sigmas': [1, "Color the array of given ``sigma`` times uncertainty. Only works if the data has uncertainties", ],
    'init': [False, "Initialize a new plot"],
    'ss': [True, "save, add legends and grid to the plot", ],
    'also_data': [True, " also plot the data"],
    'also_fit': [True, "also plot the fit", ],
    'logy': [False, "logarithmic x axis", ],
    'logx': [False, "logarithmic y axis", ],
    'data_color': [None, "Color of the data plot", ],
    'fit_color': [None, "Color of the fit plot", ],
    'residue': [False, "Display difference between fit and data in a second plot", ],
    'residue_err': [True, "Differences between fit and data will have errorbars", ],
    'show': [False, "Call plt.show()", ],
    'size': [None, "Size of the plot as a tuple (x,y). Only has an effect if ``init`` is True", ],
    'number_format': [io.gf(4), "Format to display numbers.", ],
    # ,          'selector'      :[ None     ,"Function that takes ``x`` and ``y`` as parameters and returns an array mask in order to limit the data points for fitting. Alternatively a mask for selecting elements from datax and datay.",],
    # ,          'fixed_params'  :[ True     ,"Enable fixing parameters by choosing the same-named variables from ``kwargs``.",],
    # ,          'sortbyx'       :[ True     , "Enable sorting the x and y data so that x is sorted.",],
    'interpolate': [True, "Enable interpolation of whole data if fit range is limited by ``frange`` or ``fselector``.", ],
    'interpolate_min': [None, "Lower interpolation bound", ],
    'interpolate_max': [None, "Higher interpolation bound", ],
    'interpolate_hatch': [r"||", "Interpolation shape/hatch for filled area in case of ``sigmas``>0. See https://matplotlib.org/stable/gallery/shapes_and_collections/hatch_style_reference.html", ],
    'bbox_to_anchor': [None, "Position in a tuple (x,y),Shift position of the legend out of the main pane. ", ],
    'ncol': [None, "Columns in the legend if used with ``bbox_to_anchor``.", ],
    'steps': [1000, "resolution of the plotted function", ],
    'fitinline': [False,  "No newlines for each fit parameter", ],
    'grid': [True,  "Enable grid for the plot", ],
    'hist': [False, "Enable histogram plot", ],
    'stairs': [False, "Enable stair plot", ],
    'capsize': [5, "size of cap on error bar plot"],
    'axes': [None, "set current axis"],
    'linestyle': [None, "linestyle"]
}


@doc.append_doc(ffit.fit_kwargs)
@doc.append_str("\t")
@doc.append_str(doc.table(default, init=False))
@doc.append_str(doc.table({"plot_kwargs        ": ["default", "description"]}, bottom=False))
def plot_kwargs(kwargs):
    """Set default plot_kwargs if not set.

    """
    kwargs = ffit.fit_kwargs(kwargs)
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
        see :func:`plot_kwargs`.

    Returns
    -------
    The best fit function and it's parameters. Also a lambda function where the parameters are already applied.



    """
    best_f, best_ff, lambda_f = ffit.auto(datax, datay, funcs, **kwargs)
    if not best_f is None:
        fit(datax, datay, best_f, **kwargs)
    return best_f, best_ff, lambda_f


# @append_doc(default_kwargs)
def fit(datax, datay, function, **kwargs):
    """
    Fit and plot function to datax and datay.

    Parameters
    ----------
    datax : array_like
        X data either as ``unp.uarray`` or ``np.array`` or ``list``
    datay : array_like
        Y data either as ``unp.uarray`` or ``np.array`` or ``list``
    function : func
        Fit function with parameters: ``x``, ``params``
    **kwargs : optional
        see :func:`plot_kwargs`.
    Fit parameters can be fixed via ``kwargs`` eg. ``a=5``.

    Returns
    -------
    array_like
        Optimized fit parameters of ``function`` to ``datax`` and ``datay``

    Examples
    --------

    .. plot::
        :include-source:

        >>> from smpl import functions as f
        >>> from smpl import plot
        >>> param = plot.fit([0,1,2],[0,1,2],f.line)
        >>> plot.unv(param).round()[0]
        1.0

    """
    kwargs = plot_kwargs(kwargs)
    fit = None
    fig = None
    fig = init_plot(**kwargs)
    if kwargs['also_data']:
        plt_data(datax, datay, **kwargs)
    if kwargs['also_fit']:
        fit, kwargs['fit_color'] = plt_fit(datax, datay, function, **kwargs)
    if kwargs['ss']:
        kwargs['oldshow'] = kwargs['show']
        kwargs['show'] = kwargs['show'] and not kwargs['residue']
        save_plot(**kwargs)
        kwargs['show'] = kwargs['oldshow']
    if kwargs['residue'] and fig is not None:
        plt_residue(datax, datay, function, fit, fig, **kwargs)
    return fit

# @append_doc(default_kwargs)


def data(datax, datay, function=None, **kwargs):
    """
    Plot datay against datax via :func:`fit`

    Parameters
    ----------
    datax : array_like
        X data either as ``unp.uarray`` or ``np.array`` or ``list``
    datay : array_like
        Y data either as ``unp.uarray`` or ``np.array`` or ``list``
    function : func,optional
        Fit function with parameters: ``x``, ``params``
    **kwargs : optional
        see :func:`plot_kwargs`.
    Returns
    -------
    array_like
        Optimized fit parameters of ``function`` to ``datax`` and ``datay``
    """
    if not 'also_fit' in kwargs:
        kwargs['also_fit'] = False
    kwargs = plot_kwargs(kwargs)
    if kwargs['label'] == None and kwargs['lpos'] == 0:
        kwargs['lpos'] = -1
    return fit(datax, datay, function, **kwargs)


def _function(func, xfit, **kwargs):
    kargs = {}
    if util.has('fmt', kwargs):
        kargs["fmt"] = kwargs["fmt"]
    if util.has('label', kwargs) and kwargs['label'] != "":
        kargs['label'] = kwargs['label']
    if util.has('color', kwargs) and kwargs['color'] != "":
        kargs['color'] = kwargs['color']
    if util.has('sigmas', kwargs) and kwargs['sigmas'] != "":
        kargs['sigmas'] = kwargs['sigmas']
    __function(func, xfit, **kargs)


def __function(gfunc, xlinspace, fmt="-", label=None, color=None, hatch=None, sigmas=0.):
    func = gfunc
    x = xlinspace
    l = label
    if isinstance(func(x[0]), uncertainties.UFloat):
        if sigmas > 0:
            ll, = plt.plot(x, unv(func(x)), fmt, color=color)
            y = func(x)
            plt.fill_between(x, unv(y)-sigmas*usd(y), unv(
                y)+sigmas*usd(y), alpha=0.4, label=l, color=ll.get_color(), hatch=hatch)
        else:
            ll, = plt.plot(x, unv(func(x)), fmt, label=l, color=color)
    else:
        ll, = plt.plot(x, func(x), fmt, label=l, color=color)
    return ll


def function(func, *args, **kwargs):
    """
    Plot function ``func`` between ``xmin`` and ``xmax``

    Parameters
    ----------
    func : function
        Function to be plotted between ``xmin`` and ``xmax``, only taking `array_like` ``x`` as parameter
    *args : optional
        arguments for ``func``
    **kwargs : optional
        see :func:`plot_kwargs`.
    """
    if not util.has("xmin", kwargs) or not util.has("xmin", kwargs):
        raise Exception("xmin or xmax missing.")

    # if not util.has('lpos', kwargs) and not util.has('label', kwargs):
    #    kwargs['lpos'] = -1
    if not util.has('fmt', kwargs):
        kwargs['fmt'] = "-"

    kwargs = plot_kwargs(kwargs)
    xlin = np.linspace(kwargs['xmin'], kwargs['xmax'], kwargs['steps'])
    init_plot(**kwargs)

    if not util.has("label", kwargs) or kwargs['label'] is None:
        kwargs['label'] = get_fnc_legend(func, args, **kwargs)
        # kwargs['lpos'] = 0
    #_plot(xfit, func(xfit, *args), **kwargs)
    _function(wrap.get_lambda_argd(
        func, kwargs['xvar'], *args), xlin, **kwargs)
    if kwargs['ss']:
        save_plot(**kwargs)


# xaxis="",yaxis="",fit_color=None,save = None,residue_err=True,show=False):
def plt_residue(datax, datay, gfunction, fit, fig, **kwargs):
    function = wrap.get_lambda(gfunction, kwargs['xvar'])
    fig.add_axes((.1, .1, .8, .2))
    kwargs['yaxis'] = "$\\Delta$" + kwargs['yaxis']
    kwargs['data_color'] = kwargs['fit_color']

    if kwargs['residue_err']:
        plt_data(datax, datay-function(datax, *fit), **kwargs)
    else:
        plt_data(unv(datax), unv(datay-function(datax, *fit)), **kwargs)
    kwargs['lpos'] = -1
    save_plot(**kwargs)


def data_split(datax, datay, **kwargs):
    return ffit.data_split(datax, datay, **kwargs)


def _fit(datax, datay, function, **kwargs):
    """
    Returns a fit like :func:`fit` but does no plotting.
    """
    return ffit.fit(datax, datay, function, **kwargs)


def plt_data(datax, datay, **kwargs):
    """
        Plot datay vs datax
    """
    x, y, xerr, yerr = data_split(datax, datay, **kwargs)
    if xerr is not None:
        xerr = xerr * kwargs['data_sigmas']
    if yerr is not None:
        yerr = yerr * kwargs['data_sigmas']

    if xerr is None and yerr is None:
        if kwargs['fmt'] is None:
            plt.plot(
                x, y, label=kwargs['label'], color=kwargs['data_color'], linestyle=kwargs['linstyle'])
        elif kwargs['fmt'] == "step":
            plt.step(x, y, where='mid',
                     label=kwargs['label'], color=kwargs['data_color'])
        elif kwargs['fmt'] == "hist":
            plt.step(x, y, where='mid',
                     label=kwargs['label'], color=kwargs['data_color'])
            plt.fill_between(x, y, step="mid")
        else:
            plt.plot(x, y, kwargs['fmt'], label=kwargs['label'],
                     color=kwargs['data_color'], linestyle=kwargs['linstyle'])
    else:
        if kwargs['fmt'] is None:
            plt.errorbar(x, y, yerr=yerr, xerr=xerr, fmt=" ", capsize=kwargs["capsize"],
                         label=kwargs['label'], color=kwargs['data_color'], linestyle=kwargs['linstyle'])
        elif kwargs['fmt'] == "step":
            ll, = plt.step(x, y, where='mid',
                           color=kwargs['data_color'])
            if xerr is not None:
                for ix, xv in enumerate(x):
                    dx = (xerr[ix])
                    tx = [xv-dx, xv+dx]
                    plt.fill_between(tx, y[ix]-yerr[ix], y[ix]+yerr[ix],
                                     label=kwargs['label']if ix == 1 else None, alpha=0.2, step='pre', color=ll.get_color())
            else:
                plt.fill_between(x, y-yerr, y+yerr,
                                 label=kwargs['label'], alpha=0.2, step='mid', color=ll.get_color())
        elif kwargs['fmt'] == "hist":
            plt.errorbar(x, y, yerr=yerr, xerr=xerr, fmt=" ", capsize=kwargs["capsize"],
                         color="black")
            plt.fill_between(x, y, step="mid", label=kwargs['label'])
        else:
            plt.errorbar(x, y, yerr=yerr, xerr=xerr, fmt=kwargs['fmt'], capsize=kwargs["capsize"],
                         label=kwargs['label'], color=kwargs['data_color'], linestyle=kwargs['linstyle'])


def get_fnc_legend(function, fit, **kwargs):
    l = wrap.get_latex(function)

    vnames = wrap.get_varnames(function, kwargs['xvar'])
    for i in range(1, len(vnames)):
        l = l + ("\n" if not kwargs["fitinline"] or i == 1 else " ")
        l = l + "$" + sympy.latex(sympy.symbols(str(vnames[i]))) + "$="
        if kwargs['units'] is not None and usd(fit[i-1]) > 0:
            l = l + "("
        if 'number_format' in kwargs:
            l = l + kwargs['number_format'].format(fit[i-1])
        else:
            l = l + "%s" % (fit[i-1])

        if kwargs['units'] is not None and usd(fit[i-1]) > 0:
            l = l + ")"
        if kwargs['units'] is not None:
            l = l + " " + kwargs['units'][i-1]
    return l


def plt_fit(datax, datay, gfunction, **kwargs):
    """
    Plot Fit
    """
    func = wrap.get_lambda(gfunction, kwargs['xvar'])
    fit = _fit(datax, datay, gfunction, **kwargs)
    def fitted(x): return func(x, *fit)
    l = get_fnc_legend(gfunction, fit, **kwargs)
    if kwargs['prange'] is None:
        x, _, _, _ = ffit.fit_split(datax, datay, **kwargs)
        xfit = np.linspace(np.min(unv(x)), np.max(unv(x)), 1000)
    else:
        xfit = np.linspace(kwargs['prange'][0], kwargs['prange'][1], 1000)
    ll = __function(fitted, xfit, "-", label=l,
                    color=kwargs['fit_color'], sigmas=kwargs['sigmas'])

    if (kwargs['frange'] is not None or kwargs['fselector'] is not None) and util.true('interpolate', kwargs) or util.has("interpolate_max", kwargs) or util.has("interpolate_min", kwargs):
        xxfit = np.linspace(util.get("interpolate_min", kwargs, np.min(
            unv(datax))), util.get("interpolate_max", kwargs, np.max(unv(datax))))
        __function(fitted, np.linspace(np.min(xxfit), np.min(xfit)), "--",
                   color=ll.get_color(), hatch=util.get("interpolate_hatch", kwargs, r"||"), sigmas=kwargs['sigmas'])
        __function(fitted, np.linspace(np.max(xfit), np.max(xxfit)), "--",
                   color=ll.get_color(), hatch=util.get("interpolate_hatch", kwargs, r"||"), sigmas=kwargs['sigmas'])
    return fit, ll.get_color()


def init_plot(**kwargs):
    fig = None
    if util.has("axes", kwargs) and kwargs["axes"] is not None:
        plt.sca(kwargs["axes"])
        fig = kwargs["axes"].get_figure()
    if kwargs['init'] or util.true("residue", kwargs):
        if kwargs['size'] is None:
            fig = plt.figure()
        else:
            fig = plt.figure(figsize=kwargs['size'])
        if kwargs['residue']:
            fig.add_axes((.1, .3, .8, .6))
    if util.has("xlabel", kwargs) and kwargs['xlabel'] != "":
        plt.xlabel(kwargs['xlabel'])
    if util.has("ylabel", kwargs) and kwargs['ylabel'] != "":
        plt.ylabel(kwargs['ylabel'])
    if util.has("xaxis", kwargs) and kwargs['xaxis'] != "":
        plt.xlabel(kwargs['xaxis'])
    if util.has("yaxis", kwargs) and kwargs['yaxis'] != "":
        plt.ylabel(kwargs['yaxis'])
    return fig


def save_plot(**kwargs):
    """
        save plot
    """
    if 'logy' in kwargs and kwargs['logy']:
        plt.gca().set_yscale('log')
    if 'logx' in kwargs and kwargs['logx']:
        plt.gca().set_xscale('log')
    if 'tight' in kwargs and kwargs['tight']:
        plt.tight_layout()
    if 'lpos' in kwargs and kwargs['lpos'] >= 0:
        if(util.has('bbox_to_anchor', kwargs)):
            if(util.has('ncol', kwargs)):
                plt.legend(loc=kwargs['lpos'], bbox_to_anchor=kwargs['bbox_to_anchor'],
                           ncol=kwargs['ncol'], borderaxespad=0)
            else:
                plt.legend(loc=kwargs['lpos'],
                           bbox_to_anchor=kwargs['bbox_to_anchor'])
        else:
            plt.legend(loc=kwargs['lpos'])
    # plt.gca().set_xlim([kwargs['xmin'],kwargs['xmax']])
    # plt.gca().set_ylim([kwargs['ymin'],kwargs['ymax']])
    if 'save' in kwargs and not kwargs['save'] == None:
        io.mkdirs(kwargs['save'])
        plt.savefig(kwargs['save'] + ".pdf")
    plt.grid(b=kwargs["grid"])
    if 'show' in kwargs and kwargs['show']:
        show(**kwargs)


def show(**kwargs):
    kwargs = plot_kwargs(kwargs)

    plt.grid(b=kwargs["grid"])
    plt.show()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
