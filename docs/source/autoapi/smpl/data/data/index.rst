:py:mod:`smpl.data.data`
========================

.. py:module:: smpl.data.data


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   smpl.data.data.data_kwargs
   smpl.data.data.__data_split
   smpl.data.data._data_split
   smpl.data.data.filtered_data_split
   smpl.data.data.flatmesh



Attributes
~~~~~~~~~~

.. autoapisummary::

   smpl.data.data.default
   smpl.data.data.unv
   smpl.data.data.usd


.. py:data:: default
   

   

.. py:data:: unv
   

   

.. py:data:: usd
   

   

.. py:function:: data_kwargs(kwargs)

   Set default data_kwargs if not set.


.. py:function:: __data_split(datax, datay, **kwargs)

   Splits datax and datay into (x,y,xerr,yerr).
   Does not apply filters `frange` and `fselector`.

   Parameters
   ----------
   **kwargs : optional
       see :func:`data_kwargs`.


.. py:function:: _data_split(datax, datay, **kwargs)

   Applies `fselector` and calls :func:`data_split`


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
