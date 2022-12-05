:py:mod:`smpl.data`
===================

.. py:module:: smpl.data

.. autoapi-nested-parse::

   Simplified internal data parsing and transforming.



Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   data/index.rst


Package Contents
----------------


Functions
~~~~~~~~~

.. autoapisummary::

   smpl.data.__data_split
   smpl.data.data_kwargs
   smpl.data.filtered_data_split
   smpl.data.flatmesh



.. py:function:: __data_split(datax, datay, **kwargs)

   Splits datax and datay into (x,y,xerr,yerr).
   Does not apply filters `frange` and `fselector`.

   Parameters
   ----------
   **kwargs : optional
       see :func:`data_kwargs`.


.. py:function:: data_kwargs(kwargs)

   Set default data_kwargs if not set.


.. py:function:: filtered_data_split(datax, datay, **kwargs)

   Splits datax and datay into (x,y,xerr,yerr).
   Applies filters `fselector` and `frange`.

   Returns
   -------
   (x,y,xerr,yerr) : tuple
       four arrays with specified values.

   Parameters
   ----------
   **kwargs : optional
       see :func:`data_kwargs`.


.. py:function:: flatmesh(*args)

   Similar to `numpy.meshgrid` but the result will be of one dimension instead of stacked arrays.
