from scipy.interpolate import make_interp_spline, BSpline
from scipy import interpolate as interp
from smpl import doc
from smpl import plot as splot
from smpl import data
import numpy as np
import uncertainties as unc

default = {
    'spline': [True, "Use spline (No alternatives yet)."],
}

# @doc.insert_str("\tDefault kwargs\n\n\t")


@doc.append_doc(data.data_kwargs)
@doc.append_str("\t")
@doc.append_str(doc.table(default, init=False))
@doc.append_str(doc.table({"interpolate_kwargs": ["default", "description"]}, bottom=False))
def interpolate_kwargs(kwargs):
    """Set default interpolate_kwargs if not set.

    """
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
    if len(data) == 2:
        return interpolate_1d(data[0], data[1], **kwargs)
    if len(data) == 3:
        return interpolate_2d(data[0], data[1], data[2], **kwargs)


def interpolate_1d(datax, datay, **kwargs):
    kwargs = interpolate_kwargs(kwargs)
    x, y, dx, dy = interpolate_split(datax, datay, **kwargs)

    if dy is None:
        spl_center = make_interp_spline(x, y, k=3)  # type: BSpline
        return np.vectorize(lambda x: spl_center(x), otypes=["float"])
    else:
        spl_up = make_interp_spline(x, y+dy, k=3)  # type: BSpline
        spl_down = make_interp_spline(x, y-dy, k=3)  # type: BSpline
        # np.abs for uncertainty just in case the numerics are really bad
        return np.vectorize(lambda x: unc.ufloat(spl_up(x)/2 + spl_down(x)/2, np.abs(spl_up(x) - spl_down(x))/2), otypes=["object"])


def interpolate_2d(datax, datay, dataz, **kwargs):
    # TODO beter data handling for 2d -> Nd
    kwargs = interpolate_kwargs(kwargs)
    x, z, dx, dz = interpolate_split(datax, dataz, sortbyx=False, **kwargs)
    y, z, dy, dz = interpolate_split(datay, dataz, sortbyx=False, **kwargs)

    if dz is None:
        spl_center = interp.SmoothBivariateSpline(x, y, z)  # type: BSpline
        return np.vectorize(lambda x, y: spl_center(x, y), otypes=["float"])
    else:
        spl_up = interp.SmoothBivariateSpline(x, y, z+dz)  # type: BSpline
        spl_down = interp.SmoothBivariateSpline(x, y, z-dz)  # type: BSpline
        # np.abs for uncertainty just in case the numerics are really bad
        return np.vectorize(lambda x, y: unc.ufloat(spl_up(x, y)/2 + spl_down(x, y)/2, np.abs(spl_up(x, y) - spl_down(x, y))/2), otypes=["object"])
