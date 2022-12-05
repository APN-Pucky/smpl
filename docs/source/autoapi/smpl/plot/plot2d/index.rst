:py:mod:`smpl.plot.plot2d`
==========================

.. py:module:: smpl.plot.plot2d


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   smpl.plot.plot2d.plot2d_kwargs
   smpl.plot.plot2d.plot2d
   smpl.plot.plot2d.sort_xyz
   smpl.plot.plot2d.pcolormesh_vplot
   smpl.plot.plot2d.map_vplot
   smpl.plot.plot2d.scatter_vplot



Attributes
~~~~~~~~~~

.. autoapisummary::

   smpl.plot.plot2d.default


.. py:data:: default
   

   

.. py:function:: plot2d_kwargs(kwargs)

   Set default plot2d_kwargs if not set.


.. py:function:: plot2d(datax, datay, dataz, **kwargs)

   Creates a 2D-Plot.

   Parameters
   ----------
   **kwargs : optional
       see :func:`plot2d_kwargs`.


.. py:function:: sort_xyz(x, y, z)


.. py:function:: pcolormesh_vplot(tvx, tvy, tvz, xaxis=None, yaxis=None, zaxis=None, logz=True, zscale=1.0, **kwargs)

   Advantage over matplotlibs pcolor(mesh) is that does not require a meshgrid. Instead it uses the data points directly in three lists.


.. py:function:: map_vplot(tvx, tvy, tvz, xaxis=None, yaxis=None, zaxis=None, logz=True, sort=True, fill_missing=True, zscale=1.0, **kwargs)


.. py:function:: scatter_vplot(vx, vy, vz, xaxis=None, yaxis=None, zaxis=None, logz=True, sort=True, fill_missing=True, zscale=1.0, **kwargs)
