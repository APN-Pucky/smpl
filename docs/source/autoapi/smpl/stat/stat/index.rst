:py:mod:`smpl.stat.stat`
========================

.. py:module:: smpl.stat.stat


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   smpl.stat.stat.round_sig
   smpl.stat.stat.R2
   smpl.stat.stat.Chi2
   smpl.stat.stat.average_deviation
   smpl.stat.stat.unv_lambda
   smpl.stat.stat.poisson_dist
   smpl.stat.stat.no_dist
   smpl.stat.stat.normalize
   smpl.stat.stat.novar_mean
   smpl.stat.stat.mean
   smpl.stat.stat.noisy
   smpl.stat.stat.normal
   smpl.stat.stat.fft
   smpl.stat.stat.trim_domain
   smpl.stat.stat.get_domain
   smpl.stat.stat.is_monotone
   smpl.stat.stat.get_interesting_domain



Attributes
~~~~~~~~~~

.. autoapisummary::

   smpl.stat.stat.unv
   smpl.stat.stat.usd
   smpl.stat.stat.r2
   smpl.stat.stat.chi2


.. py:data:: unv
   

   

.. py:data:: usd
   

   

.. py:function:: round_sig(x, sig=2)

   Round to ``sig`` significant digits.

   Parameters
   ----------
   x : float
       Value to round.
   sig : int
       Number of significant digits.

   Returns
   -------
   float
       Rounded value.

   Examples
   --------
   >>> round_sig(1.23456789, sig=2)
   1.2
   >>> round_sig(1.23456789, sig=4)
   1.235


.. py:function:: R2(y, f)

   R2 - Coefficient of determination

   In the best case, the modeled values exactly match the observed values, which results in R2 = 1.
   A baseline model, which always predicts the mean of y, will have R2 = 0.
   Models that have worse predictions than this baseline will have a negative R2.

   References
   ----------

   https://en.wikipedia.org/wiki/Coefficient_of_determination


.. py:data:: r2
   

   

.. py:function:: Chi2(y, f, sigmas=None)

   Chi2 - Goodness of Fit

   In general, if Chi-squared/Nd is of order 1.0, then the fit is reasonably good.
   Coversely,  if Chi-squared/Nd >> 1.0, then the fit is a poor one.

   References
   ----------

   https://www.phys.hawaii.edu/~varner/PHYS305-Spr12/DataFitting.html


.. py:data:: chi2
   

   

.. py:function:: average_deviation(y, f)


.. py:function:: unv_lambda(f)

   Returns a function which applies :func:`unv` on the result of ``f``.


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


.. py:function:: no_dist(N)

   Return ``N`` with no uncertainties.


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


.. py:function:: normal(x, mean=0, std=1)


.. py:function:: fft(y)

   Compute the FFT of ``y``.

   Parameters
   ----------
   y : array_like
       Data to be transformed.

   Returns
   -------
   array_like



.. py:function:: trim_domain(f, fmin=np.finfo(np.float32).min / 2, fmax=np.finfo(np.float32).max / 2, steps=10000, min_ch=0.0001, recursion_limit=100)

   Get the domain of the function ``f`` with the ranges removed where the derivative of ``f`` is below ``min_ch``.


.. py:function:: get_domain(f, fmin=np.finfo(np.float32).min / 2, fmax=np.finfo(np.float32).max / 2, steps=1000)

   Return the statistically probed domain of the function ``f``.


.. py:function:: is_monotone(f, tmin=None, tmax=None, steps=1000)

   Test if function ``f`` is monotone.

   Parameters
   ----------
   f : function
       Function to be tested.
   test : array_like
       Test points.

   Returns
   -------
   bool
       True if function is monotone.

   Examples
   --------
   >>> def f(x):
   ...     return x**2
   >>> is_monotone(f)
   False
   >>> is_monotone(np.exp)
   True


.. py:function:: get_interesting_domain(f, min_ch=1e-06)

   Return interesting xmin and xmax of function ``f``.

   Examples
   --------
   >>> def f(x):
   ...     return np.sin(x)
   >>> get_interesting_domain(f)
   (-3.141625000000003, 3.141625000000003)
