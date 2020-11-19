params = 0
name = 1

def append(original):
    """
    Append doc string of ``original`` to ``target`` object.

    Paramerters
    ===========
    original : ``class`` or ``function``
        ``orignal.__doc__`` is appended to the ``__doc__`` of the ``target``

    Examples
    ========

    >>> def ho():
    ...     '''Ho'''
    ...     print(ho.__doc__)
    >>> @append(ho)
    ... def hi():
    ...     '''Hi'''
    ...     print(hi.__doc__)
    >>> hi()
    HiHo
    """
    def wrapper(target):
        if target.__doc__ is None:
            target.__doc__ = ""
        target.__doc__ += original.__doc__
        return target
    return wrapper

def insert(original):
    def wrapper(target):
        if target.__doc__ is None:
            target.__doc__ = ""
        target.__doc__ = original.__doc__ + target.__doc__
        return target
    return wrapper

def insert_eq():
    """
    Inserts the function and its parameters and a equal sign
    """
    def wrapper(target):
        if target.__doc__ is None:
            target.__doc__ = ""
        safe = target.__doc__
        target.__doc__ = target.__name__  + "("
        for v in target.__code__.co_varnames:
            target.__doc__ += v + ","
        target.__doc__ = target.__doc__[:-1]
        target.__doc__ += ") = " + safe
        return target
    return wrapper

def insert_latex():
    """
    TODO 
    """
    def wrapper(target):
        if target.__doc__ is None:
            target.__doc__ = ""
        safe = target.__doc__
        target.__doc__ = target.__name__  + "("
        for v in target.__code__.co_varnames:
            target.__doc__ += v + ","
        target.__doc__ = target.__doc__[:-1]
        target.__doc__ += ") = " + safe
        return target
    return wrapper



if __name__ == "__main__":
    import doctest
    doctest.testmod()