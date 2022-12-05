:py:mod:`smpl.io`
=================

.. py:module:: smpl.io

.. autoapi-nested-parse::

   Simplified input and output.



Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   io/index.rst


Package Contents
----------------


Functions
~~~~~~~~~

.. autoapisummary::

   smpl.io.append
   smpl.io.files
   smpl.io.find_file
   smpl.io.gf
   smpl.io.mkdirs
   smpl.io.pr
   smpl.io.pwd
   smpl.io.read
   smpl.io.write



.. py:function:: append(destination, content, mode='a+')

   Appends to file by string or writable :obj:`destiantion`.

   Parameters
   ----------
   destination : str, writeable
       destination to write to.
   content : str
       text to be written.
   mode : str
       mode to open the file.
       Default is 'a+' (append and read).

   Examples
   --------
   >>> append(sys.stdout,"hi")
   hi


.. py:function:: files(ending, folder='.')

   Get all the files in ``folder`` ending with ``ending``.

   Parameters
   ----------
   folder : str
       folder name.
   ending : str
       ending of the files.

   Returns
   -------
   list
       list of files.

   Examples
   --------
   >>> files(".ini")
   [(0, 'pytest', './pytest.ini')]


.. py:function:: find_file(fname, up=0)

   Searches for ``fname`` in all down folders or up folder to given order respectively.


.. py:function:: gf(i=3)

   Scientific number format.

   Parameters
   ----------
   i : int
       Number of digits.

   Returns
   -------
   str
       Scientific number format string.

   Examples
   --------
   >>> gf(2)
   '{0:.2g}'
   >>> gf(2).format(789234578934)
   '7.9e+11'
   >>> gf(5).format(789234578934)
   '7.8923e+11'



.. py:function:: mkdirs(fn)

   Creates the neccessary directories above ``fn``.

   Parameters
   ----------
   fn : str
       file name.

   Examples
   --------
   >>> mkdirs("test.out")


.. py:function:: pr(a, nnl=False)

   Prints the passed ``a``.

   Parameters
   ----------
   nnl : bool
       no-new-line

   Returns
   -------
   a : any
       unchanged ``a``.

   Examples
   --------
   >>> 5 + pr(4)
   4
   9
   >>> 5 + pr(4, nnl=True)
   49



.. py:function:: pwd()

   Returns the path to the path of current file (in linux format).

   Returns
   -------
   str
       path to the path of current file.


.. py:function:: read(fname)

   Reads the file ``fname``.

   Parameters
   ----------
   fname : str
       file name.

   Returns
   -------
   str
       content of the file.

   Examples
   --------
   >>> read("nonexistent.txt")
   ''
   >>> write("test.out","hi")
   >>> read("test.out")
   'hi'


.. py:function:: write(destination, content, mode='w+')

   Write to file by string or writable :obj:`destiantion`.

   Parameters
   ----------
   destination : str, writeable
       destination to write to.
   content : str
       text to be written.

   Examples
   --------
   >>> write(sys.stdout,"hi")
   hi
   >>> write("test.out","hi")
   >>> read("test.out")
   'hi'
