:py:mod:`smpl.parallel`
=======================

.. py:module:: smpl.parallel

.. autoapi-nested-parse::

   Simplified parallelization.



Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   parallel/index.rst


Package Contents
----------------


Functions
~~~~~~~~~

.. autoapisummary::

   smpl.parallel.calc
   smpl.parallel.gen
   smpl.parallel.par
   smpl.parallel.partitioned_parallel
   smpl.parallel.res



Attributes
~~~~~~~~~~

.. autoapisummary::

   smpl.parallel.parallel


.. py:function:: calc(f, *args, **kwargs)


.. py:function:: gen(f, *args, **kwargs)

   Generates parallel execution list generator.


.. py:function:: par(f, *args, **kwargs)

   Parallel execution of f on each element of args and kwargs

   Examples
   --------
   >>> par(lambda x : x**2, range(0,5))
   [0, 1, 4, 9, 16]



.. py:data:: parallel
   

   

.. py:function:: partitioned_parallel(f, arr, n_jobs=None)

   Parallel execution of f on each element of args

   Examples
   --------
   >>> partitioned_parallel(lambda x : x**2, range(0,5))
   [0, 1, 4, 9, 16]



.. py:function:: res(a)

   Parallel evaluation of the list generator from :func:`gen`.

   Return parallel executed values.

   Examples
   --------
   >>> def twice(x):
   ...     return x+x
   >>> for r in [calc(twice,i) for i in range(0,5)]:
   ...     print(res(r))
   0
   2
   4
   6
   8
   >>> res([calc(lambda x : x**3, i) for i in range(0,5)])
   [0, 1, 8, 27, 64]
