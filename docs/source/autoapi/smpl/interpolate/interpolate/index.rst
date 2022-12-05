:py:mod:`smpl.interpolate.interpolate`
======================================

.. py:module:: smpl.interpolate.interpolate


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   smpl.interpolate.interpolate.identity
   smpl.interpolate.interpolate.interpolate_kwargs
   smpl.interpolate.interpolate.interpolate_split
   smpl.interpolate.interpolate.interpolate
   smpl.interpolate.interpolate.check
   smpl.interpolate.interpolate._interpolate
   smpl.interpolate.interpolate._interpolate_exp



Attributes
~~~~~~~~~~

.. autoapisummary::

   smpl.interpolate.interpolate.unv
   smpl.interpolate.interpolate.usd
   smpl.interpolate.interpolate.default


.. py:data:: unv
   

   

.. py:data:: usd
   

   

.. py:function:: identity(x)


.. py:data:: default
   

   

.. py:function:: interpolate_kwargs(kwargs)

   Set default interpolate_kwargs if not set.


.. py:function:: interpolate_split(datax, datay, **kwargs)

   Splits datax and datay into (x,y,xerr,yerr).

   Parameters
   ----------
   **kwargs : optional
       see :func:`interpolate_kwargs`.


.. py:function:: interpolate(*data, **kwargs)


.. py:function:: check(f, *args)


.. py:function:: _interpolate(*data, **kwargs)


.. py:function:: _interpolate_exp(x, y, **kwargs)
