#!/usr/bin/env python
# coding: utf-8

# # Parallel

# In[1]:


import smpl
from smpl import plot
from smpl import functions as f
import time
from smpl.parallel import *


# In[2]:


# our heavy duty test function we aim to parallelize
def long_calc(x):
    for i in range(1000000):
        i = i+x
        i = i*x
        i = i/x
        i = i-x
    return x*x


# ### Non-parallelized

# In[3]:


tic = time.perf_counter()
print([long_calc(x) for x in range(1,20)])
toc = time.perf_counter()
print(f"\nTook {toc - tic:0.4f} seconds")


# In[4]:


tic = time.perf_counter()
for x in range(1,20):
        print(long_calc(x))
toc = time.perf_counter()
print(f"\nTook {toc - tic:0.4f} seconds")


# ### Auto parallelized

# In[5]:


tic = time.perf_counter()
print(par(long_calc,range(1,20)))
toc = time.perf_counter()
print(f"\nTook {toc - tic:0.4f} seconds")


# In[6]:


tic = time.perf_counter()
for p in par(long_calc,range(1,20)):
        print(p)
toc = time.perf_counter()
print(f"\nTook {toc - tic:0.4f} seconds")


# ### Manual parallelized

# In[7]:


tic = time.perf_counter()
print(res([calc(long_calc,x) for x in range(1,20)]))
toc = time.perf_counter()
print(f"\nTook {toc - tic:0.4f} seconds")


# In[ ]:




