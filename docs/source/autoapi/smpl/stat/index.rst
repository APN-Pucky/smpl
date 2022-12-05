:py:mod:`smpl.stat`
===================

.. py:module:: smpl.stat

.. autoapi-nested-parse::

   Simplified statistics.



Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   stat/index.rst


Package Contents
----------------


Functions
~~~~~~~~~

.. autoapisummary::

   smpl.stat.R2
   smpl.stat.Chi2
   smpl.stat.average_deviation
   smpl.stat.fft
   smpl.stat.get_interesting_domain
   smpl.stat.mean
   smpl.stat.no_dist
   smpl.stat.noisy
   smpl.stat.normalize
   smpl.stat.novar_mean
   smpl.stat.poisson_dist
   smpl.stat.unv_lambda



Attributes
~~~~~~~~~~

.. autoapisummary::

   smpl.stat.unv
   smpl.stat.usd


.. py:function:: R2(y, f)

   R2 - Coefficient of determination

   In the best case, the modeled values exactly match the observed values, which results in R2 = 1.
   A baseline model, which always predicts the mean of y, will have R2 = 0.
   Models that have worse predictions than this baseline will have a negative R2.

   References
   ----------

   https://en.wikipedia.org/wiki/Coefficient_of_determination


.. py:function:: Chi2(y, f, sigmas=None)

   Chi2 - Goodness of Fit

   In general, if Chi-squared/Nd is of order 1.0, then the fit is reasonably good.
   Coversely,  if Chi-squared/Nd >> 1.0, then the fit is a poor one.

   References
   ----------

   https://www.phys.hawaii.edu/~varner/PHYS305-Spr12/DataFitting.html


.. py:function:: average_deviation(y, f)


.. py:function:: fft(y)

   Compute the FFT of ``y``.

   Parameters
   ----------
   y : array_like
       Data to be transformed.

   Returns
   -------
   array_like



.. py:function:: get_interesting_domain(f, min_ch=1e-06)

   Return interesting xmin and xmax of function ``f``.

   Examples
   --------
   >>> def f(x):
   ...     return np.sin(x)
   >>> get_interesting_domain(f)
   (-3.141625000000003, 3.141625000000003)


.. py:function:: mean(n)

   Return mean of ``n`` with combined error of variance and unvertainties of ``n``.

   Parameters
   ----------
   n : array_like
       Data to be averaged.

   Returns
   -------
   uncertainties.unumpy.uarray
       Mean of ``n``.

   Examples
   --------
   >>> n = np.array([1, 2, 3, 4, 5])
   >>> mean(n)
   3.0+/-1.5811388300841898


.. py:function:: no_dist(N)

   Return ``N`` with no uncertainties.


.. py:function:: noisy(x, mean=1, std=0.1)

   Add gaussian noise to ``x``.

   Parameters
   ----------
   x : array_like
       Data to be smeared.
   mean : float
       Mean of gaussian noise.
   std : float
       Standard deviation of gaussian noise.

   Returns
   -------
   array_like
       Smeared data.

   Examples
   --------
   >>> x = np.array([1, 2, 3, 4, 5])
   >>> noisy(x,std=0)
   array([1., 2., 3., 4., 5.])


.. py:function:: normalize(ydata)

   Return normalized ``ydata``.

   Parameters
   ----------
   ydata : array_like
       Data to be normalized.

   Returns
   -------
   array_like
       Normalized data.

   Examples
   --------
   >>> ydata = np.array([1, 2, 3, 4, 5])
   >>> normalize(ydata)
   array([0.  , 0.25, 0.5 , 0.75, 1.  ])


.. py:function:: novar_mean(n)

   Return mean of ``n`` with only the uncertainties of ``n`` and no variance.


.. py:function:: poisson_dist(N)

   Return ``N`` with added poissonian uncertainties.

   Parameters
   ----------
   N : float or array_like of floats
       Number of events.

   Returns
   -------
   uncertainties.unumpy.uarray
       Number of events with uncertainties.

   Examples
   --------
   >>> poisson_dist(100)
   array(100.0+/-10.0, dtype=object)


.. py:data:: unv
   

   

.. py:function:: unv_lambda(f)

   Returns a function which applies :func:`unv` on the result of ``f``.


.. py:data:: usd
   

   
