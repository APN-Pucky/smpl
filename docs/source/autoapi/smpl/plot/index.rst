:py:mod:`smpl.plot`
===================

.. py:module:: smpl.plot

.. autoapi-nested-parse::

   Simplified plotting.



Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   plot/index.rst
   plot2d/index.rst


Package Contents
----------------


Functions
~~~~~~~~~

.. autoapisummary::

   smpl.plot.auto
   smpl.plot.data
   smpl.plot.fit
   smpl.plot.function
   smpl.plot.plot_kwargs
   smpl.plot.plot2d
   smpl.plot.plot2d_kwargs



Attributes
~~~~~~~~~~

.. autoapisummary::

   smpl.plot.unv
   smpl.plot.usd


.. py:function:: auto(*adata, funcs=None, **kwargs)

   Automatically loop over functions and fit the best one.

   Parameters
   ----------
   funcs : function array
       functions to consider as fit. Default all ``smpl.functions``.
   **kwargs : optional
       see :func:`plot_kwargs`.

   Returns
   -------
   The best fit function and it's parameters. Also a lambda function where the parameters are already applied.





.. py:function:: data(*data, function=None, **kwargs)

   Plot datay against datax via :func:`fit`

   Parameters
   ----------
   datax : array_like
       X data either as ``unp.uarray`` or ``np.array`` or ``list``
   datay : array_like
       Y data either as ``unp.uarray`` or ``np.array`` or ``list``
   function : func,optional
       Fit function with parameters: ``x``, ``params``
   **kwargs : optional
       see :func:`plot_kwargs`.
   Returns
   -------
   array_like
       Optimized fit parameters of ``function`` to ``datax`` and ``datay``


.. py:function:: fit(func, *adata, **kwargs)

   Fit and plot function to datax and datay.

   Parameters
   ----------
   datax : array_like
       X data either as ``unp.uarray`` or ``np.array`` or ``list``
   datay : array_like
       Y data either as ``unp.uarray`` or ``np.array`` or ``list``
   function : func
       Fit function with parameters: ``x``, ``params``
   **kwargs : optional
       see :func:`plot_kwargs`.
   Fit parameters can be fixed via ``kwargs`` eg. ``a=5``.

   Returns
   -------
   array_like
       Optimized fit parameters of ``function`` to ``datax`` and ``datay``.
       If ``datay`` is complex, both the real and imaginary part are returned.

   Examples
   --------

   .. plot::
       :include-source:

       >>> from smpl import functions as f
       >>> from smpl import plot
       >>> param = plot.fit([0,1,2],[0,1,2],f.line)
       >>> plot.unv(param).round()[0]
       1.0



.. py:function:: function(func, *args, **kwargs)

   Plot function ``func`` between ``xmin`` and ``xmax``

   Parameters
   ----------
   func : function
       Function to be plotted between ``xmin`` and ``xmax``, only taking `array_like` ``x`` as parameter
   *args : optional
       arguments for ``func``
   **kwargs : optional
       see :func:`plot_kwargs`.


.. py:function:: plot_kwargs(kwargs)

   Set default plot_kwargs if not set.


.. py:data:: unv
   

   

.. py:data:: usd
   

   

.. py:function:: plot2d(datax, datay, dataz, **kwargs)

   Creates a 2D-Plot.

   Parameters
   ----------
   **kwargs : optional
       see :func:`plot2d_kwargs`.


.. py:function:: plot2d_kwargs(kwargs)

   Set default plot2d_kwargs if not set.
