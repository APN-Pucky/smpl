import matplotlib.patches as mpatches
import numpy as np
import statistics as stat
import scipy as sci
import scipy.integrate as integrate
import scipy.fftpack
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.axes as axes
from matplotlib import colors as mcolors
import math
from scipy import optimize
import uncertainties as unc
import uncertainties.unumpy as unp
import uncertainties.umath as umath
import glob
import os
import matplotlib.pyplot as plt
from scipy.odr import *
import sympy
#from tqdm import tqdm
import matplotlib.pylab as pylab
import pathlib
import types
import inspect
# local imports
from smpl import functions
from smpl import io
from smpl import util
from smpl import wrap 
from smpl.doc import  append_doc,append_str
from smpl import doc
from smpl import fit as ffit
import inspect

def set_plot_style():
    #fig_size = (8, 6)
    #fig_legendsize = 14
    #fig_labelsize = 12 # ‘xx-small’, ‘x-small’, ‘small’, ‘medium’, ‘large’, ‘x-large’, ‘xx-large’.
    params = {'legend.fontsize': 'x-large',
              'figure.figsize': (8, 6),
             'axes.labelsize': 'x-large',
             'axes.titlesize':'x-large',
             'xtick.labelsize':'x-large',
             'ytick.labelsize':'x-large'}
    pylab.rcParams.update(params)
    matplotlib.rcParams.update(params)
    #matplotlib.rcParams.update({'font.size': fig_labelsize})
    #colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
      
unv=unp.nominal_values
usd=unp.std_devs

default = {
#    'params'        :[None      ,"Initial fit parameters",
              'xlabel'         :[""        ,"X axis label",
],            'ylabel'         :[""        ,"Y axis label",
],            'label'         :[None      ,"Legend name of plotted ``data``",
],            'fmt'           :['.'       ,"Format for plotting fit function",
 ],           'units'         :[None      ,"Units of the fit parameters as strings. Displayed in the Legend",
 ],           'save'          :[None      ," File to save the plot",
   ],         'lpos'          :[0         ,"Legend position",
# ],           'frange'        :[None      ,"Limit the fit to given range. First integer is the lowest and second the highest index.",
  ],          'prange'        :[None      ,"Limit the plot of the fit to given range",
   ],         'sigmas'        :[0         ,"Color the array of given ``sigma`` times uncertainty. Only works if the fit function is coded with ``unp``",
 ],           'init'          :[False     ,"Initialize a new plot"
  ],          'ss'            :[True      ,"save, add legends and grid to the plot",
  ],          'also_data'     :[True      ," also plot the data"
  ],          'also_fit'      :[True      ,"also plot the fit",
  ],          'logy'          :[False     ,"logarithmic x axis",
  ],          'logx'          :[False     ,"logarithmic y axis",
  ],          'data_color'    :[None      , "Color of the data plot", 
  ],          'fit_color'     :[None      ,"Color of the fit plot",
   ],         'residue'       :[False     ,"Display difference between fit and data in a second plot",
  ],          'residue_err'   :[True      ,"Differences between fit and data will have errorbars",
  ],          'show'          :[False     ,"Call plt.show()",
   ],         'size'          :[None      ,"Size of the plot as a tuple (x,y)",
  ],          'number_format' :[ io.gf(4) ,"Format to display numbers.",
#  ],          'selector'      :[ None     ,"Function that takes ``x`` and ``y`` as parameters and returns an array mask in order to limit the data points for fitting. Alternatively a mask for selecting elements from datax and datay.",
#  ],          'fixed_params'  :[ True     ,"Enable fixing parameters by choosing the same-named variables from ``kwargs``.",
#  ],          'sortbyx'       :[ True     , "Enable sorting the x and y data so that x is sorted.",
  ],          'interpolate'   :[ True     , "Enable interpolation of whole data if fit range is limited by ``frange`` or ``selector``.",
  ],          'bbox_to_anchor':[ None     , "Position in a tuple (x,y),Shift position of the legend out of the main pane. ",
  ],          'ncol'          :[ None     , "Columns in the legend if used with ``bbox_to_anchor``.",
  ],          'steps'         :[ 1000     ,"resolution of the plotted function",
  ],          'fitinline'     : [ False ,  "No newlines for each fit parameter",
  ],          }

#@doc.insert_str("\tDefault kwargs\n\n\t")
@doc.append_doc(ffit.fit_kwargs)
@doc.append_str(doc.table(default))
@doc.append_str(doc.table({"plot_kwargs":["default","description"]}, bottom=False))
def plot_kwargs(kwargs):
    """
    Set default plot_kwargs if not set.
    """
    kwargs = ffit.fit_kwargs(kwargs)
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
        see :func:`plot_kwargs`.

    Returns
    =======
    The best fit function and it's parameters. Also a lambda function where the parameters are already applied.



    """
    best_f,best_ff,lambda_f = ffit.auto(datax,datay,funcs,**kwargs)
    if not best_f is None:
        fit(datax,datay,best_f,**kwargs)
    return best_f,best_ff,lambda_f
  

#@append_doc(default_kwargs)
def fit(datax,datay,function,**kwargs):#params=None,xaxis="",yaxis="",label=None,fmt='.',units=None,save=None,lpos=0,frange=None,prange=None,sigmas=0,init=True,ss=True,also_data=True,also_fit=True,logy=False,logx=False,data_color=None, fit_color =None,residue=False,residue_err=True,show=False):
    """Fit and plot function to datax and datay.

    Parameters
    ==========
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
    =======
    array_like
        Optimized fit parameters of ``function`` to ``datax`` and ``datay``

    Examples
    ======== 

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
        plt_data(datax,datay,**kwargs)
    if kwargs['also_fit']:
        fit,kwargs['fit_color'] = plt_fit(datax,datay,function,**kwargs)#params,units,frange=frange,prange=prange,sigmas=sigmas,residue=residue,fig =fig,fit_color=fit_color)
    if kwargs['ss']:
        kwargs['oldshow'] = kwargs['show']
        kwargs['show'] = kwargs['show'] and not kwargs['residue']
        save_plot(**kwargs)
        kwargs['show'] = kwargs['oldshow']
    if kwargs['residue'] and fig is not None:
        plt_residue(datax,datay,function,fit,fig,**kwargs)#xaxis,yaxis,fit_color,save,residue_err,show=show)
    return fit

#@append_doc(default_kwargs)
def data(datax,datay,function=None,**kwargs):#params=None,xaxis="",yaxis="",label=None,fmt='.',units=None,save=None,lpos=0,frange=None,prange=None,sigmas=0,init=True,ss=True,also_data=True,also_fit=True,logy=False,logx=False,data_color=None,show=False):
    """Plot datay against datax via :func:`fit`

    Parameters
    ==========
    datax : array_like
        X data either as ``unp.uarray`` or ``np.array`` or ``list``
    datay : array_like
        Y data either as ``unp.uarray`` or ``np.array`` or ``list``
    function : func,optional
        Fit function with parameters: ``x``, ``params``
    **kwargs : optional
        see :func:`plot_kwargs`.
    Returns
    =======
    array_like
        Optimized fit parameters of ``function`` to ``datax`` and ``datay``
    """
    if not 'also_fit' in kwargs:
        kwargs['also_fit'] = False
    kwargs = plot_kwargs(kwargs)
    if kwargs['label']==None and kwargs['lpos']==0:
        kwargs['lpos'] = -1
    #return fit(datax,datay,function,params,xaxis,yaxis,label,fmt,units,save,lpos,frange,prange,sigmas,init,ss,also_data,also_fit=False,logy=logy,logx=logx,data_color =data_color,show=show)
    return fit(datax,datay,function,**kwargs)

def _plot(x,y,**kwargs):
    args = [x,y]
    kargs = {}
    if util.has('fmt',kwargs):
        args += [kwargs["fmt"]]
    if util.has('label',kwargs) and kwargs['label']!="":
        kargs['label'] = kwargs['label']
    if util.has('color',kwargs) and kwargs['color']!="":
        kargs['color'] = kwargs['color']
    plt.plot(*args,**kargs)
#@append_doc(default_kwargs)
def function(func,*args,**kwargs):
    """
    Plot function ``func`` between ``xmin`` and ``xmax``

    Parameters
    ==========
    func : function
        Function to be plotted between ``xmin`` and ``xmax``, only taking `array_like` ``x`` as parameter
    *args : optional
        arguments for ``func``
    **kwargs : optional
        see :func:`plot_kwargs`.
    """
    if not util.has("xmin",kwargs) or not util.has("xmin",kwargs):
        raise Exception("xmin or xmax missing.")

    if not util.has('lpos',kwargs) and not util.has('label',kwargs):
        kwargs['lpos'] =-1
    if not util.has('fmt',kwargs):
        kwargs['fmt'] ="-"

    kwargs = plot_kwargs(kwargs)
    xfit = np.linspace(kwargs['xmin'],kwargs['xmax'],kwargs['steps'])
    fig = init_plot(**kwargs)

    if not util.has("label",kwargs) or kwargs['label']is None:
        kwargs['label']=get_fnc_legend(func,args,**kwargs)
        kwargs['lpos'] =0
    _plot(xfit,func(xfit,*args),**kwargs)
    if kwargs['ss']:
        save_plot(**kwargs)


def plt_residue(datax,datay,gfunction,fit,fig,**kwargs):#xaxis="",yaxis="",fit_color=None,save = None,residue_err=True,show=False):
    function = wrap.get_lambda(gfunction,kwargs['xvar'])
    frame2=fig.add_axes((.1,.1,.8,.2))  
    kwargs['yaxis'] = "$\\Delta$" + kwargs['yaxis']
    kwargs['data_color'] = kwargs['fit_color']

    if kwargs['residue_err']:
        plt_data(datax,datay-function(datax,*fit),**kwargs)
    else:
        plt_data(unv(datax),unv(datay-function(datax,*fit)),**kwargs)
    kwargs['lpos'] = -1
    save_plot(**kwargs)


def data_split(datax,datay,**kwargs):
    return ffit.data_split(datax,datay,**kwargs)

def _fit(datax,datay,function,**kwargs):
    """
    Returns a fit like :func:`fit` but does no plotting.
    """
    return ffit.fit(datax,datay,function,**kwargs)

#@append_doc(plot_kwargs)
def plt_data(datax,datay,**kwargs):#xaxis="",yaxis="",label=None,fmt=None,data_color=None):
    """
        Plot datay vs datax
    """
    x,y,xerr,yerr = data_split(datax,datay)

    if  xerr is None and yerr is None :
        if kwargs['fmt'] is None:
            plt.plot(x,y, label=kwargs['label'],color=kwargs['data_color'])
        else:
            plt.plot(x,y, kwargs['fmt'], label=kwargs['label'],color=kwargs['data_color'])
    else:
        plt.errorbar(x,y,yerr=yerr,xerr=xerr,fmt=" ",capsize=5,label=kwargs['label'],color=kwargs['data_color'])
 
def get_fnc_legend(function,fit,**kwargs):
    if isinstance(function,str):
        l = "$" + sympy.latex(wrap.str_get_expr(function)) + "$"
    else:
        l = function.__name__
    #l = ""
    if l == "<lambda>":
        #l = "$\\lambda$(" +  ','.join(function.__code__.co_varnames) + ") = " #sympy.latex(eval(function.__code__.co_code))
        try:
            cc,li = inspect.findsource(function)
            f = ''.join(cc[li:]).split('lambda')[-1].split(':')[1].split(',')[0].replace("\n","")#.replace("#", "").replace("'''","")
            l = "$" + sympy.latex(wrap.str_get_expr(f)) + "$"
        except OSError:
            l = "$\\lambda$(" +  ','.join(function.__code__.co_varnames) + ")"
        
    if function.__doc__ is not None and not isinstance(function,str):
        l =  function.__doc__.split('\n')[0]
    vnames = wrap.get_varnames(function,kwargs['xvar'])
    for i in range(1,len(vnames)):
        l = l + ("\n" if not kwargs["fitinline"] or i==1 else " ")
        l = l + "$" + sympy.latex(sympy.symbols(str(vnames[i]))) + "$="
        if kwargs['units'] is not None and usd(fit[i-1])>0:
            l = l + "("
        if 'number_format' in kwargs:
            l = l +kwargs['number_format'].format(fit[i-1])
        else:
            l = l +"%s"%(fit[i-1])

        if kwargs['units'] is not None and usd(fit[i-1])>0:
            l = l + ")" 
        if kwargs['units'] is not None:
            l = l + " " +kwargs['units'][i-1]
    return l

#@append_doc(default_kwargs)
def plt_fit(datax,datay,gfunction,**kwargs):#p0=None,units=None,frange=None,prange=None,sigmas=1,residue=False, fig = None,fit_color=None):
    """
       Plot Fit 
    """
    function = wrap.get_lambda(gfunction,kwargs['xvar'])
    x,y,xerr,yerr =data_split(datax,datay,**kwargs)
    fit = _fit(datax,datay,gfunction,**kwargs)
    if kwargs['prange'] is None:
        xfit = np.linspace(np.min(unv(x)),np.max(unv(x)),1000)
    else:
        xfit = np.linspace(kwargs['prange'][0],kwargs['prange'][1],1000)
    l = get_fnc_legend(gfunction,fit,**kwargs)
    ll = None
    if kwargs['sigmas']>0:
        ll, = plt.plot(xfit,function(xfit,*unv(fit)),"-",color =kwargs['fit_color'])
        yfit = function(xfit,*fit)
        plt.fill_between(xfit, unv(yfit)-kwargs['sigmas']*usd(yfit),unv(yfit)+kwargs['sigmas']*usd(yfit),alpha=0.4,label=l,color = ll.get_color())    
    else:
        ll, = plt.plot(xfit,function(xfit,*unv(fit)),"-",label=l,color =kwargs['fit_color'])
    if (kwargs['frange'] is not None or kwargs['selector'] is not None) and util.true('interpolate',kwargs):
        xfit = np.linspace(np.min(unv(datax)),np.max(unv(datax)))
        plt.plot(xfit,unv(function(xfit,*fit)),"--",color=ll.get_color())
    return fit,ll.get_color()

def init_plot(**kwargs):#size=None,residue=False): #init
    #fig = plt.figure(figsize=fig_size)
    fig = None
    if kwargs['init'] or util.true("residue",kwargs):
        if kwargs['size'] is None:
            fig = plt.figure()
        else:
            fig = plt.figure(figsize=kwargs['size'])
        if kwargs['residue']:
            frame1=fig.add_axes((.1,.3,.8,.6))
        if util.has("xlabel",kwargs) and kwargs['xlabel'] != "":
            plt.xlabel(kwargs['xlabel'])
        if  util.has("ylabel",kwargs) and kwargs['ylabel'] != "":
            plt.ylabel(kwargs['ylabel'])
        if  util.has("xaxis",kwargs) and kwargs['xaxis'] != "":
            plt.xlabel(kwargs['xaxis'])
        if  util.has("yaxis",kwargs) and kwargs['yaxis'] != "":
            plt.ylabel(kwargs['yaxis'])
    return fig

def save_plot(**kwargs):#save=None,lpos=0,logy=False,logx=False,show=True): #save
    """
        save plot
    """
    if 'logy' in kwargs and kwargs['logy']:
        plt.gca().set_yscale('log')
    if 'logx' in kwargs and kwargs['logx']:
        plt.gca().set_xscale('log')
    plt.tight_layout()
    if 'lpos' in kwargs and kwargs['lpos']>=0:
        if(util.has('bbox_to_anchor', kwargs)):
            if(util.has('ncol', kwargs)):
                plt.legend(loc=kwargs['lpos'],bbox_to_anchor=kwargs['bbox_to_anchor'],ncol=kwargs['ncol'],borderaxespad=0)
            else:
                plt.legend(loc=kwargs['lpos'],bbox_to_anchor=kwargs['bbox_to_anchor'])
        else:
            plt.legend(loc=kwargs['lpos'])
    #plt.gca().set_xlim([kwargs['xmin'],kwargs['xmax']])
    #plt.gca().set_ylim([kwargs['ymin'],kwargs['ymax']])
    if 'save' in kwargs and not kwargs['save']==None:
        io.mkdirs(kwargs['save'])
        plt.savefig(kwargs['save'] +".pdf")
    plt.grid(b=True)
    if 'show' in kwargs and kwargs['show']:
        show(**kwargs)

def show(**kwargs):
    kwargs = plot_kwargs(kwargs)

    plt.grid(b=True)
    plt.show()


if __name__ == "__main__":
    import doctest
    doctest.testmod()