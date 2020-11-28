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
from tqdm import tqdm
import matplotlib.pylab as pylab
import pathlib
import types
import inspect
# local imports
from smpl import functions
from smpl import io
from smpl import util
from smpl.doc import  append
#TODO create folders for file saves

fig_size = (8, 6)
fig_legendsize = 14
fig_labelsize = 12 # ‘xx-small’, ‘x-small’, ‘small’, ‘medium’, ‘large’, ‘x-large’, ‘xx-large’.
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (8, 6),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)
matplotlib.rcParams.update(params)
#matplotlib.rcParams.update({'font.size': fig_labelsize})

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
      
unv=unp.nominal_values
usd=unp.std_devs


def default_kwargs(kwargs) :
    """
    Other Parameters
    ================
    params : array_like
        Initial fit parameters
    xaxis : str
        X axis label
    yaxis : str
        Y axis label
    label : str
        Legend name of plotted ``data``
    fmt : str
        Format for plotting fit function
    units : array
        Units of the fit parameters as strings. Displayed in the Legend
    save : str
        File to save the plot
    lpos: int
        Legend position
    frange : array
        Limit the fit to given range. First integer is the lowest and second the highest index.
    prange : array
        Limit the plot of the fit to given range
    sigmas : int
        Color the array of given ``sigma`` times uncertainty
    init : bool
        Initialize a new plot
    ss : bool
        save, add legends and grid to the plot
    also_data: bool
        also plot the data
    also_fit : bool
        also plot the fit
    logy : bool
        logarithmic y axis
    logx : bool
        logarithmic x axis
    data_color : str
        Color of the data plot
    fit_color : str
        Color of the fit plot
    residue : bool
        Display difference between fit and data in a second plot 
    residue_err : bool
        Differences between fit and data will have errorbars
    show : bool
        Call plt.show()
    number_format : str
        Format to display numbers.
    selector : func
        Function that takes ``x`` and ``y`` as parameters and returns an array mask in order to limit the data points for fitting.
    steps : int
        resolution of the plotted function
    

    """
    default = {'params':None,
            'xaxis':"",
            'yaxis':"",
            'label':None,
            'fmt':'.',
            'units':None,
            'save':None,
            'lpos':0,
            'frange':None,
            'prange':None,
            'sigmas':0,
            'init':True,
            'ss':True,
            'also_data':True,
            'also_fit':True,
            'logy':False,
            'logx':False,
            'data_color':None, 
            'fit_color' :None,
            'residue':False,
            'residue_err':True,
            'show':False,
            'size':None,
            'number_format': io.gf(4),
            'selector' : None,
            'steps' : 1000
            }
    for k,v in default.items():
        if not k in kwargs:
            kwargs[k] = v
    return kwargs

  

@append(default_kwargs)
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
    kwargs = default_kwargs(kwargs)
    fit = None
    fig = None
    if kwargs['init']:
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

@append(default_kwargs)
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

    Returns
    =======
    array_like
        Optimized fit parameters of ``function`` to ``datax`` and ``datay``
    """
    if not 'also_fit' in kwargs:
        kwargs['also_fit'] = False
    kwargs = default_kwargs(kwargs)
    if kwargs['label']==None and kwargs['lpos']==0:
        kwargs['lpos'] = -1
    #return fit(datax,datay,function,params,xaxis,yaxis,label,fmt,units,save,lpos,frange,prange,sigmas,init,ss,also_data,also_fit=False,logy=logy,logx=logx,data_color =data_color,show=show)
    return fit(datax,datay,function,**kwargs)

@append(default_kwargs)
def function(func,*args,**kwargs):
    """
    Plot function ``func`` between ``xmin`` and ``xmax``

    Parameters
    ==========
    func : function
        Function to be plotted between ``start`` and ``end``, only taking `array_like` ``x`` as parameter
    start : float
        lowest ``x``
    end : float
        highest ``x``

    """
    if not 'lpos' in kwargs:
        kwargs['lpos'] =-1
    kwargs = default_kwargs(kwargs)
    xfit = np.linspace(kwargs['xmin'],kwargs['xmax'],kwargs['steps'])
    if kwargs['init']:
        fig = init_plot(**kwargs)
    if kwargs['xaxis'] != "":
        plt.xlabel(kwargs['xaxis'])
    if kwargs['xaxis'] != "":
        plt.ylabel(kwargs['yaxis'])
    if kwargs['label'] != "":
        plt.plot(xfit,func(xfit,*args),label=kwargs['label'])
    else:
        plt.plot(xfit,func(xfit,*args))
    if kwargs['ss']:
        save_plot(**kwargs)


def plt_residue(datax,datay,function,fit,fig,**kwargs):#xaxis="",yaxis="",fit_color=None,save = None,residue_err=True,show=False):
    frame2=fig.add_axes((.1,.1,.8,.2))  
    kwargs['yaxis'] = "$\Delta$" + kwargs['yaxis']
    kwargs['data_color'] = kwargs['fit_color']

    if kwargs['residue_err']:
        plt_data(datax,datay-function(datax,*fit),**kwargs)
    else:
        plt_data(unv(datax),unv(datay-function(datax,*fit)),**kwargs)
    kwargs['lpos'] = -1
    save_plot(**kwargs)



# fittet ein dataset mit gegebenen x und y werten, eine funktion und ggf. anfangswerten und y-Fehler
# gibt die passenden parameter der funktion, sowie dessen unsicherheiten zurueck
#
# https://stackoverflow.com/questions/14581358/getting-standard-errors-on-fitted-parameters-using-the-optimize-leastsq-method-i#
# Updated on 4/6/2016
# User: https://stackoverflow.com/users/1476240/pedro-m-duarte
def fit_curvefit(datax, datay, function, params=None, yerr=None, **kwargs):
    pfit, pcov = \
         optimize.curve_fit(function,datax,datay,p0=params,\
                            sigma=yerr, epsfcn=0.0001, **kwargs, maxfev=1000000)
    error = []
    for i in range(len(pfit)):
        try:
          error.append(np.absolute(pcov[i][i])**0.5)
        except:
          error.append( 0.00 )
    pfit_curvefit = pfit
    perr_curvefit = np.array(error)
    return unp.uarray(pfit_curvefit, perr_curvefit)

def fit_curve(datax,datay,function,params=None,yerr=None,xerr=None):
    model = Model(lambda p,x : function(x,*p))
    realdata = RealData(datax,datay,sy=yerr,sx=xerr)
    odr = ODR(realdata,model,beta0=params)
    out = odr.run()
    return unp.uarray(out.beta,out.sd_beta)

def _data_split(datax,datay):
    '''
    Split data + errors
    '''
    x = unv(datax)
    y = unv(datay)
    xerr = usd(datax)
    yerr = usd(datay)
    xerr = xerr if np.any(np.abs(xerr)>0) else None
    yerr = yerr if np.any(np.abs(yerr)>0) else None
    return x,y,xerr,yerr
def data_split(datax,datay,**kwargs):
    if util.has('selector',kwargs):
        sel = kwargs['selector']
        return _data_split(datax[sel(datax,datay)],datay[sel(datax,datay)])
    if util.has('frange',kwargs):
        return _data_split(datax[kwargs['frange'][0]:kwargs['frange'][1]],datay[kwargs['frange'][0]:kwargs['frange'][1]])
    else:
        return _data_split(datax,datay)
def _fit(datax,datay,function,**kwargs):
    x,y,xerr,yerr =data_split(datax,datay,**kwargs)
    params = kwargs['params']
    # Count parameters for function
    if params is None:
        N=function.__code__.co_argcount
        params = [1 for i in range(N-1)]
    def tmp(*x):
        return unv(function(*x))
    if xerr is not None:
        fit = fit_curve(x,y,tmp,params=params,xerr=xerr,yerr=yerr)
    else:
        fit = fit_curvefit(x,y,tmp,params=params,yerr=yerr)
    return fit

@append(default_kwargs)
def plt_data(datax,datay,**kwargs):#xaxis="",yaxis="",label=None,fmt=None,data_color=None):
    """
        Plot datay vs datax
    """
    x,y,xerr,yerr = data_split(datax,datay)
    if kwargs['xaxis'] != "":
        plt.xlabel(kwargs['xaxis'])
    if kwargs['xaxis'] != "":
        plt.ylabel(kwargs['yaxis'])
    if  xerr is None and yerr is None :
        if kwargs['fmt'] is None:
            plt.plot(x,y, label=kwargs['label'],color=kwargs['data_color'])
        else:
            plt.plot(x,y, kwargs['fmt'], label=kwargs['label'],color=kwargs['data_color'])
    else:
        plt.errorbar(x,y,yerr=yerr,xerr=xerr,fmt=" ",capsize=5,label=kwargs['label'],color=kwargs['data_color'])
 
@append(default_kwargs)
def plt_fit(datax,datay,function,**kwargs):#p0=None,units=None,frange=None,prange=None,sigmas=1,residue=False, fig = None,fit_color=None):
    """
       Plot Fit 
    """
    x,y,xerr,yerr =data_split(datax,datay,**kwargs)
    fit = _fit(datax,datay,function,**kwargs)
    if kwargs['prange'] is None:
        xfit = np.linspace(unv(x[0]),unv(x[-1]),1000)
    else:
        xfit = np.linspace(kwargs['prange'][0],kwargs['prange'][1],1000)
    #l = function.__name__
    if function.__doc__ is not None:
        l = function.__doc__
    for i in range(1,len(function.__code__.co_varnames)):
        l = l + "\n"
        l = l + "" + str(function.__code__.co_varnames[i]) + "="
        if kwargs['units'] is not None:
            l = l + "("
        if 'number_format' in kwargs:
            l = l +kwargs['number_format'].format(fit[i-1])
        else:
            l = l +"%s"%(fit[i-1])

        if kwargs['units'] is not None:
            l = l + ") " + kwargs['units'][i-1]
    ll = None
    if kwargs['sigmas']>0:
        ll, = plt.plot(xfit,function(xfit,*unv(fit)),"-",color =kwargs['fit_color'])
        yfit = function(xfit,*fit)
        plt.fill_between(xfit, unv(yfit)-kwargs['sigmas']*usd(yfit),unv(yfit)+kwargs['sigmas']*usd(yfit),alpha=0.4,label=l,color = ll.get_color())    
    else:
        ll, = plt.plot(xfit,function(xfit,*unv(fit)),"-",label=l,color =kwargs['fit_color'])
        if kwargs['frange'] is not None:
            xfit = np.linspace(unv(datax[0]),unv(datax[-1]))
            plt.plot(xfit,unv(function(xfit,*fit)),"--",color=ll.get_color())
    return fit,ll.get_color()

def init_plot(**kwargs):#size=None,residue=False): #init
    #fig = plt.figure(figsize=fig_size)
    if kwargs['size']==None:
        fig = plt.figure()
    else:
        fig = plt.figure(figsize=kwargs['size'])
    if kwargs['residue']:
        frame1=fig.add_axes((.1,.3,.8,.6))
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
        plt.legend(loc=kwargs['lpos'])
    if 'save' in kwargs and not kwargs['save']==None:
        mkdirs(kwargs['save'])
        plt.savefig(kwargs['save'] +".pdf")
    plt.grid()
    if 'show' in kwargs and kwargs['show']:
        show(**kwargs)

def show(**kwargs):
    plt.grid()
    plt.show()
# usage zB:
# pfit, perr = fit_curvefit(unv(xdata), unv(ydata), gerade, yerr = usd(ydata), p0 = [1, 0])
# fuer eine gerade mit anfangswerten m = 1, b = 0


if __name__ == "__main__":
    import doctest
    doctest.testmod()