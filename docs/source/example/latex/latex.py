#!/usr/bin/env python
# coding: utf-8

# # Latex

# In[1]:


import smpl
from smpl import latex
from smpl import io
from uncertainties import ufloat
import uncertainties.unumpy as unp
import numpy as np


# In[2]:


print(latex.si(ufloat(1,1),"\\tesla"))


# In[3]:


data = np.loadtxt(io.find_file('test_linear_data.txt',3))
xdata = data[:,0]
xerr = data[:,2]
ydata = data[:,1]
yerr = data[:,3]
x = unp.uarray(xdata,xerr)
y = unp.uarray(ydata,yerr)


# In[6]:


print(latex.si_line(x))


# In[4]:


print(latex.si_tab([x,y]))


# In[5]:


print(latex.si_ttab([x,y]))


# In[ ]:





# In[ ]:




