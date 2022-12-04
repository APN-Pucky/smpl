#!/usr/bin/env python
# coding: utf-8

# # Linear Fit

# In[1]:


import numpy as np
from smpl import plot
from smpl import io
from smpl import fit
from smpl import functions as f
import uncertainties.unumpy as unp
import uncertainties as unc


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


# ## SciPy

# In[4]:


ff = plot.fit(xdata, ydata, fmt='.', label='data', xaxis="x in a.u.",yaxis="y in a.u.",function=f.linear, params=[1])


# In[5]:


ff = plot.fit(xdata, ydata, fmt='.', label='data', xaxis="x in a.u.",yaxis="y in a.u.",function=f.line, params=[1,2])


# In[6]:


ff = plot.fit(x, y, fmt='.', function=f.line, params=[1,1], sigmas=1,lpos=2)


# In[12]:


ff = plot.fit(xdata, y, fmt='.', function=f.line, params=[1,1], sigmas=1,lpos=2)
print("Chi2 = ",fit.Chi2(xdata,y,f.line,ff))


# ## Minuit

# In[11]:


ff = plot.fit(xdata, y, fmt='.', function=f.line, params=[1,1], sigmas=1,lpos=2,fitter=fit.Fitter.MINUIT_LEASTSQUARES)
print("Chi2 = ",fit.Chi2(xdata,y,f.line,ff))

