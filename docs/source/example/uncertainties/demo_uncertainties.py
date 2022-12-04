#!/usr/bin/env python
# coding: utf-8

# # uncertainties
# 
# see: https://uncertainties-python-package.readthedocs.io/en/latest/

# In[9]:


from uncertainties import ufloat
import uncertainties.umath as umath
import uncertainties.unumpy as unp
import numpy as np
from smpl import io


# ## Single number

# In[2]:


x = ufloat(1,0.1)
print(x)


# In[3]:


print(x*x)


# This is error propagation of the function $f(x)=x^2$ yielding $\Delta f = \frac{\partial f(x)}{\partial x} \Delta x=2\Delta x$

# In[4]:


y = ufloat(1,0.2)
print(x*y)


# Here $f(x,y)=x*y$ gives $\Delta f = \sqrt{(\frac{\partial f(x)}{\partial x} \Delta x)^2 +(\frac{\partial f(y)}{\partial y} \Delta y)^2}$

# In[7]:


umath.sin(2*y)


# ## Arrays

# In[10]:


data = np.loadtxt(io.find_file('test_linear_data.txt',3))
xdata = data[:,0]
xerr = data[:,2]
ydata = data[:,1]
yerr = data[:,3]
x = unp.uarray(xdata,xerr)
y = unp.uarray(ydata,yerr)


# In[12]:


print(x)
print(y)


# In[13]:


print(x*y)


# Error propagation for each number in the array.

# In[14]:


print(unp.sin(x)*y)


# In[ ]:




