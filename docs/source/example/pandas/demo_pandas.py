#!/usr/bin/env python
# coding: utf-8

# # pandas
# 
# see: https://pandas.pydata.org/pandas-docs/stable/

# In[1]:


import pandas as pd
from smpl import io


# ## Read

# In[2]:


data = pd.read_csv(io.find_file('test_linear_data2.txt',3),delimiter=" ")
data


# In[3]:


data['z'] = data['x']*data['y']
data


# In[4]:


data.describe()


# In[5]:


data.plot(x='x',y='z')


# ## To Latex

# In[6]:


df = pd.DataFrame({'name': ['Raphael', 'Donatello'],

                   'mask': ['red', 'purple'],

                   'weapon': ['sai', 'bo staff']})
print(df.to_latex())


# Needs \usepackage{booktabs}

# In[ ]:





# ## pandas + uncertainties

# In[7]:


import uncertainties.unumpy as unp


# In[8]:


rdata = pd.read_csv(io.find_file('test_linear_data2.txt',3),delimiter=" ")
data = pd.DataFrame()
data['x'] = unp.uarray(rdata['x'],rdata['dx'])
data['y'] = unp.uarray(rdata['y'],rdata['dy'])
data['z'] = data['x']*data['y']
data


# In[13]:


data.describe()


# Error once with variance and once without:
# $nerr=\sqrt{\text{var}^2+\text{err}^2}$

# In[13]:


from smpl import stat
print(stat.novar_mean(data['x']))
print(stat.mean(data['x']))


# In[10]:


print(data.to_latex())


# In[ ]:





# ## pandas + plot

# In[11]:


from smpl import plot
plot.data(data['x'],data['y'])
plot.data(data['x'],data['z'])


# In[ ]:




