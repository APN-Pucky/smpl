:py:mod:`smpl.doc`
==================

.. py:module:: smpl.doc

.. autoapi-nested-parse::

   Simplified python code documentation.



Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   doc/index.rst


Package Contents
----------------


Functions
~~~~~~~~~

.. autoapisummary::

   smpl.doc.append_doc
   smpl.doc.append_plot
   smpl.doc.append_str
   smpl.doc.array_table
   smpl.doc.dict_to_table
   smpl.doc.insert_doc
   smpl.doc.insert_eq
   smpl.doc.insert_latex
   smpl.doc.insert_latex_eq
   smpl.doc.insert_str
   smpl.doc.table



.. py:function:: append_doc(original)

   Append doc string of ``original`` to ``target`` object.

   Parameters
   ----------
   original : ``class`` or ``function``
       ``orignal.__doc__`` is appended to the ``__doc__`` of the ``target``

   Examples
   --------
   >>> def ho():
   ...     '''Ho'''
   ...     print(ho.__doc__)
   >>> @append_doc(ho)
   ... def hi():
   ...     '''Hi'''
   ...     print(hi.__doc__)
   >>> hi()
   HiHo



.. py:function:: append_plot(*args, xmin=-5, xmax=5)

   Append a plot to a function.


.. py:function:: append_str(txt)


.. py:function:: array_table(arr, top=True, bottom=True, init=True, tabs=1, header=True)

   Produces a reST table from a numpy array or normal 2d array.

   Parameters
   ----------
   arr : ``numpy.ndarray``, ``list`` or ``dict``
       2d array or dict
   top : ``bool``
       If ``True`` a top line is added.
   bottom : ``bool``
       If ``True`` a bottom line is added.
   init : ``bool``
       If ``True`` a tab is added at the beginning of each line.
   tabs : ``int``
       Number of tabs at the beginning of each line.
   header : ``bool``
       If ``True`` the first row is used as header.

   Examples
   --------
   >>> print(trim_eol_spaces(array_table([["a","b"],["hihi", "hoho"]],tabs=0)))
   ====== ======
   a      b
   ====== ======
   hihi   hoho
   ====== ======
   <BLANKLINE>



.. py:function:: dict_to_table(dic)


.. py:function:: insert_doc(original)

   Inserts the docstring from passed function ``original`` in the ``target`` function docstring.

   Parameters
   ----------
   original : ``class`` or ``function``
       ``orignal.__doc__`` is inserted to the ``__doc__`` of the ``target``

   Examples
   --------
   >>> def ho():
   ...     '''Ho'''
   ...     print(ho.__doc__)
   >>> @insert_doc(ho)
   ... def hi():
   ...     '''Hi'''
   ...     print(hi.__doc__)
   >>> hi()
   HoHi


.. py:function:: insert_eq()

   Inserts the function and its parameters and an equal sign.


.. py:function:: insert_latex()

   Inserts latexed code of a oneline function.


.. py:function:: insert_latex_eq()

   Inserts latexed code of a oneline function with parameters.


.. py:function:: insert_str(txt)


.. py:function:: table(dic, top=True, bottom=True, init=True, tabs=1)

   Add dict= {'key': [values...]} to a simple reST table.

   ..deprecated:: 0.0.0
