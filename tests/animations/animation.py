#!/usr/bin/env python
# coding: utf-8

# # Render
# 
# This is done through rendering the figure first and then reload it in a FuncAnimation with imshow.
# Therefore the zoom function is limited to the resolution of the figure.

# In[1]:


from smpl import animation
from smpl import plot
import matplotlib.pyplot as plt
import numpy as np
import tqdm


# ## live-render

# In[5]:


#get_ipython().run_line_magic('matplotlib', 'notebook')
plt.ioff()
def update(a):
    plot.function(lambda x : a*x**2,xmin=0,xmax=5,init=True,tight=False)

ani = animation.animate(update = update,frames=np.linspace(0,10,200), interval=10,blit=True)
plt.show(block=False)
plt.pause(10)
plt.close()


# 
# ## pre-render

# In[3]:


#get_ipython().run_line_magic('matplotlib', 'notebook')
plt.ioff()
for a in tqdm.tqdm(np.linspace(0,10,200)):
    plot.function(lambda x : a*x**2,xmin=0,xmax=5,init=True,tight=False)
    animation.frame()

#ani.save("test.gif")
ani = animation.animate(interval=10,blit=True)
plt.show(block=False)
plt.pause(10)
plt.close()


# ## Save

# In[4]:


ani.save("test.gif")


# In[ ]:





# In[ ]:





# In[ ]:




