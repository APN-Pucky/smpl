import numpy as np

def times(str,int):
    return str.join(["" for i in range(0,int+1)])

def has(key, dict):
    """
        Checks if the key is in the dict and not None.
    """
    return key in dict and not dict[key] is None

def true(key, dict):
    """
        Checks if the key is in the dict and not None and True.
    """
    return has(key,dict) and dict[key]


def find_nearest_index(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx
def find_nearest(array, value):
    array[find_nearest_index(array,value)]
