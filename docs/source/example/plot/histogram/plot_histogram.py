#!/usr/bin/env python
# coding: utf-8

# # Histogram

# In[1]:


import smpl
from smpl import plot
from smpl import stat
from smpl import functions as f
import numpy as np
np.random.seed(1337)
print(smpl.__version__)


# Data will be binned for histogram like treatment if bins is set.

# In[28]:


x= np.random.randn(1000000)
# Default uncertainty of bins is poisson distributed in y direction and none for x
plot.fit(x,f.gauss,bins=20,label="data",binunc=stat.no_dist,init=True)
plot.fit(x,f.gauss,bins=20,label="data",init=True)
plot.fit(x,f.gauss,bins=20,label="data",fmt="hist",init=True)
plot.fit(x,f.gauss,bins=20,label="data",sigmas=1,fmt="step",init=True)


# In[30]:


x= np.random.randn(100000)
plot.fit(stat.normalize(x),stat.normalize(x**3),f.gauss,bins=50,lpos=-1,binunc=stat.no_dist,init=False)


# In[ ]:




