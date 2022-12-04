#!/usr/bin/env python
# coding: utf-8

# # Custom Fit

# In[1]:


import numpy as np
from smpl import plot
from smpl import io
from smpl import functions as f
import uncertainties.unumpy as unp


# In[2]:


data = data_malus = np.loadtxt(io.find_file("test_custom_data.csv",3),skiprows = 1, delimiter=',')
ydata = unp.uarray(data[:,0],data[:,1])
xdata = unp.uarray(data[:,2],data[:,3])
plot.data(xdata,ydata)


# ## Initial guess
# params allows to set initial guess values for fitting.

# In[3]:


def Malus(x,I_max,I_min,w,p):
    ''' $(I_{max}-I_{min})*\\cos(w*x-p)^2+I_{min} $'''
    return (I_max-I_min)*unp.cos(w*x-p)**2+I_min

plot.fit((xdata),ydata,Malus,xaxis="anlge in °", yaxis="intensity in a.u.", params=[4.6,0.11,0.0175,180+90-137], units=["a.u.","a.u.","rad$^{-1}$","rad"])

