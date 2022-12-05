:py:mod:`smpl.io.io`
====================

.. py:module:: smpl.io.io


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   smpl.io.io.grep
   smpl.io.io.tail
   smpl.io.io.head
   smpl.io.io.read
   smpl.io.io.write
   smpl.io.io.append
   smpl.io.io.gf
   smpl.io.io.find_file
   smpl.io.io.pwd
   smpl.io.io.import_path
   smpl.io.io.mkdirs
   smpl.io.io.pr
   smpl.io.io.files
   smpl.io.io.pn



.. py:function:: grep(pattern, inp)

   Searches for ``pattern`` in ``inp``.

   >>> from smpl import io
   >>> write("test.txt","hi\nho1\n2\n3\n4\n")
   >>> grep("h","test.txt").read()
   'hi\nho1\n'


.. py:function:: tail(inp, n=1)

   Returns the last ``n`` lines of ``fname``.

   Parameters
   ----------
   inp : str
       file name.

   Returns
   -------
   str
       last ``n`` lines of ``fname``.

   Examples
   --------
   >>> import pandas as pd
   >>> write("test.txt","hi\n1\n2\n3\n4\n")
   >>> pd.read_csv(tail("test.txt",n=2))
      3
   0  4
   >>> pd.read_csv(tail("test.txt",n=3))
      2
   0  3
   1  4



.. py:function:: head(inp, n=1)

   Returns the first ``n`` lines of ``fname``.

   Parameters
   ----------
   inp : str
       file name.

   Returns
   -------
   str
       first ``n`` lines of ``fname``.

   Examples
   --------
   >>> import pandas as pd
   >>> write("test.txt","hi\n1\n2\n3\n4\n")
   >>> pd.read_csv(head("test.txt",n=2))
      hi
   0   1
   >>> pd.read_csv(head("test.txt",n=3))
      hi
   0   1
   1   2



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



.. py:function:: find_file(fname, up=0)

   Searches for ``fname`` in all down folders or up folder to given order respectively.


.. py:function:: pwd()

   Returns the path to the path of current file (in linux format).

   Returns
   -------
   str
       path to the path of current file.


.. py:function:: import_path(path='../..')

   Adds ``path`` to the ``sys.path``.

   Parameters
   ----------
   path : str
       path to add.

   Examples
   --------
   >>> import_path('../../smpl')


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


.. py:function:: pn(a, nnl=False)
