:py:mod:`smpl.util.util`
========================

.. py:module:: smpl.util.util


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   smpl.util.util.times
   smpl.util.util.get
   smpl.util.util.has
   smpl.util.util.true
   smpl.util.util.find_nearest_index
   smpl.util.util.find_nearest



.. py:function:: times(s, n)

   Concats string ``s`` ``n`` times.

   Examples
   --------
   >>> times("hi",5)
   'hihihihihi'

   .. deprecated:: 0.0.0



.. py:function:: get(key, ddict, default=None)

   Returns dict[key] if this exists else default.

   Examples
   --------
   >>> d = {'a' : 1 , 'b' : 2 , 'c' : 3}
   >>> get('a',d,5)
   1
   >>> get('x',d,5)
   5



.. py:function:: has(key, ddict)

   Checks if the key is in the dict and not None.

   Examples
   --------
   >>> d = {'a' : 1 , 'b' : 2 , 'c' : 3}
   >>> has('a',d)
   True
   >>> has('x',d)
   False




.. py:function:: true(key, ddict)

   Checks if the key is in the dict and not None and True.

   Examples
   --------
   >>> d = {'a' : True , 'b' : True , 'c' : False}
   >>> true('a', d)
   True
   >>> true('c', d)
   False
   >>> true('x', d)
   False



.. py:function:: find_nearest_index(array, value)

   Returns the index of the element in ``array`` closest to ``value``

   Examples
   --------
   >>> find_nearest_index([1,7,6,2] , 1.9)
   3



.. py:function:: find_nearest(array, value)

   Return the element in ``array`` closest to ``value``

   Examples
   --------
   >>> find_nearest([1,7,6,2] , 1.9)
   2
