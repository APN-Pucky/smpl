#!/usr/bin/env python
# coding: utf-8

# # Interactive

# In[3]:


from smpl import animation
from smpl import plot
import matplotlib.pyplot as plt
import scipy
import numpy as np
import tqdm
import uncertainties as unc
from uncertainties import unumpy
from ipywidgets import widgets


# In[4]:


get_ipython().run_line_magic('matplotlib', 'notebook')
#plt.ioff()
import ipywidgets
def fta(n = 1.0):
    plot.function(lambda x : np.exp(n*np.log(x)-x),xmin = 0.1,xmax=100,tight=False,init=True)
    plot.function(lambda x : np.exp(n*np.log(n)-n-(x-n)**2/2/n),xmin = 0.1,xmax=100,tight=False,init=False)
    fac = np.math.factorial(n)
    sti = np.sqrt(2* np.pi* n) *  n**n *np.exp(-n) 
    print("FAKULTÄT("+str(n)+") = " + str(fac))
    print("STIRLING("+str(n)+") = " +  str(sti))
    print("REL-DIFF(" + str(n)+") = "+ str((sti-fac)/fac*100) + "%")
    
ipywidgets.interactive(fta,  n=widgets.IntSlider(min=1, max=130, step=1, value=1)) 


# In[3]:


# Approximate factorial by gamma
def fac(n):
    return scipy.special.gamma(n+1)

plot.function(lambda n : (fac(n)-np.sqrt(2* np.pi* n) *  n**n *np.exp(-n))/fac(n) *100 ,xmin = 1,xmax=140,xlabel="N", ylabel="Rel. diff. between factorial und stirling [%]",label="",logy=True,tight=False,init=True)
    


# In[ ]:




