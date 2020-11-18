def add_doc(original):
    """
    Append doc string of ``original`` to ``target`` object.

    Examples
    ========

    >>> def ho():
    ...     '''
    ...     Ho
    ...     ''' 
    ...     print(ho.__doc__)
    ... @add_doc(ho)
    ... def hi():
    ...     '''
    ...     Hi
    ...     ''' 
    ...     print(hi.__doc__)
    ... hi()
    HiHo
    """
    def wrapper(target):
        target.__doc__ += original.__doc__
        return target
    return wrapper



if __name__ == "__main__":
    import doctest
    doctest.testmod()