#!/usr/bin/env python
# coding: utf-8

# # SubPlotInteractive

# In[1]:


from smpl import animation
from smpl import plot
import matplotlib.pyplot as plt
import scipy
import numpy as np
import tqdm
import uncertainties as unc
from uncertainties import unumpy
from ipywidgets import widgets
from sympy import binomial


# In[2]:


get_ipython().run_line_magic('matplotlib', 'notebook')
#plt.ioff()
import ipywidgets

def fac(n):
    return scipy.special.gamma(n+1)

def fta(N_tot = 1.0,p=1.0):
    fig, axs = plot.subplots(2, 1,  sharex=True)
    fig.subplots_adjust(hspace=0)
    n_bar = N_tot*p
    bina = lambda n: fac(N_tot)/(fac(n)*fac(N_tot-n))*p**n*(1.-p)**(N_tot-n)
    gaus = lambda n: np.sqrt(N_tot/(2*np.pi*(n_bar)*(N_tot-n_bar)))*np.exp(-(n-n_bar)**2/2*N_tot/(n_bar*(N_tot-n_bar)))
    poisson  =  lambda n : n_bar**n*np.exp(-n_bar)/fac(n)
    plot.function(bina,label="binomial",axes=axs[0],tight=False,xmin=0,xmax=N_tot)
    plot.function(gaus,label="gauss",axes=axs[0],tight=False,xmin=0,xmax=N_tot)
    plot.function(poisson,label="poisson",axes=axs[0],tight=False,xmin=0,xmax=N_tot)
    plot.function(lambda n: (bina(n)-gaus(n)),label="diff binomial to gauss",axes=axs[1],tight=False,xmin=0,xmax=N_tot)
    plot.function(lambda n: (bina(n)-poisson(n)),label="diff binomial to poisson",axes=axs[1],tight=False,xmin=0,xmax=N_tot)
    
    #plot.function(lambda n: N_tot*n**5,axes=axs[1],tight=False,xmin=0,xmax=1)
    
ipywidgets.interactive(fta,  N_tot=widgets.IntSlider(min=1, max=100, step=1, value=1),  p=widgets.FloatSlider(min=0, max=1, step=0.01, value=0.1)) 


# In[ ]:




