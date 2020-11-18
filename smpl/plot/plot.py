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
from smpl.doc import  add_doc
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


def kwargslist() :
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
        Limit the fit to given range
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
    """
    return {} 

@add_doc(kwargslist)
def fit(datax,datay,function,params=None,xaxis="",yaxis="",label=None,fmt='.',units=None,save=None,lpos=0,frange=None,prange=None,sigmas=0,init=True,ss=True,also_data=True,also_fit=True,logy=False,logx=False,data_color=None, fit_color =None,residue=False,residue_err=True,show=False):
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
    >>> from smpl import functions as f
    >>> unv(fit([0,1,2,3],[0,1,2,3],f.Line)).round()[0]
    1.0
    """
    fit = None
    fig = None
    if init:
        fig = init_plot(residue=residue)
    if also_data:
        plt_data(datax,datay,xaxis,yaxis,label,fmt,data_color=data_color)
    if also_fit:
        fit,fit_color = plt_fit(datax,datay,function,params,units,frange=frange,prange=prange,sigmas=sigmas,residue=residue,fig =fig,fit_color=fit_color)
    if ss:
        save_plot(save,lpos,logy,logx,show=show and not residue)
    if residue and fig is not None:
        plt_residue(datax,datay,function,fit,fig,xaxis,yaxis,fit_color,save,residue_err,show=show)
    return fit

@add_doc(kwargslist)
def data(datax,datay,function=None,params=None,xaxis="",yaxis="",label=None,fmt='.',units=None,save=None,lpos=0,frange=None,prange=None,sigmas=0,init=True,ss=True,also_data=True,also_fit=True,logy=False,logx=False,data_color=None,show=False):
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
    if label==None and lpos==0:
        lpos = -1

    return fit(datax,datay,function,params,xaxis,yaxis,label,fmt,units,save,lpos,frange,prange,sigmas,init,ss,also_data,also_fit=False,logy=logy,logx=logx,data_color =data_color,show=show)


def function(func,start,end,steps=1000,label=""):
    """
    Plot function ``func`` between ``start`` and ``end``

    Parameters
    ==========
    func : function
        Function to be plotted between ``start`` and ``end``, only taking `array_like` ``x`` as parameter
    start : float
        lowest ``x``
    end : float
        highest ``x``
    steps : int
        resolution of the plotted function
    label : str
        Legend name of the function

    """
    xfit = np.linspace(start,end,steps)
    if label != "":
        plt.plot(xfit,func(xfit),label=label)
    else:
        plt.plot(xfit,func(xfit))

def plt_residue(datax,datay,function,fit,fig,xaxis="",yaxis="",fit_color=None,save = None,residue_err=True,show=False):
    frame2=fig.add_axes((.1,.1,.8,.2))  
    if residue_err:
        plt_data(datax,datay-function(datax,*fit),xaxis=xaxis,yaxis = "$\Delta$" + yaxis, data_color=fit_color)
    else:
        plt_data(unv(datax),unv(datay-function(datax,*fit)),xaxis=xaxis,yaxis = "$\Delta$" + yaxis, data_color=fit_color)
    save_plot(save,-1,show=show)



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
def data_split(datax,datay,frange=None):
    if frange is not None:
        return _data_split(datax[frange[0]:frange[1]],datay[frange[0]:frange[1]])
    else:
        return _data_split(datax,datay)
def _fit(datax,datay,function,params=None,frange=None):
    x,y,xerr,yerr =data_split(datax,datay,frange)
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

def plt_data(datax,datay,xaxis="",yaxis="",label=None,fmt=None,data_color=None):
    """
        Plot datay vs datax
        ...
        TODO more info
    """
    x,y,xerr,yerr = data_split(datax,datay)
    if xaxis != "":
        plt.xlabel(xaxis)
    if yaxis != "":
        plt.ylabel(yaxis)
    if  xerr is None and yerr is None :
        if fmt is None:
            plt.plot(x,y, label=label,color =data_color)
        else:
            plt.plot(x,y, fmt, label=label,color =data_color)
    else:
        plt.errorbar(x,y,yerr=yerr,xerr=xerr,fmt=" ",capsize=5,label=label,color =data_color)
 
def plt_fit(datax,datay,function,p0=None,units=None,frange=None,prange=None,sigmas=1,residue=False, fig = None,fit_color=None):
    """
        
    """
    x,y,xerr,yerr =data_split(datax,datay,frange)
    fit = _fit(datax,datay,function,p0,frange)
    if prange is None:
        xfit = np.linspace(unv(x[0]),unv(x[-1]),1000)
    else:
        xfit = np.linspace(prange[0],prange[1],1000)
    l = function.__name__
    if function.__doc__ is not None:
        l = l + ": f(x)=" + function.__doc__
    for i in range(1,len(function.__code__.co_varnames)):
        l = l + "\n"
        l = l + "" + str(function.__code__.co_varnames[i]) + "="
        if units is not None:
            l = l + "("
        l = l +"%s"%(fit[i-1])
        if units is not None:
            l = l + ") " + units[i-1]
    ll = None
    if sigmas>0:
        ll, = plt.plot(xfit,function(xfit,*unv(fit)),"-",color =fit_color)
        yfit = function(xfit,*fit)
        plt.fill_between(xfit, unv(yfit)-sigmas*usd(yfit),unv(yfit)+sigmas*usd(yfit),alpha=0.4,label=l,color = ll.get_color())    
    else:
        ll, = plt.plot(xfit,function(xfit,*unv(fit)),"-",label=l,color =fit_color)
        if frange is not None:
            xfit = np.linspace(unv(datax[0]),unv(datax[-1]))
            plt.plot(xfit,unv(function(xfit,*fit)),"--",color=ll.get_color())
    return fit,ll.get_color()

def init_plot(size=None,residue=False): #init
    #fig = plt.figure(figsize=fig_size)
    if size==None:
        fig = plt.figure()
    else:
        fig = plt.figure(figsize=size)
    if residue:
        frame1=fig.add_axes((.1,.3,.8,.6))
    return fig
def save_plot(save=None,lpos=0,logy=False,logx=False,show=True): #save
    """
        save plot
    """
    if logy:
        plt.gca().set_yscale('log')
    if logx:
        plt.gca().set_xscale('log')
    plt.tight_layout()
    if lpos>=0:
        plt.legend(loc=lpos)
    plt.grid()
    if not save==None:
        mkdirs(save)
        plt.savefig(save +".pdf")
    if show:
        plt.show()
    #plt.show()
# usage zB:
# pfit, perr = fit_curvefit(unv(xdata), unv(ydata), gerade, yerr = usd(ydata), p0 = [1, 0])
# fuer eine gerade mit anfangswerten m = 1, b = 0


if __name__ == "__main__":
    import doctest
    doctest.testmod()