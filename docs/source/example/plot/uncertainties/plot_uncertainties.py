#!/usr/bin/env python
# coding: utf-8

# # Uncertainties

# In[1]:


import smpl
from smpl import plot
from smpl import io
from smpl import functions as f
import numpy as np
np.random.seed(1337)
print(smpl.__version__)


# In[2]:


import uncertainties.unumpy as unp
data = np.loadtxt(io.find_file('test_linear_data.txt',3))
xdata = data[:,0]
xerr = data[:,2]
ydata = data[:,1]
yerr = data[:,3]
x = unp.uarray(xdata,xerr)
y = unp.uarray(ydata,yerr)


# In[3]:


plot.data(x,y,label="data",fmt=None)
plot.data(x,y,label="data",fmt="step",init=True)
plot.data(x,y,label="data",fmt="hist",init=True)


# In[4]:


plot.data(plot.unv(x),plot.unv(y),label="data",fmt="hist")


# In[6]:


x= np.random.randn(1000)
print(isinstance(x, (list, tuple, np.ndarray)))
plot.data(x,bins=20,label="data",fmt=None)
plot.data(x,bins=20,label="data",fmt="step",init=True)


# Visually increased uncertainties by the scaling given by data_sigmas.

# In[8]:


plot.data(x,bins=20,data_sigmas=5,label="data",fmt=None)
plot.data(x,bins=20,data_sigmas=5,label="data",fmt="step",init=True)


# In[ ]:




