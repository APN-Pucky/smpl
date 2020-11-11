import matplotlib.patches as mpatches
import numpy as np
import statistics as stat
import scipy as sci
import scipy.integrate as integrate
import scipy.fftpack
import sympy as sym
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

def data(datax,datay,function=None,p0=None,axis=("",""),label=None,fmt=None,units=None,save=None,lpos=0,frange=None,prange=None,sigmas=1,init=True,ss=True,also_data=True,also_fit=True,logy=False,logx=False):
    """
    Plot datay vs datax
    """
    return fit(datax,datay,function,p0,axis,label,fmt,units,save,lpos,frange,prange,sigmas,init,ss,also_data,also_fit=False,logy=logy,logx=logx)

def fit(datax,datay,function,params=None,axis=("",""),label=None,fmt=None,units=None,save=None,lpos=0,frange=None,prange=None,sigmas=1,init=True,ss=True,also_data=True,also_fit=True,logy=False,logx=False):
    """
        Fit and plot function to datax and datay.
        ...
        TODO more info
    """
    #x,y,xerr,yerr = data_split(datax,datay)
    fit = None
    if label==None and lpos==0:
        lpos = -1
    if init:
        init_plot()
    if also_data:
        plt_data(datax,datay,axis,label,fmt)
    if also_fit:
        fit = plt_fit(datax,datay,function,params,units,frange=frange,prange=prange,sigmas=sigmas)
    if ss:
        save_plot(save,lpos,logy,logx)
    return fit
def _function(func,start,end,steps=1000,label=""):
    xfit = np.linspace(start,end,steps)
    if label != "":
        plt.plot(xfit,func(xfit),label=label)
    else:
        plt.plot(xfit,func(xfit))


show_=False
def show():
    if show_:
        plt.show()

# fittet ein dataset mit gegebenen x und y werten, eine funktion und ggf. anfangswerten und y-Fehler
# gibt die passenden parameter der funktion, sowie dessen unsicherheiten zurueck
#
# https://stackoverflow.com/questions/14581358/getting-standard-errors-on-fitted-parameters-using-the-optimize-leastsq-method-i#
# Updated on 4/6/2016
# User: https://stackoverflow.com/users/1476240/pedro-m-duarte
def fit_curvefit(datax, datay, function, p0=None, yerr=None, **kwargs):
    pfit, pcov = \
         optimize.curve_fit(function,datax,datay,p0=p0,\
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

def fit_curve(datax,datay,function,p0=None,yerr=None,xerr=None):
    model = Model(lambda p,x : function(x,*p))
    realdata = RealData(datax,datay,sy=yerr,sx=xerr)
    odr = ODR(realdata,model,beta0=p0)
    out = odr.run()
    return unp.uarray(out.beta,out.sd_beta)

def _data_split(datax,datay):
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
 
def _fit(datax,datay,function,p0=None,frange=None):
    x,y,xerr,yerr =data_split(datax,datay,frange)
    def tmp(*x):
        return unv(function(*x))
    if xerr is not None:
        fit = fit_curve(x,y,tmp,p0=p0,xerr=xerr,yerr=yerr)
    else:
        fit = fit_curvefit(x,y,tmp,p0=p0,yerr=yerr)
    return fit
def plt_data(datax,datay,axis=("",""),label=None,fmt=None):
    """
        Plot datay vs datax
        ...
        TODO more info
    """
    x,y,xerr,yerr = data_split(datax,datay)
    if axis[0] != "":
        plt.xlabel(axis[0])
    if axis[1] != "":
        plt.ylabel(axis[1])
    if  xerr is None and yerr is None :
        if fmt is None:
            plt.plot(x,y, label=label)
        else:
            plt.plot(x,y, fmt, label=label)
    else:
        plt.errorbar(x,y,yerr=yerr,xerr=xerr,fmt=" ",capsize=5,label=label)
 
def plt_fit(datax,datay,function,p0=None,units=None,frange=None,prange=None,sigmas=1):
    """
        
    """
    x,y,xerr,yerr =data_split(datax,datay,frange)
    fit = _fit(datax,datay,function,p0,frange)
    if prange is None:
        xfit = np.linspace(unv(x[0]),unv(x[-1]),1000)
    else:
        xfit = np.linspace(prange[0],prange[1],1000)
    l = function.__name__ + ": f(x)=" + function.__doc__
    for i in range(1,len(function.__code__.co_varnames)):
        l = l + "\n"
        l = l + str(function.__code__.co_varnames[i]) + "=%s"%(fit[i-1])
        if units is not None:
            l = l + " " + units[i-1]
    if sigmas>0:
        ll, = plt.plot(xfit,function(xfit,*unv(fit)),"-")
        yfit = function(xfit,*fit)
        plt.fill_between(xfit, unv(yfit)-sigmas*usd(yfit),unv(yfit)+sigmas*usd(yfit),alpha=0.4,label=l,color = ll.get_color())    
    else:
        l, = plt.plot(xfit,function(xfit,*unv(fit)),"-",label=l)
        if frange is not None:
            xfit = np.linspace(unv(datax[0]),unv(datax[-1]))
            plt.plot(xfit,unv(function(xfit,*fit)),"--",color=l.get_color())
    return fit

def init_plot(size=None): #init
    #fig = plt.figure(figsize=fig_size)
    if size==None:
        fig = plt.figure()
    else:
        fig = plt.figure(figsize=size)
def save_plot(save=None,lpos=0,logy=False,logx=False): #save
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
    show()
    #plt.show()
# usage zB:
# pfit, perr = fit_curvefit(unv(xdata), unv(ydata), gerade, yerr = usd(ydata), p0 = [1, 0])
# fuer eine gerade mit anfangswerten m = 1, b = 0


