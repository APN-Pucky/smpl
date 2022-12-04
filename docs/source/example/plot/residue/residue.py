#!/usr/bin/env python
# coding: utf-8

# # Residue Plot

# In[1]:


from smpl import plot
from smpl import io
from smpl import functions as f
import numpy as np
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt


# In[2]:


dat = np.loadtxt(io.find_file("dat.dat",3), skiprows=0, delimiter=" ")


xdata = dat[:,0]
ydata = dat[:,1]
ymodel = dat[:,-2]


# In[3]:


plot.data(xdata,ydata,logy=True,ss=False)
plot.data(xdata,ymodel,fmt="-",logy=True,init=False,label="model")


# In[ ]:





# In[4]:


data = np.loadtxt(io.find_file('test_linear_data.txt',3))
xdata = data[:,0]
xerr = data[:,2]
ydata = data[:,1]
yerr = data[:,3]
x = unp.uarray(xdata,xerr)
y = unp.uarray(ydata,yerr)


# In[5]:


plot.fit(x,y,function=f.line,residue=True,xaxis="t",yaxis="s",units=["l","b"],sigmas=1)


# In[6]:


plot.fit(x,y,function=f.line,residue=True,xaxis="t",yaxis="s",units=["l","b"],sigmas=1,residue_err=False)

