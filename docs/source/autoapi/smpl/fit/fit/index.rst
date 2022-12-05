:py:mod:`smpl.fit.fit`
======================

.. py:module:: smpl.fit.fit


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   smpl.fit.fit.Fitter



Functions
~~~~~~~~~

.. autoapisummary::

   smpl.fit.fit.fit_kwargs
   smpl.fit.fit.auto
   smpl.fit.fit.fit
   smpl.fit.fit._wrap_func_and_param
   smpl.fit.fit._unwrap_param
   smpl.fit.fit.Chi2
   smpl.fit.fit.R2
   smpl.fit.fit.data_split
   smpl.fit.fit.fit_split



Attributes
~~~~~~~~~~

.. autoapisummary::

   smpl.fit.fit.unv
   smpl.fit.fit.usd
   smpl.fit.fit.default


.. py:data:: unv
   

   

.. py:data:: usd
   

   

.. py:class:: Fitter

   Bases: :py:obj:`enum.Enum`

   Different implementations to perform a fit.

   .. py:attribute:: AUTO
      :annotation: = 0

      

   .. py:attribute:: SCIPY_CURVEFIT
      :annotation: = 1

      

   .. py:attribute:: SCIPY_ODR
      :annotation: = 2

      

   .. py:attribute:: MINUIT_LEASTSQUARES
      :annotation: = 3

      


.. py:data:: default
   

   

.. py:function:: fit_kwargs(kwargs)

   Set default fit_kwargs if not set.


.. py:function:: auto(datax, datay, funcs=None, **kwargs)

   Automatically loop over functions and fit the best one.

   Parameters
   ----------
   funcs : function array
       functions to consider as fit. Default all ``smpl.functions``.
   **kwargs : optional
       see :func:`fit_kwargs`.

   Returns
   -------
   The best fit function and it's parameters and a ``lambda`` where the parameters are already applied to the function.



.. py:function:: fit(datax, datay, function, **kwargs)

   Returns a fit of ``function`` to ``datax`` and ``datay``.

   Parameters
   ----------
   datax : array_like
       X data either as ``unp.uarray`` or ``np.array`` or ``list``
   datay : array_like
       Y data either as ``unp.uarray`` or ``np.array`` or ``list``
   function : func
       Fit function with parameters: ``x``, ``params``
   **kwargs : optional
       see :func:`fit_kwargs`.



.. py:function:: _wrap_func_and_param(function, **kwargs)

   Wraps a function with a lambda function.


.. py:function:: _unwrap_param(fitt, fixed, Ntot)


.. py:function:: Chi2(datax, datay, function, ff, **kwargs)


.. py:function:: R2(datax, datay, function, ff, **kwargs)


.. py:function:: data_split(datax, datay, **kwargs)

   Split data + errors


.. py:function:: fit_split(datax, datay, **kwargs)

   Splits datax and datay into (x,y,xerr,yerr).

   Parameters
   ----------
   **kwargs : optional
       see :func:`fit_kwargs`.
