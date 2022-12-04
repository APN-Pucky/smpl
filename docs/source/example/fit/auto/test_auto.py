#!/usr/bin/env python
# coding: utf-8

# # Auto Fit

# In[1]:


import numpy as np
from smpl import plot
from smpl import stat
from smpl import io
from smpl import functions as f
import uncertainties.unumpy as unp
import smpl


# In[2]:


for n in ['test_linear_data.txt', 'test_quad_data.txt']:
    data = np.loadtxt(io.find_file(n,3))
    xdata = data[:,0]
    xerr = data[:,2]
    ydata = data[:,1]
    yerr = data[:,3]
    x = unp.uarray(xdata,xerr)
    y = unp.uarray(ydata,yerr)


    function,fitparams,lfunc = plot.auto(xdata, ydata, fmt='.', label='data', xaxis="x in a.u.",yaxis="y in a.u.",sigmas=1,epsfcn=0.00001,maxfev=1000000,init=True)


# In[ ]:





# In[3]:


x= np.linspace(-5,5,100)
y = stat.noisy(np.exp(2*x))
ff = plot.auto(x, y, fmt='.', label='data', xaxis="x in a.u.",yaxis="y in a.u.",sigmas=1)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




