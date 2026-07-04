"""
Simplified Interpolating.

Uses scipy.interpolate.
"""

import warnings

import numpy as np
import uncertainties.unumpy as unp
from scipy import interpolate as interp
from scipy.interpolate import bisplev, bisplrep

# from smpl import plot as splot
from smpl import data, doc
from smpl.doc import append_doc, append_str

unv = unp.nominal_values
usd = unp.std_devs


# mimick removed interp2d from scipy
# https://scipy.github.io/devdocs/tutorial/interpolate/interp_transition_guide.html
def interp_interp2d(xxr, yyr, zzr, kind="linear"):
    kx = 1
    ky = 1
    if kind == "linear":
        kx = 1
        ky = 1
    elif kind == "cubic":
        kx = 3
        ky = 3
    else:
        err = f"kind must be 'linear' or 'cubic', got {kind}"
        raise ValueError(err)
    tck = bisplrep(xxr, yyr, zzr, kx=kx, ky=ky)

    def f(xnew, ynew):
        xnew = np.asarray(xnew)
        ynew = np.asarray(ynew)

        if xnew.shape == ynew.shape:
            return np.array(
                [
                    bisplev(float(xi), float(yi), tck)
                    for xi, yi in zip(xnew.ravel(), ynew.ravel())
                ]
            ).reshape(xnew.shape)

        return bisplev(xnew, ynew, tck).T

    return f


def identity(x):
    return x


default = {
    "interpolator": [
        "cubic",
        "Use 'cubic' (spline) or 'linear' (cf. <https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html#scipy.interpolate.interp1d>).",
    ],
    "order": [3, "Spline order."],
    "pre": [identity, "pre interpolation"],
    "post": [identity, "post interpolation"],
    "interpolate_upper_uncertainty": [
        True,
        "Interpolate only using upper uncertainty.",
    ],
    "interpolate_lower_uncertainty": [
        True,
        "Interpolate only using lower uncertainty.",
    ],
}

# @doc.insert_str("\tDefault kwargs\n\n\t")


@append_doc(data.data_kwargs)
@append_str("\t")
@append_str(doc.array_table(default, init=False))
@append_str(
    doc.array_table({"interpolate_kwargs": ["default", "description"]}, bottom=False)
)
def interpolate_kwargs(kwargs):
    """Set default interpolate_kwargs if not set."""
    kwargs = data.data_kwargs(kwargs)
    for k, v in default.items():
        if k not in kwargs:
            kwargs[k] = v[0]
    return kwargs


def interpolate_split(datax, datay, **kwargs):
    """
    Splits datax and datay into (x,y,xerr,yerr).

    Parameters
    ----------
    **kwargs : optional
        see :func:`interpolate_kwargs`.
    """
    kwargs = interpolate_kwargs(kwargs)
    return data.filtered_data_split(datax, datay, **kwargs)


def interpolate(*data, **kwargs):
    # TODO save spl_upd spl_down values instead of recalculate
    # TODO set eps
    kwargs = interpolate_kwargs(kwargs)
    kwargs["sortbyx"] = False
    _, y, _, dy = interpolate_split(data[0], data[-1], **kwargs)
    ret = None
    if dy is None:
        spl_center = _interpolate(*data[:-1], (y), **kwargs)
        ret = spl_center
        # ret = np.vectorize(spl_center, otypes=["float"])
    elif (
        kwargs["interpolate_upper_uncertainty"]
        and kwargs["interpolate_lower_uncertainty"]
    ):
        spl_up = _interpolate(*data[:-1], (y + dy), **kwargs)
        spl_down = _interpolate(*data[:-1], (y - dy), **kwargs)
        ret = lambda *a: unp.uarray(
            spl_up(*a) / 2 + spl_down(*a) / 2,
            np.abs(spl_up(*a) - spl_down(*a)) / 2,
        )  # symmetrized error...
        # ret = np.vectorize(ret , otypes=["object"],)
        # return np.vectorize(Bounds(spl_up, spl_down), otypes=["object"])
    elif not kwargs["interpolate_lower_uncertainty"]:
        spl_center = _interpolate(*data[:-1], (y), **kwargs)
        spl_up = _interpolate(*data[:-1], (y + dy), **kwargs)
        ret = lambda *a: unp.uarray(
            spl_center(*a), np.abs(spl_up(*a) - spl_center(*a))
        )  # symmetrized error...
        # ret = np.vectorize(ret, otypes=["object"],)
    elif not kwargs["interpolate_upper_uncertainty"]:
        spl_center = _interpolate(*data[:-1], (y), **kwargs)
        spl_down = _interpolate(*data[:-1], (y - dy), **kwargs)
        ret = lambda *a: unp.uarray(
            spl_center(*a), np.abs(spl_down(*a) - spl_center(*a))
        )  # symmetrized error...
        # ret = np.vectorize( ret , otypes=["object"],)
    else:
        err = "interpolate_upper_uncertainty and interpolate_lower_uncertainty can't be both False"
        raise ValueError(err)

    if not check(ret, *data):
        warnings.warn(
            "Bad interpolation. Increase Order or symmetrize error.",
            UserWarning,
            stacklevel=2,
        )
    return ret


def check(f, *args):
    val = f(*args[:-1])
    unvval = unv(val)
    close = np.isclose(unvval, unv(args[-1]), rtol=1e-2)
    return np.all(close)


def _interpolate(*data, **kwargs):
    ret = None
    datay = kwargs["pre"](data[-1])
    if len(data) == 2:
        if kwargs["interpolator"] == "exp":
            ret = _interpolate_exp(*data[:-1], datay)
        else:
            ret = interp.interp1d(*data[:-1], datay, kind=kwargs["interpolator"])
    elif len(data) == 3:
        if kwargs["interpolator"] == "bivariatespline":
            spline = interp.SmoothBivariateSpline(
                *data[:-1], datay, kx=kwargs["order"], ky=kwargs["order"]
            )

            def spline_no_grid(*a):
                return spline(*a, grid=False)

            ret = spline_no_grid
        elif kwargs["interpolator"] == "linearnd":
            ret = interp.LinearNDInterpolator(list(zip(*data[:-1])), datay)
        else:
            ret = interp_interp2d(*data[:-1], datay, kind=kwargs["interpolator"])
    elif kwargs["interpolator"] == "linear":
        ret = interp.LinearNDInterpolator(list(zip(*data[:-1])), datay)

    # return np.vectorize(Post(ret, kwargs['post']), otypes=["object"])
    return lambda *a: kwargs["post"](ret(*a))


def _interpolate_exp(x, y):
    ip = interp.interp1d(x, np.log(y), kind="linear")
    return lambda x_new: np.exp(ip(x_new))
