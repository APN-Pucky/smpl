import numpy as np
import statistics as stat
import scipy as sci
import scipy.integrate as integrate
import scipy.fftpack
import math
from scipy import optimize
import uncertainties as unc
import uncertainties.unumpy as unp
import uncertainties.umath as umath
from scipy.odr import *
#from tqdm import tqdm
import matplotlib.pylab as pylab
import pathlib
import types
import inspect
# local imports
from smpl import functions
from smpl import io
from smpl.doc import  append_doc,append_str
from smpl import util
from smpl import wrap
from smpl import doc
from numpy.linalg import LinAlgError
      
unv=unp.nominal_values
usd=unp.std_devs

default = {   'params'        :[None      ,"Initial fit parameters",
  #],            'xaxis'         :[""        ,"X axis label",
  #],            'yaxis'         :[""        ,"Y axis label",
  #],            'label'         :[None      ,"Legend name of plotted ``data``",
  #],            'fmt'           :['.'       ,"Format for plotting fit function",
  #],           'units'         :[None      ,"Units of the fit parameters as strings. Displayed in the Legend",
  #],           'save'          :[None      ," File to save the plot",
  #],         'lpos'          :[0         ,"Legend position",
  ],           'frange'        :[None      ,"Limit the fit to given range. First integer is the lowest and second the highest index.",
  #],          'prange'        :[None      ,"Limit the plot of the fit to given range",
  #],         'sigmas'        :[0         ,"Color the array of given ``sigma`` times uncertaint",
  #],          'init'          :[True      ,"Initialize a new plot"
  #],          'ss'            :[True      ,"save, add legends and grid to the plot",
  #],          'also_data'     :[True      ," also plot the data"
  #],          'also_fit'      :[True      ,"also plot the fit",
  #],          'logy'          :[False     ,"logarithmic x axis",
  #],          'logx'          :[False     ,"logarithmic y axis",
  #],          'data_color'    :[None      , "Color of the data plot", 
  #],          'fit_color'     :[None      ,"Color of the fit plot",
  #],         'residue'       :[False     ,"Display difference between fit and data in a second plot",
  #],          'residue_err'   :[True      ,"Differences between fit and data will have errorbars",
  #],          'show'          :[False     ,"Call plt.show()",
  #],         'size'          :[None      ,"Size of the plot as a tuple (x,y)",
  #],          'number_format' :[ io.gf(4) ,"Format to display numbers.",
  ],            'selector'        :[ None     , "Function that takes ``x`` and ``y`` as parameters and returns an array mask in order to limit the data points for fitting. Alternatively a mask for selecting elements from datax and datay.",
  ],            'fixed_params'    :[ True     , "Enable fixing parameters by choosing the same-named variables from ``kwargs``.",
  ],            'sortbyx'         :[ True     , "Enable sorting the x and y data so that x is sorted.",
  ],            'maxfev'          :[ 10000    , "Maximum function evaluations during fitting.",
  ],            'epsfcn'          :[ 0.0001   , "Suitable step length for jacobian approximation.",
  ],            'xvar'            :[ None     , "Variable in fit function parameters that corresponds to the x axis. If it is None the last of the alphabetical sorted parameters is used.",
  #],          'interpolate'   :[ True     , "Enable interpolation of whole data if fit range is limited by ``frange`` or ``selector``.",
  #],          'bbox_to_anchor':[ None     , "Position in a tuple (x,y),Shift position of the legend out of the main pane. ",
  #],          'ncol'          :[ None     , "Columns in the legend if used with ``bbox_to_anchor``.",
  #],          'steps'         :[ 1000     ,"resolution of the plotted function" 
  ]          }

#@doc.insert_str("\tDefault kwargs\n\n\t")
@doc.append_str(doc.table(default))
@doc.append_str(doc.table({"fit_kwargs":["default","description"]}, bottom=False))
def fit_kwargs(kwargs):
    """
    Set default fit_kwargs if not set.
    """
    
    for k,v in default.items():
        if not k in kwargs:
            kwargs[k] = v[0]
    return kwargs


#@append_doc(default_kwargs)
def auto(datax,datay,funcs = None,**kwargs):
    """
    Automatically loop over functions and fit the best one.

    Parameters
    ==========
    funcs : function array
        functions to consider as fit. Default all ``smpl.functions``.
    **kwargs : optional
        see :func:`fit_kwargs`.

    Returns
    =======
    The best fit function and it's parameters and a ``lambda`` where the parameters are already applied to the function.

    """
    kwargs = fit_kwargs(kwargs)
    min_sq = None
    best_f = None
    best_ff = None
    

    
    if funcs is None:
        funcs = functions.__dict__.values()
    for f in funcs:
        if callable(f):
            #print(n)
            try:
                ff = fit(datax,datay,f,**kwargs)
                fy = f(datax,*ff)
            except (ValueError,LinAlgError) as ve:
                #print (ve)
                continue
            sum_sq = np.sum((fy - datay)**2) + np.sum((fy + usd(fy) - datay)**2) + np.sum((fy - usd(fy) - datay)**2)
            if min_sq is None or sum_sq < min_sq:
                min_sq = sum_sq
                best_f = f
                best_ff = ff
    #if not best_f is None:
    #    fit(datax,datay,best_f,**kwargs)
    return best_f,best_ff,lambda x : best_f(x,*best_ff)

def fit(datax,datay,function,**kwargs):
    """
    Returns a fit of ``function`` to ``datax`` and ``datay``. 

    Parameters
    ==========
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
    x,y,xerr,yerr =data_split(datax,datay,**kwargs)
    params = None
    if util.has('params',kwargs):
        params = kwargs['params']

    fixed = {}
    vnames = wrap.get_varnames(function,kwargs['xvar'])
    Ntot = len(vnames)-1
    if util.has("fixed_params",kwargs) and kwargs['fixed_params']:
        for i in range(1,len(vnames)):
            if util.has(vnames[i],kwargs):
                fixed[i] = kwargs[vnames[i]]
    # Count parameters for function
    if params is None:
        N=len(vnames)
        params = [1 for i in range(N-1)]
    tmp_params = []
    for i in range(len(params)):
        if not util.has(i+1,fixed):
            tmp_params += [params[i]]
    params = tmp_params
    N=len(params)
    Nfree = len(params)

    def tmp(*x):
        tmp_x = []
        j = 1
        #print(x)
        for i in range(1,Ntot+1):
            #print(i," ",j)
            if not util.has(i,fixed):
                tmp_x += [x[j]]
                #print(x[j])
                j = j+1
            else:
                tmp_x += [fixed[i]]
        
        #print(Ntot)
        #print(tmp_x)
        return unv(wrap.get_lambda(function,kwargs['xvar'])(x[0],*tmp_x))
    if xerr is not None:
        fit = _fit_odr(x,y,tmp,params=params,xerr=xerr,yerr=yerr)
    else:
        fit = _fit_curvefit(x,y,tmp,params=params,yerr=yerr)

    rfit = []
    j = 0
    for i in range(1,Ntot+1):
        if not util.has(i,fixed):
            rfit += [fit[j]]
            j = j+1
        else:
            rfit += [fixed[i]]

    return rfit
  

def data_split(datax,datay,**kwargs):
    """
    Splits datax and datay into (x,y,xerr,yerr).

    Parameters
    ==========
    **kwargs : optional
        see :func:`fit_kwargs`.
    """
    kwargs = fit_kwargs(kwargs)
    x,y,xerr,yerr = _data_split(datax,datay,**kwargs)
    if util.has('frange',kwargs):
        x =x[kwargs['frange'][0]:kwargs['frange'][1]]
        y =y[kwargs['frange'][0]:kwargs['frange'][1]]
        if not yerr is None:
            yerr =yerr[kwargs['frange'][0]:kwargs['frange'][1]]
        if not xerr is None:
            xerr =xerr[kwargs['frange'][0]:kwargs['frange'][1]]
    return x,y,xerr,yerr



# fittet ein dataset mit gegebenen x und y werten, eine funktion und ggf. anfangswerten und y-Fehler
# gibt die passenden parameter der funktion, sowie dessen unsicherheiten zurueck
#
# https://stackoverflow.com/questionsquestions/14581358/getting-standard-errors-on-fitted-parameters-using-the-optimize-leastsq-method-i#
# Updated on 4/6/2016
# User: https://stackoverflow.com/users/1476240/pedro-m-duarte
def _fit_curvefit(datax, datay, function, params=None, yerr=None, **kwargs):
    try:
        pfit, pcov = \
            optimize.curve_fit(function,datax,datay,p0=params,\
                            sigma=yerr, epsfcn=util.get("epsfcn",kwargs,0.0001), **kwargs, maxfev=util.get("maxfev",kwargs,10000))
    except RuntimeError as e:
        #print(e)
        return params
    error = []
    for i in range(len(pfit)):
        try:
          error.append(np.absolute(pcov[i][i])**0.5)
        except:
          error.append( 0.00 )
    pfit_curvefit = pfit
    perr_curvefit = np.array(error)
    #This was the old wrong way! Now use correct co. matrix through unc-package
    tmp = unp.uarray(pfit_curvefit, perr_curvefit)
    tmp2 =unc.correlated_values(pfit,pcov)
    return tmp2

def _fit_odr(datax,datay,function,params=None,yerr=None,xerr=None):
    model = Model(lambda p,x : function(x,*p))
    realdata = RealData(datax,datay,sy=yerr,sx=xerr)
    odr = ODR(realdata,model,beta0=params)
    out = odr.run()
    # This was the old wrong way! Now use correct co. matrix through unc-package!
    # Note Issues on scipy odr and curve_fit, regarding different definitions/namings of standard deviation or error and covaraince matrix
    # https://github.com/scipy/scipy/issues/6842
    # https://github.com/scipy/scipy/pull/12207
    # https://stackoverflow.com/questions/62460399/comparison-of-curve-fit-and-scipy-odr-absolute-sigma
    tmp = unp.uarray(out.beta,out.sd_beta)
    tmp2 = unc.correlated_values(out.beta,out.cov_beta)
    return tmp2

def __data_split(datax,datay,sortbyx=True):
    '''
    Split data + errors
    '''
    ind = np.argsort(unv(datax))
    x = unv(datax)[ind]
    y = unv(datay)[ind]
    xerr = usd(datax)[ind]
    yerr = usd(datay)[ind]
    xerr = xerr if np.any(np.abs(xerr)>0) else None
    yerr = yerr if np.any(np.abs(yerr)>0) else None
    return x,y,xerr,yerr

def _data_split(datax,datay,**kwargs):
    if util.has('selector',kwargs):
        sel = kwargs['selector']
        if callable(sel):
            return __data_split(datax[sel(datax,datay)],datay[sel(datax,datay)],kwargs['sortbyx'])
        else:
            return __data_split(datax[sel],datay[sel],kwargs['sortbyx'])
    if util.has("sortbyx", kwargs):
        return __data_split(datax,datay,kwargs['sortbyx'])
    else:
        return __data_split(datax,datay)

if __name__ == "__main__":
    import doctest
    doctest.testmod()