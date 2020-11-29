
def has(key, dict):
    """
        Checks if the key is in the dict and not None.
    """
    return key in dict and not dict[key] is None

def find_nearest_index(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx
def find_nearest(array, value):
    array[find_nearest_index(array,value)]