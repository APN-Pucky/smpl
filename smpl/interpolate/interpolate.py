from scipy.interpolate import make_interp_spline, BSpline
from smpl import doc

default = {
           'params': [None, "Initial fit parameters", ],
           'frange': [None, "Limit the fit to given range. First integer is the lowest and second the highest index.", ],
           'fselector': [None, "Function that takes ``x`` and ``y`` as parameters and returns an array mask in order to limit the data points for fitting. Alternatively a mask for selecting elements from datax and datay.", ],
           'fixed_params': [True, "Enable fixing parameters by choosing the same-named variables from ``kwargs``.", ],
           'sortbyx': [True, "Enable sorting the x and y data so that x is sorted.", ],
           'maxfev': [10000, "Maximum function evaluations during fitting.", ],
           'epsfcn': [0.0001, "Suitable step length for jacobian approximation.", ],
           'xvar': [None, "Variable in fit function parameters that corresponds to the x axis. If it is None the last of the alphabetical sorted parameters is used.", ],
           'bins': [0, "Number of bins for histogram", ],
           'binunc': [stat.poisson_dist, "Number of bins for histogram", ],
           'autotqdm': [True, "Auto fitting display tqdm", ],
           'xerror': [True, "enable xerrors"],
           'yerror': [True, "enable yerrors"],
           }

# @doc.insert_str("\tDefault kwargs\n\n\t")


@doc.append_str(doc.table(default, init=False))
@doc.append_str(doc.table({"interpolate_kwargs": ["default", "description"]}, bottom=False))
def interpolate_kwargs(kwargs):
    """Set default interpolate_kwargs if not set.

    """
    for k, v in default.items():
        if not k in kwargs:
            kwargs[k] = v[0]
    return kwargs

def interpolate():
    spl = make_interp_spline(vx, splot.unv(vy), k=3)  # type: BSpline
    power_smooth = spl(xnew)