#!/usr/bin/env python
# coding: utf-8

# # SubplotAnimation

# In[1]:


from smpl import animation
from smpl import plot
import matplotlib.pyplot as plt
import numpy as np
import tqdm


# ## Tight

# In[2]:


# get_ipython().run_line_magic('matplotlib', 'notebook')
plt.ioff()
for a in tqdm.tqdm(np.linspace(0,10,200)):
    fig, axs = plot.subplots(1, 3, figsize=(12, 8), sharey=True)
    fig.subplots_adjust(wspace=0)

    plot.function(lambda x: a*x**2,axes=axs[0],tight=False,xmin=0,xmax=1)
    plot.function(lambda x: a*x**5,axes=axs[0],tight=False,xmin=0,xmax=1)
    plot.function(lambda x: a*x**3,axes=axs[1],logx=True,tight=False,xmin=0,xmax=1)
    plot.function(lambda x: a*x**1,axes=axs[2],tight=False,xmin=0,xmax=1)
    animation.frame()

#ani.save("test.gif")
ani = animation.animate(interval=10,blit=True)
plt.show(block=False)
plt.pause(10)
plt.close()


# ## Normal

# In[5]:


#get_ipython().run_line_magic('matplotlib', 'notebook')
animation.clear()
for a in tqdm.tqdm(np.linspace(0,10,100)):
    fig, axs = plot.subplots(1, 3, figsize=(12, 8), sharey=True)
    fig.subplots_adjust(wspace=0)

    plot.function(lambda x: a*x**3,axes=axs[1],logx=True,xmin=0,xmax=1)
    plot.function(lambda x: a*x**2,axes=axs[0],xmin=0,xmax=1)
    plot.function(lambda x: a*x**5,axes=axs[0],xmin=0,xmax=1)
    plot.function(lambda x: a*x**1,axes=axs[2],xmin=0,xmax=1)
    animation.frame()

#ani.save("test.gif")
ani = animation.animate(interval=10,blit=True)
plt.show(block=False)
plt.pause(10)
plt.close()




# In[ ]:




