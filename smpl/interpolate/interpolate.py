from scipy.interpolate import make_interp_spline, BSpline
from smpl import doc
from smpl import data

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
        see :func:`fit_kwargs`.
    """
    kwargs = interpolate_kwargs(kwargs)
    return data.filtered_data_split(datax,datay,**kwargs)


def interpolate():
    pass
#    spl = make_interp_spline(vx, splot.unv(vy), k=3)  # type: BSpline
#    power_smooth = spl(xnew)