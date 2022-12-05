:py:mod:`smpl.plot.plot`
========================

.. py:module:: smpl.plot.plot


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   smpl.plot.plot.set_plot_style
   smpl.plot.plot.plot_kwargs
   smpl.plot.plot.fit
   smpl.plot.plot._fit_impl
   smpl.plot.plot.data
   smpl.plot.plot.auto
   smpl.plot.plot._function
   smpl.plot.plot.plt_plt
   smpl.plot.plot.__function
   smpl.plot.plot.function
   smpl.plot.plot.plt_residue
   smpl.plot.plot.data_split
   smpl.plot.plot._fit
   smpl.plot.plot.plt_data
   smpl.plot.plot.get_fnc_legend
   smpl.plot.plot.plt_fit_or_interpolate
   smpl.plot.plot.plt_interpolate
   smpl.plot.plot.plt_fit
   smpl.plot.plot.init_plot
   smpl.plot.plot.save_plot
   smpl.plot.plot.show



Attributes
~~~~~~~~~~

.. autoapisummary::

   smpl.plot.plot.unv
   smpl.plot.plot.usd
   smpl.plot.plot.default


.. py:function:: set_plot_style()


.. py:data:: unv
   

   

.. py:data:: usd
   

   

.. py:data:: default
   

   

.. py:function:: plot_kwargs(kwargs)

   Set default plot_kwargs if not set.


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



.. py:function:: _fit_impl(datax, datay, function, **kwargs)


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





.. py:function:: _function(func, xfit, **kwargs)


.. py:function:: plt_plt(x, y, fmt, color, label, linestyle)


.. py:function:: __function(gfunc, xlinspace, fmt='-', label=None, color=None, hatch=None, sigmas=0.0, linestyle=None, alpha=0.4)


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


.. py:function:: plt_residue(datax, datay, gfunction, rfit, fig, **kwargs)


.. py:function:: data_split(datax, datay, **kwargs)


.. py:function:: _fit(datax, datay, function, **kwargs)

   Returns a fit like :func:`fit` but does no plotting.


.. py:function:: plt_data(datax, datay, **kwargs)

   Plot datay vs datax


.. py:function:: get_fnc_legend(function, rfit, **kwargs)


.. py:function:: plt_fit_or_interpolate(datax, datay, fitted, l=None, c=None, f=None, ls=None, **kwargs)


.. py:function:: plt_interpolate(datax, datay, icolor=None, **kwargs)

   Interpolate and Plot that Interpolation.


.. py:function:: plt_fit(datax, datay, gfunction, **kwargs)

   Fit and Plot that Fit.


.. py:function:: init_plot(kwargs)


.. py:function:: save_plot(**kwargs)

   save plot


.. py:function:: show(**kwargs)
