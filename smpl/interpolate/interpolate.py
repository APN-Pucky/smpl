import warnings
from scipy import interpolate as interp
from smpl.doc import append_str, append_doc, table
# from smpl import plot as splot
from smpl import data
import numpy as np
import uncertainties as unc
import uncertainties.unumpy as unp
unv = unp.nominal_values
usd = unp.std_devs


def identity(x):
    return x


default = {
    'interpolator': ['cubic', "Use 'cubic' (spline) or 'linear' (cf. <https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html#scipy.interpolate.interp1d>)."],
    'order': [3, "Spline order."],
    'pre': [identity, "pre interpolation"],
    'post': [identity, "post interpolation"],
    'interpolate_upper_uncertainty': [True, "Interpolate only using upper uncertainty."],
    'interpolate_lower_uncertainty': [True, "Interpolate only using lower uncertainty."],
}

# @doc.insert_str("\tDefault kwargs\n\n\t")


@append_doc(data.data_kwargs)
@append_str("\t")
@append_str(table(default, init=False))
@append_str(table({"interpolate_kwargs": ["default", "description"]}, bottom=False))
def interpolate_kwargs(kwargs):
    """Set default interpolate_kwargs if not set.

    """
    kwargs = data.data_kwargs(kwargs)
    for k, v in default.items():
        if not k in kwargs:
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
    kwargs['sortbyx'] = False
    _, y, _, dy = interpolate_split(data[0], data[-1], **kwargs)
    ret = None
    if dy is None:
        spl_center = _interpolate(*data[:-1], (y), **kwargs)
        ret = np.vectorize(spl_center, otypes=["float"])
    else:
        if kwargs['interpolate_upper_uncertainty'] and kwargs['interpolate_lower_uncertainty']:
            spl_up = _interpolate(*data[:-1], (y+dy), **kwargs)
            spl_down = _interpolate(*data[:-1], (y-dy), **kwargs)
            ret = np.vectorize(lambda *a: unc.ufloat(spl_up(*a)/2 + spl_down(*a)/2,
                                                     np.abs(spl_up(*a) - spl_down(*a))/2), otypes=["object"])  # symmetrized error...
            # return np.vectorize(Bounds(spl_up, spl_down), otypes=["object"])
        elif not kwargs['interpolate_lower_uncertainty']:
            spl_center = _interpolate(*data[:-1], (y), **kwargs)
            spl_up = _interpolate(*data[:-1], (y+dy), **kwargs)
            ret = np.vectorize(lambda *a: unc.ufloat(spl_center(*a),
                                                     np.abs(spl_up(*a) - spl_center(*a))), otypes=["object"])  # symmetrized error...
        elif not kwargs['interpolate_upper_uncertainty']:
            spl_center = _interpolate(*data[:-1], (y), **kwargs)
            spl_down = _interpolate(*data[:-1], (y-dy), **kwargs)
            ret = np.vectorize(lambda *a: unc.ufloat(spl_center(*a),
                                                     np.abs(spl_down(*a) - spl_center(*a))), otypes=["object"])  # symmetrized error...
        else:
            raise ValueError(
                "interpolate_upper_uncertainty and interpolate_lower_uncertainty can't be both False")

    if not check(ret, *data):
        warnings.warn("Bad interpolation. Increase Order or symmetrize error.")
    return ret


def check(f, *args):
    return np.all(np.isclose(unv(f(*args[:-1])), unv(args[-1]), rtol=1e-2))


def _interpolate(*data, **kwargs):
    ret = None
    datay = kwargs['pre'](data[-1])
    if len(data) == 2:
        if kwargs['interpolator'] == 'exp':
            ret = _interpolate_exp(*data[:-1], datay)
        else:
            ret = interp.interp1d(
                *data[:-1], datay, kind=kwargs['interpolator'])
    elif len(data) == 3:
        if kwargs['interpolator'] == 'bivariatespline':
            ret = interp.SmoothBivariateSpline(
                *data[:-1], datay, kx=kwargs['order'], ky=kwargs['order'])
        elif kwargs['interpolator'] == 'linearnd':
            ret = interp.LinearNDInterpolator(list(zip(*data[:-1])), datay)
        else:
            ret = interp.interp2d(
                *data[:-1], datay, kind=kwargs['interpolator'])
    else:
        if kwargs['interpolator'] == 'linear':
            ret = interp.LinearNDInterpolator(list(zip(*data[:-1])), datay)

    # return np.vectorize(Post(ret, kwargs['post']), otypes=["object"])
    return np.vectorize(lambda *a: kwargs['post'](ret(*a)), otypes=["object"])


def _interpolate_exp(x, y, **kwargs):
    ip = interp.interp1d(x, np.log(y), kind="linear")
    return lambda x_new: np.exp(ip(x_new))
