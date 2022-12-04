#!/usr/bin/env python
# coding: utf-8

# # Function Plot

# In[1]:


from smpl import plot
import numpy as np


# ## without uncertainties

# ### $\dot x = 1- \exp(- x^2)$
# 
# Fixed point $x = 0$ and 
# 
# $\ddot x = -2x \exp(-x^2) \implies \ddot x(x = 0)=0$
# 
# only metastable for $x\lt0$
# 

# In[2]:


plot.function( lambda x : 1- np.exp(-x**2), xaxis="$x$", yaxis="$\\dot x$",xmin=-10, xmax=10 )


# ### $\dot x = \ln x$
# 
# Fixed point $x = 1$
# 
# $$\ddot x = \frac{1}{x} \implies \ddot x(x=1) = 1 > 0$$
# 
# $\implies$  unstable

# In[3]:


plot.function( lambda x : np.log(x), xaxis="$x$", yaxis="$\\dot x$",xmin=0.1, xmax=5 )


# ### $\dot x = -\tan x$
# Fixed points for $x=0$ or $x=\pm n\pi$ with $n\in \mathbb{N}$
# 
# $$\ddot x = -\frac{1}{\cos^2(x)}$$
# 
# 
# $$\ddot x(x=0) = -1 \lt 0$$
# 
# $$\ddot x(x=n \pi) = -1 \lt 0$$
# 
# $\implies$ stable

# In[4]:


plot.function( lambda x : -np.tan(x), xaxis="$x$", yaxis="$\\dot x$",xmin=0.1, xmax=5,steps=100 )


# ## with uncertainties

# In[5]:


import uncertainties as unc
a = unc.ufloat(1,0.1)


# In[6]:


plot.function(lambda x : 1- a*np.exp(-x**2), xaxis="$x$", yaxis="$\\dot x$",xmin=-1, xmax=1,sigmas=1 )


# ## Complex

# In[7]:


from smpl.stat import fft
y = np.sin(np.arange(256))
print(len(fft(y)))
plot.data(*fft(y),label="FFT",fmt="-")


# In[8]:


from smpl.stat import fft
plot.data(*fft(np.sin(np.arange(256))),*fft(np.sin(1/np.pi*np.arange(100))),label="FFT",fmt="-")


# ## without xmin and xmax
# xmin and xmax will have to be guessed

# In[9]:


from smpl import plot
plot.function(lambda x: x**2,)


# In[10]:


from smpl import plot
import numpy as np
def f(x):
    return np.exp(x)
plot.function(f,label="exp")


# In[11]:


from smpl import plot
from smpl import functions as f
def gauss(x):
    """Gauss"""
    return f.gauss(x,0,1,3,0)
plot.function(gauss)


# In[12]:


def gauss(x):
    return np.arctan(x)
plot.function(gauss)


# In[13]:


def gauss(x):
    return np.tan(x)
plot.function(gauss)


# In[14]:


def gauss(x):
    return np.log(x)
plot.function(gauss)


# In[17]:


def gauss(x):
    return x**3+5*x**2-2
plot.function(gauss)


# In[16]:


def gauss(x):
    return x**0.5
plot.function(gauss)


# In[ ]:




