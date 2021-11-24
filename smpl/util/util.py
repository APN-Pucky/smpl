import numpy as np


def times(s, n):
    """
    Concats string ``s`` ``n`` times.

    Examples
    --------
    >>> times("hi",5)
    'hihihihihi'

    """
    return s.join(["" for i in range(0, n+1)])


def get(key, ddict, default):
    """
    Returns dict[key] if this exists else default.

    Examples
    --------
    >>> d = {'a' : 1 , 'b' : 2 , 'c' : 3}
    >>> get('a',d,5)
    1
    >>> get('x',d,5)
    5

    """
    if has(key, ddict):
        return ddict[key]
    else:
        return default


def has(key, ddict):
    """
    Checks if the key is in the dict and not None.

    Examples
    --------
    >>> d = {'a' : 1 , 'b' : 2 , 'c' : 3}
    >>> has('a',d)
    True
    >>> has('x',d)
    False


    """
    return key in ddict and not ddict[key] is None


def true(key, ddict):
    """
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

    """
    return has(key, ddict) and ddict[key]


def find_nearest_index(array, value):
    """
    Returns the index of the element in ``array`` closest to ``value``

    Examples
    --------
    >>> find_nearest_index([1,7,6,2] , 1.9)
    3

    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def find_nearest(array, value):
    """
    Return the element in ``array`` closest to ``value``

    Examples
    --------
    >>> find_nearest([1,7,6,2] , 1.9)
    2

    """
    return array[find_nearest_index(array, value)]
