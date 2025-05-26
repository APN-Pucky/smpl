
Animations
================================

.. jupyter-execute::

    print('hi')
    from ipywidgets import widgets
    widgets.IntSlider(value=0,min=0,max=100)

.. jupyter-execute::

    from smpl_animation import animation
    from smpl import plot
    from ipywidgets import widgets
    import numpy as np

    def fta(n = 1.0):
        plot.function(lambda x : np.exp(n*np.log(x)-x),xmin = 0.1,xmax=100,tight=False,init=False)
    
    animation.interactive(fta,widgets.IntSlider(value=0,min=0,max=100),prerender=True)
 

.. jupyter-execute::

    from smpl_animation import animation
    from smpl import plot
    import numpy as np

    for a in np.linspace(0,10,200):
        plot.function(lambda x : a*x**2,xmin=0,xmax=5,init=True,tight=False)
        animation.frame()

    ani = animation.animate(interval=10,blit=True)
    ani.widget_gif()
   

.. toctree::
    :glob:
    :maxdepth: 2

    **
