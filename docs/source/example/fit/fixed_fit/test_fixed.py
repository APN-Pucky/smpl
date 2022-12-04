#!/usr/bin/env python
# coding: utf-8

# # Fixed Fit

# In[1]:


import numpy as np
from smpl import plot
from smpl import io
from smpl import functions as f
import uncertainties.unumpy as unp
import uncertainties as un
import smpl
smpl.__version__


# In[2]:


data = np.loadtxt(io.find_file('test_linear_data.txt',3))
xdata = data[:,0]
xerr = data[:,2]
ydata = data[:,1]
yerr = data[:,3]
x = unp.uarray(xdata,xerr)
y = unp.uarray(ydata,yerr)


# In[3]:


data


# In[4]:


ff = plot.fit(xdata, ydata, fmt='.', label='data', xaxis="x in a.u.",yaxis="y in a.u.",function=f.line, b=0)


# In[5]:


ff = plot.fit(xdata, ydata, fmt='.', label='data', xaxis="x in a.u.",yaxis="y in a.u.",function=f.line, a=un.ufloat(1,0.1),sigmas=1)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




