from scipy.interpolate import make_interp_spline, BSpline
from smpl import doc
from smpl import plot as splot
from smpl import data
import uncertainties

default = {
           'spline' : [True,"Use spline (No alternatives yet)."],
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
    return data.filtered_data_split(datax,datay,**kwargs)


def interpolate(datax,datay,**kwargs):
    kwargs  = interpolate_kwargs(kwargs)
    x,y,dx,dy = interpolate_split(datax,datay**kwargs)
    spl_center = make_interp_spline(splot.unv(datax), splot.unv(datay), k=3)  # type: BSpline
    spl_up = make_interp_spline(splot.unv(datax), splot.unv(datay) + splot.usd(datay), k=3)  # type: BSpline
    spl_down = make_interp_spline(splot.unv(datax), splot.unv(datay) - splot.usd(datay), k=3)  # type: BSpline

    if kwargs['yerror']:
        return lambda x : uncertainties.ufloat(spl_up(x)/2+ spl_down(x)/2,(spl_up(x)- spl_down(x))/2)
    else:
        return spl_center

    # TODO add option to interpolate in plot
    # TODO interpolation examples/tests
    # TODO map examples/tests