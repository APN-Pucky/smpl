import numpy as np


def times(s, n):
    """
        Concats str n times.
    """
    return s.join(["" for i in range(0, n+1)])


def get(key, ddict, default):
    """
        Returns dict[key] if this exists else default.
    """
    if has(key, ddict):
        return ddict[key]
    else:
        return default


def has(key, ddict):
    """
        Checks if the key is in the dict and not None.
    """
    return key in ddict and not ddict[key] is None


def true(key, ddict):
    """
        Checks if the key is in the dict and not None and True.
    """
    return has(key, ddict) and ddict[key]


def find_nearest_index(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def find_nearest(array, value):
    return array[find_nearest_index(array, value)]
