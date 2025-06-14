"""Simplified plotting."""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import smplr
import sympy
import uncertainties
import uncertainties.unumpy as unp
from matplotlib import pylab
from matplotlib.pyplot import *

# local imports
from smpl import doc, interpolate, io, stat, util, wrap
from smpl import fit as ffit


def set_plot_style():
    # fig_size = (8, 6)
    # fig_legendsize = 14
    # fig_labelsize = 12 # ‘xx-small’, ‘x-small’, ‘small’, ‘medium’, ‘large’, ‘x-large’, ‘xx-large’.
    params = {
        "legend.fontsize": "x-large",
        "figure.figsize": (8, 6),
        "axes.labelsize": "x-large",
        "axes.titlesize": "x-large",
        "xtick.labelsize": "x-large",
        "ytick.labelsize": "x-large",
    }
    pylab.rcParams.update(params)
    matplotlib.rcParams.update(params)
    # matplotlib.rcParams.update({'font.size': fig_labelsize})
    # colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)


unv = unp.nominal_values
usd = unp.std_devs

default = {
    #    'params'        :[None      ,"Initial fit parameters",
    "title": [None, "Plot title"],
    "xlabel": [
        "",
        "X axis label",
    ],
    "ylabel": [
        "",
        "Y axis label",
    ],
    "label": [
        None,
        "Legend name of plotted ``data``",
    ],
    "fmt": [
        ".",
        "Format for plotting fit function (could be a line style, marker or a combination of both or 'step')",
    ],
    "where": [
        "mid",
        "Where to place the ticks. Possible values are 'pre', 'post', 'mid', 'edge'. Might be incompatible with uncertainties.",
    ],
    "units": [
        None,
        "Units of the fit parameters as strings. Displayed in the Legend",
    ],
    "save": [
        None,
        " File to save the plot",
    ],
    "lpos": [
        0,
        "Legend position",
    ],
    "tight": [
        True,
        "tight_layout",
    ],
    #          'frange'        :[None      ,"Limit the fit to given range. First integer is the lowest and second the highest index.",],
    "prange": [
        None,
        "Limit the plot of the fit to given range",
    ],
    "sigmas": [
        0,
        "Color the array of given ``sigma`` times uncertainty. Only works if the fit function is coded with ``unp``",
    ],
    "data_sigmas": [
        1,
        "Color the array of given ``sigma`` times uncertainty. Only works if the data has uncertainties",
    ],
    "init": [False, "Initialize a new plot"],
    "ss": [
        True,
        "save, add legends and grid to the plot",
    ],
    "also_data": [True, " also plot the data"],
    "also_fit": [
        True,
        "also plot the fit",
    ],
    "auto_fit": [
        False,
        "automatically fit",
    ],
    "logy": [
        False,
        "logarithmic x axis",
    ],
    "logx": [
        False,
        "logarithmic y axis",
    ],
    "function_color": [
        None,
        "Color of the function plot",
    ],
    "data_color": [
        None,
        "Color of the data plot",
    ],
    "fit_color": [
        None,
        "Color of the fit plot",
    ],
    "fit_fmt": [
        "-",
        "Format of the fit plot",
    ],
    "residue": [
        False,
        "Display difference between fit and data in a second plot",
    ],
    "residue_err": [
        True,
        "Differences between fit and data will have errorbars",
    ],
    "show": [
        False,
        "Call plt.show()",
    ],
    "size": [
        None,
        "Size of the plot as a tuple (x,y). Only has an effect if ``init`` is True",
    ],
    "number_format": [
        io.gf(4),
        "Format to display numbers.",
    ],
    # ,          'selector'      :[ None     ,"Function that takes ``x`` and ``y`` as parameters and returns an array mask in order to limit the data points for fitting. Alternatively a mask for selecting elements from datax and datay.",],
    # ,          'fixed_params'  :[ True     ,"Enable fixing parameters by choosing the same-named variables from ``kwargs``.",],
    # ,          'sortbyx'       :[ True     , "Enable sorting the x and y data so that x is sorted.",],
    "interpolate": [False, "Enable interpolation of the data."],
    "interpolate_fmt": [
        "-",
        "Either format string or linestyle tuple.",
    ],
    "interpolate_label": [
        None,
        "Label for the interpolation.",
    ],
    "extrapolate": [
        True,
        "Enable extrapolation of whole data if fit range is limited by ``frange`` or ``fselector``.",
    ],
    "extrapolate_min": [
        None,
        "Lower extrapolation bound",
    ],
    "extrapolate_max": [
        None,
        "Higher extrapolation bound",
    ],
    "extrapolate_fmt": [
        "--",
        "Format of the extrapolation line",
    ],
    "extrapolate_hatch": [
        r"||",
        "Extrapolation shape/hatch for filled area in case of ``sigmas``>0. See https://matplotlib.org/stable/gallery/shapes_and_collections/hatch_style_reference.html",
    ],
    "bbox_to_anchor": [
        None,
        "Position in a tuple (x,y),Shift position of the legend out of the main pane. ",
    ],
    "ncol": [
        None,
        "Columns in the legend if used with ``bbox_to_anchor``.",
    ],
    "steps": [
        1000,
        "resolution of the plotted function",
    ],
    "fitinline": [
        False,
        "No newlines for each fit parameter",
    ],
    "grid": [
        True,
        "Enable grid for the plot",
    ],
    "hist": [
        False,
        "Enable histogram plot",
    ],
    "stairs": [
        False,
        "Enable stair plot",
    ],
    "capsize": [5, "size of cap on error bar plot"],
    "axes": [None, "set current axis"],
    "linestyle": [None, "linestyle, only active if `fmt`=None"],
    "xspace": [
        np.linspace,
        "xspace gets called with xspace(xmin,xmax,steps) in :func:`function` to get the points of the function that will be drawn.",
    ],
    "alpha": [0.2, "alpha value for the fill_between plot"],
}


@doc.append_doc(ffit.fit_kwargs)
@doc.append_str("\t")
@doc.append_str(doc.array_table(default, init=False))
@doc.append_str(
    doc.array_table({"plot_kwargs        ": ["default", "description"]}, bottom=False)
)
@doc.append_str("\n\n")
def plot_kwargs(kwargs):
    """Set default :func:`plot_kwargs` if not set."""
    kwargs = ffit.fit_kwargs(kwargs)
    for k, v in default.items():
        if k not in kwargs:
            kwargs[k] = v[0]
    return kwargs


# TODO optimize to minimize number of calls to function
# @append_doc(default_kwargs)


def fit(func, *adata, **kwargs):
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
        Optimized fit parameters of ``function`` to ``datax`` and ``datay``.
        If ``datay`` is complex, both the real and imaginary part are returned.

    Examples
    --------

    .. plot::
        :include-source:

        >>> from smpl import functions as f
        >>> from smpl import plot
        >>> param = plot.fit([0,1,2],[0,1,2],f.line)
        >>> float(plot.unv(param).round()[0])
        1.0

    """
    if "xaxis" in kwargs and ("xlabel" not in kwargs or not kwargs["xlabel"]):
        # warnings.warn("xaxis is deprecated. Use xlabel instead.", DeprecationWarning, 2)
        kwargs["xlabel"] = kwargs["xaxis"]
        # TODO maybe pop
    if "yaxis" in kwargs and ("ylabel" not in kwargs or not kwargs["ylabel"]):
        # warnings.warn("yaxis is deprecated. Use ylabel instead.", DeprecationWarning, 2)
        kwargs["ylabel"] = kwargs["yaxis"]
        # TODO maybe pop

    function = func
    if "function" in kwargs:
        function = kwargs["function"]
        del kwargs["function"]
        adata = [func, *adata]
    # Fix parameter order if necessary
    elif isinstance(function, (list, tuple, np.ndarray)):
        adata = [adata[-1], function, *adata[:-1]]
        function = adata[0]
        adata = adata[1:]
    if util.true("bins", kwargs):
        # yvalue will be overwritten
        ndata = [*adata, *adata]
        for i, o in enumerate(adata):
            ndata[2 * i] = o
            ndata[2 * i + 1] = o * 0
        adata = ndata

    assert len(adata) % 2 == 0, "data must be pairs of x and y data"
    if len(adata) == 2:
        datax, datay = adata
    else:
        rs = []
        for i in range(0, len(adata), 2):
            datax, datay = adata[i], adata[i + 1]
            if util.true("bins", kwargs):
                rs.append(fit(function, datax, **kwargs))
            else:
                rs.append(fit(function, datax, datay, **kwargs))
        return rs

    kwargs = plot_kwargs(kwargs)

    if np.any(np.iscomplex(datay)):
        label = util.get("label", kwargs, "")
        kwargs["label"] = label + "(real)"
        r = fit(datax, datay.real, function=function, **kwargs)
        kwargs["label"] = label + "(imag)"
        i = fit(datax, datay.imag, function=function, **kwargs)
        return r, i
    if kwargs["auto_fit"]:
        best_f, best_ff, lambda_f = ffit.auto(datax, datay, function, **kwargs)
        if best_f is not None:
            del kwargs["auto_fit"]
            fit(datax, datay, best_f, **kwargs)
        return best_f, best_ff, lambda_f
    if kwargs["also_fit"] == False and kwargs["label"] is None and kwargs["lpos"] == 0:
        kwargs["lpos"] = -1
    return _fit_impl(datax, datay, function, **kwargs)


def _fit_impl(datax, datay, function, **kwargs):
    x = None
    y = None
    rfit = None
    ifit = None
    fig = None
    fig = init_plot(kwargs)
    ll = None
    if kwargs["also_data"]:
        ll = plt_data(datax, datay, **kwargs).get_color()
    if kwargs["interpolate"]:
        ifit, _, x, y = plt_interpolate(datax, datay, icolor=ll, **kwargs)
    if kwargs["also_fit"]:
        assert function is not None, "function must be given"
        rfit, kwargs["fit_color"], _, _ = plt_fit(datax, datay, function, **kwargs)
    if kwargs["ss"]:
        kwargs["oldshow"] = kwargs["show"]
        kwargs["show"] = kwargs["show"] and not kwargs["residue"]
        save_plot(**kwargs)
        kwargs["show"] = kwargs["oldshow"]
    if kwargs["residue"] and fig is not None:
        plt_residue(datax, datay, function, rfit, fig, **kwargs)
    if not kwargs["also_fit"] and kwargs["interpolate"]:
        return (ifit, x, y)
        # return ifit
    return rfit


# @append_doc(default_kwargs)


def data(*data, function=None, **kwargs):
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
    if "also_fit" not in kwargs:
        kwargs["also_fit"] = False
    kwargs = plot_kwargs(kwargs)
    return fit(function=function, *data, **kwargs)


# @append_doc(default_kwargs)


def auto(*adata, funcs=None, **kwargs):
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
    if "auto_fit" not in kwargs:
        kwargs["auto_fit"] = True
    kwargs = plot_kwargs(kwargs)
    return fit(function=funcs, *adata, **kwargs)


def _function(
    func,
    xfit,
    fmt="-",
    label=None,
    function_color=None,
    sigmas=0.0,
    alpha=0.4,
    **kwargs,
):
    # kargs = {}
    # if util.has("fmt", kwargs):
    #    kargs["fmt"] = kwargs["fmt"]
    # if util.has("label", kwargs) and kwargs["label"] != "":
    #    kargs["label"] = kwargs["label"]
    # if util.has("function_color", kwargs) and kwargs["function_color"] != "":
    #    kargs["color"] = kwargs["function_color"]
    # if util.has("sigmas", kwargs) and kwargs["sigmas"] != "":
    #    kargs["sigmas"] = kwargs["sigmas"]
    # if util.has("alpha", kwargs) and kwargs["alpha"] != "":
    #    kargs["alpha"] = kwargs["alpha"]
    # __function(func, xfit,  **kargs)

    if label == "":
        label = None
    if function_color == "":
        function_color = None
    if sigmas == "":
        sigmas = 0.0
    if alpha == "":
        alpha = 0.4
    __function(
        func,
        xfit,
        fmt=fmt,
        label=label,
        color=function_color,
        sigmas=sigmas,
        alpha=alpha,
        **kwargs,
    )


def plt_plt(x, y, fmt, color, label, linestyle, **kwargs):
    if linestyle is None and fmt is not None:
        return plt.plot(x, y, fmt, label=label, color=color, **kwargs)
    if linestyle is not None and fmt is None:
        return plt.plot(x, y, label=label, color=color, linestyle=linestyle, **kwargs)
    if linestyle is None and fmt is None:
        return plt.plot(x, y, label=label, color=color, **kwargs)
    # should not reach here
    raise ValueError(
        "Either fmt or linestyle must be given, but not both. fmt=%s, linestyle=%s"
        % (fmt, linestyle)
    )


def __function(
    gfunc,
    xlinspace,
    fmt="-",
    label=None,
    color=None,
    hatch=None,
    sigmas=0.0,
    linestyle=None,
    alpha=0.4,
    **kwargs,
):
    # filter unused bad kwargs here to avoid passing them down
    # TODO it would be better to not pass them down in the first place
    for key in [
        "pre",
        "post",
        "xaxis",
        "yaxis",
        "xvar",
        "xmin",
        "xmax",
        "xlabel",
        "ylabel",
        "bins",
        "binunc",
        "bbox_to_anchor",
        "tight",
        "residue",
        "lpos",
        "interpolate",
        "params",
        "also_fit",
        "init",
        "frange",
        "epsfcn",
        "units",
        "fselector",
        "maxfev",
        "sortbyx",
        "xerror",
        "yerror",
        "fixed_params",
        "autotqdm",
        "fitter",
        "title",
        "where",
        "save",
        "prange",
        "ss",
        "also_data",
        "auto_fit",
        "data_sigmas",
        "logy",
        "logx",
        "data_color",
        "fit_color",
        "fit_fmt",
        "show",
        "size",
        "number_format",
        "selector",
        "fitinline",
        "grid",
        "hist",
        "stairs",
        "capsize",
        "axes",
        "xspace",
        "extrapolate",
        "extrapolate_min",
        "extrapolate_max",
        "extrapolate_fmt",
        "extrapolate_hatch",
        "function_color",
        "residue_err",
        "interpolate_fmt",
        "interpolate_label",
        "interpolate_lower_uncertainty",
        "ncol",
        "steps",
        "interpolator",
        "next_color",
    ]:
        kwargs.pop(key, None)
    func = gfunc
    x = xlinspace
    l = label

    if isinstance(func(x)[0], uncertainties.UFloat):
        if sigmas > 0:
            (ll,) = plt_plt(
                x,
                unv(func(x)),
                fmt,
                label=None,
                color=color,
                linestyle=linestyle,
                **kwargs,
            )
            y = func(x)
            plt.fill_between(
                x,
                unv(y) - sigmas * usd(y),
                unv(y) + sigmas * usd(y),
                alpha=alpha,
                label=l,
                color=ll.get_color(),
                hatch=hatch,
                **kwargs,
            )
        else:
            (ll,) = plt_plt(
                x,
                unv(func(x)),
                fmt,
                label=l,
                color=color,
                linestyle=linestyle,
                **kwargs,
            )
    else:
        (ll,) = plt_plt(
            x, func(x), fmt, label=l, color=color, linestyle=linestyle, **kwargs
        )
    return ll


def function(func, *args, fmt="-", **kwargs):
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
    kwargs["fmt"] = fmt
    if not util.has("xmin", kwargs) or not util.has("xmax", kwargs):
        kwargs["xmin"], kwargs["xmax"] = stat.get_interesting_domain(func)
        # raise Exception("xmin or xmax missing.")

    # if not util.has('lpos', kwargs) and not util.has('label', kwargs):
    #    kwargs['lpos'] = -1

    if "label" not in kwargs:
        kwargs = plot_kwargs(kwargs)
        kwargs["label"] = get_fnc_legend(func, args, **kwargs)
    else:
        kwargs = plot_kwargs(kwargs)

    xlin = kwargs["xspace"](kwargs["xmin"], kwargs["xmax"], kwargs["steps"])
    init_plot(kwargs)

    # kwargs['lpos'] = 0
    # _plot(xfit, func(xfit, *args), **kwargs)
    _function(wrap.get_lambda_argd(func, kwargs["xvar"], *args), xlin, **kwargs)
    if kwargs["ss"]:
        save_plot(**kwargs)


# xaxis="",yaxis="",fit_color=None,save = None,residue_err=True,show=False):
def plt_residue(datax, datay, gfunction, rfit, fig, **kwargs):
    function = wrap.get_lambda(gfunction, kwargs["xvar"])
    fig.add_axes((0.1, 0.1, 0.8, 0.2))
    kwargs["ylabel"] = "$\\Delta$" + kwargs["ylabel"]
    kwargs["data_color"] = kwargs["fit_color"]

    if kwargs["residue_err"]:
        plt_data(datax, datay - function(datax, *rfit), **kwargs)
    else:
        plt_data(unv(datax), unv(datay - function(datax, *rfit)), **kwargs)
    kwargs["lpos"] = -1
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
        xerr = xerr * kwargs["data_sigmas"]
    if yerr is not None:
        yerr = yerr * kwargs["data_sigmas"]

    ll = None
    if xerr is None and yerr is None:
        if kwargs["fmt"] is None:
            if kwargs["linestyle"] is None:
                (ll,) = plt.plot(
                    x, y, label=kwargs["label"], color=kwargs["data_color"]
                )
            else:
                (ll,) = plt.plot(
                    x,
                    y,
                    label=kwargs["label"],
                    color=kwargs["data_color"],
                    linestyle=kwargs["linestyle"],
                )
        elif kwargs["fmt"] == "step":
            (ll,) = plt.step(
                x,
                y,
                where=kwargs["where"],
                label=kwargs["label"],
                color=kwargs["data_color"],
            )
        elif kwargs["fmt"] == "hist":
            (ll,) = plt.step(
                x,
                y,
                where=kwargs["where"],
                label=kwargs["label"],
                color=kwargs["data_color"],
            )
            plt.fill_between(x, y, step="mid", color=ll.get_color())
        else:
            (ll,) = plt.plot(
                x, y, kwargs["fmt"], label=kwargs["label"], color=kwargs["data_color"]
            )
    elif kwargs["fmt"] is None:
        if kwargs["linestyle"] is None:
            (
                ll,
                _,
                _,
            ) = plt.errorbar(
                x,
                y,
                yerr=yerr,
                xerr=xerr,
                fmt=" ",
                capsize=kwargs["capsize"],
                label=kwargs["label"],
                color=kwargs["data_color"],
            )
        else:
            (
                ll,
                _,
                _,
            ) = plt.errorbar(
                x,
                y,
                yerr=yerr,
                xerr=xerr,
                fmt=" ",
                capsize=kwargs["capsize"],
                label=kwargs["label"],
                color=kwargs["data_color"],
                linestyle=kwargs["linestyle"],
            )
    elif kwargs["fmt"] == "step":
        (ll,) = plt.step(x, y, where=kwargs["where"], color=kwargs["data_color"])
        if xerr is not None:
            for ix, xv in enumerate(x):
                dx = xerr[ix]
                tx = [xv - dx, xv + dx]
                plt.fill_between(
                    tx,
                    y[ix] - yerr[ix],
                    y[ix] + yerr[ix],
                    label=kwargs["label"] if ix == 1 else None,
                    alpha=kwargs["alpha"],
                    step="pre",
                    color=ll.get_color(),
                )
        else:
            plt.fill_between(
                x,
                y - yerr,
                y + yerr,
                label=kwargs["label"],
                alpha=kwargs["alpha"],
                step="mid",
                color=ll.get_color(),
            )
    elif kwargs["fmt"] == "hist":
        (
            ll,
            _,
            _,
        ) = plt.errorbar(
            x,
            y,
            yerr=yerr,
            xerr=xerr,
            fmt=" ",
            capsize=kwargs["capsize"],
            color="black",
        )
        plt.fill_between(x, y, step="mid", label=kwargs["label"], color=ll.get_color())
    else:
        (
            ll,
            _,
            _,
        ) = plt.errorbar(
            x,
            y,
            yerr=yerr,
            xerr=xerr,
            fmt=kwargs["fmt"],
            capsize=kwargs["capsize"],
            label=kwargs["label"],
            color=kwargs["data_color"],
        )
    return ll


def get_fnc_legend(function, rfit, **kwargs):
    l = wrap.get_latex(function)

    vnames = wrap.get_varnames(function, kwargs["xvar"])
    for i in range(1, len(vnames)):
        l = l + ("\n" if not kwargs["fitinline"] or i == 1 else " ")
        l = l + "$" + sympy.latex(sympy.symbols(str(vnames[i]))) + "$="
        if kwargs["units"] is not None and usd(rfit[i - 1]) > 0:
            l = l + "("
        if "number_format" in kwargs:
            l = l + kwargs["number_format"].format(rfit[i - 1])
        else:
            l = l + "%s" % (rfit[i - 1])

        if kwargs["units"] is not None and usd(rfit[i - 1]) > 0:
            l = l + ")"
        if kwargs["units"] is not None:
            l = l + " " + kwargs["units"][i - 1]
    return l


def plt_fit_or_interpolate(
    datax, datay, fitted, l=None, c=None, f=None, ls=None, **kwargs
):
    # just filter these kwargs out, so they dont get passed down and are replaced by above args
    # TODO why not pass label=XXX directly to this?
    #      -> probably since there are cases where both e.g. color and replace color are needed
    for key in ["color", "label", "fmt", "linestyle", "hatch"]:
        kwargs.pop(key, None)
    if kwargs["prange"] is None:
        x, _, _, _ = ffit.fit_split(datax, datay, **kwargs)
        xfit = kwargs["xspace"](np.min(unv(x)), np.max(unv(x)), kwargs["steps"])
    else:
        xfit = kwargs["xspace"](
            kwargs["prange"][0], kwargs["prange"][1], kwargs["steps"]
        )
    ll = __function(
        fitted,
        xfit,
        kwargs["fit_fmt"] if f is not None and ls is None else f,
        label=l,
        color=kwargs["fit_color"] if c is None else c,
        linestyle=ls,
        **kwargs,
    )

    if (
        (
            (kwargs["frange"] is not None or kwargs["fselector"] is not None)
            and util.true("extrapolate", kwargs)
        )
        or util.has("extrapolate_max", kwargs)
        or util.has("extrapolate_min", kwargs)
    ):
        xxfit = kwargs["xspace"](
            util.get("extrapolate_min", kwargs, np.min(unv(datax))),
            util.get("extrapolate_max", kwargs, np.max(unv(datax))),
            kwargs["steps"],
        )
        for pmin, pmax in [
            (np.min(xxfit), np.min(xfit)),
            (np.max(xfit), np.max(xxfit)),
        ]:
            __function(
                fitted,
                kwargs["xspace"](pmin, pmax, kwargs["steps"]),
                util.get("extrapolate_fmt", kwargs, "--"),
                color=ll.get_color(),
                hatch=util.get("extrapolate_hatch", kwargs, r"||"),
                **kwargs,
            )
    return ll.get_color(), xfit, fitted(xfit)


def plt_interpolate(datax, datay, icolor=None, **kwargs):
    """
    Interpolate and Plot that Interpolation.
    """
    inter = interpolate.interpolate(datax, datay, **kwargs)
    kargs = {}
    if isinstance(kwargs["interpolate_fmt"], tuple):
        kargs["ls"] = kwargs["interpolate_fmt"]
    else:
        kargs["f"] = kwargs["interpolate_fmt"]
    if kwargs["interpolate_label"] is not None:
        kargs["l"] = kwargs["interpolate_label"]
    # l = None so that no label
    return (
        inter,
        *plt_fit_or_interpolate(datax, datay, inter, c=icolor, **kargs, **kwargs),
    )


def plt_fit(datax, datay, gfunction, **kwargs):
    """
    Fit and Plot that Fit.
    """
    func = wrap.get_lambda(gfunction, kwargs["xvar"])
    rfit = _fit(datax, datay, gfunction, **kwargs)

    def fitted(x):
        return func(x, *rfit)

    vnames = wrap.get_varnames(gfunction, kwargs["xvar"])
    for v in vnames[1:]:  # remove fixed parameters from kwargs
        kwargs.pop(v, None)

    l = get_fnc_legend(gfunction, rfit, **kwargs)
    return (rfit, *plt_fit_or_interpolate(datax, datay, fitted, l, **kwargs))


def init_plot(kwargs):
    fig = None
    if util.has("axes", kwargs) and kwargs["axes"] is not None:
        plt.sca(kwargs["axes"])
        fig = kwargs["axes"].get_figure()
    if kwargs["init"] or util.true("residue", kwargs):
        if kwargs["size"] is None:
            fig = plt.figure()
        else:
            fig = plt.figure(figsize=kwargs["size"])
        if kwargs["residue"]:
            fig.add_axes((0.1, 0.3, 0.8, 0.6))
    if util.has("next_color", kwargs) and not kwargs["next_color"]:
        lines = plt.gca()._get_lines
        tmp_color = lines._cycler_items[lines._idx]["color"]

        if kwargs["data_color"] is None:
            kwargs["data_color"] = tmp_color
        if kwargs["fit_color"] is None:
            kwargs["fit_color"] = tmp_color
        if kwargs["function_color"] is None:
            kwargs["function_color"] = tmp_color
    return fig


def save_plot(**kwargs):
    """
    save plot
    """
    smplr.style_plot1d(**kwargs)
    if "lpos" in kwargs and kwargs["lpos"] >= 0:
        if util.has("bbox_to_anchor", kwargs):
            if util.has("ncol", kwargs):
                plt.legend(
                    loc=kwargs["lpos"],
                    bbox_to_anchor=kwargs["bbox_to_anchor"],
                    ncol=kwargs["ncol"],
                    borderaxespad=0,
                )
            else:
                plt.legend(loc=kwargs["lpos"], bbox_to_anchor=kwargs["bbox_to_anchor"])
        else:
            plt.legend(loc=kwargs["lpos"])
    if "save" in kwargs and kwargs["save"] is not None:
        io.mkdirs(kwargs["save"])
        plt.savefig(kwargs["save"] + ".pdf")
    if kwargs.get("show"):
        show(**kwargs)


def show(**kwargs):
    kwargs = plot_kwargs(kwargs)

    smplr.style_plot1d(**kwargs)
    plt.show()


from smpl.plot2d import plot2d as _plot2d
from smpl.plot2d import plot2d_kwargs as _plot2d_kwargs


def plot2d(*args, **kwargs):
    _plot2d(*args, **kwargs)


def plot2d_kwargs(*args, **kwargs):
    _plot2d_kwargs(*args, **kwargs)
