from smpl import util
params = 0
name = 1

def _append(txt):
    def wrapper(target):
        if target.__doc__ is None:
            target.__doc__ = ""
        target.__doc__ += txt
        return target
    return wrapper

def append(txt):
    """
    TODO split cases doc/txt/plot?
    """
    return None

def append_str(txt):
    return _append(txt)

def append_plot(*args,xmin=-5,xmax=5):
    """
    Append a plot to a function.
    """
    #return _append("\n\n\t.. plot::\n\t\t:include-source:\n\n\t\t>>> from " + target.__module__ + " import " +target.__name__ + "\n\t\t>>> from smpl import plot\n\t\t>>> plot.function("+ target.__name__ + "," + ','.join([str(a) for a in args]) + ",xmin="+str(xmin) + ",xmax=" + str(xmax)+")")

    def wrapper(target):
        if target.__doc__ is None:
            target.__doc__ = ""
        target.__doc__ += "\n\n\t.. plot::\n\t\t:include-source:\n\n\t\t>>> from " + target.__module__ + " import " +target.__name__ + "\n\t\t>>> from smpl import plot\n\t\t>>> plot.function("+ target.__name__ + "," + ','.join([str(a) for a in args]) + ",xmin="+str(xmin) + ",xmax=" + str(xmax)+")"
        #print(target.__doc__)
        return target
    return wrapper

def append_doc(original):
    """
    Append doc string of ``original`` to ``target`` object.

    Parameters
    ==========
    original : ``class`` or ``function``
        ``orignal.__doc__`` is appended to the ``__doc__`` of the ``target``

    Examples
    ========

    >>> def ho():
    ...     '''Ho'''
    ...     print(ho.__doc__)
    >>> @append_doc(ho)
    ... def hi():
    ...     '''Hi'''
    ...     print(hi.__doc__)
    >>> hi()
    HiHo
    """
    return _append(original.__doc__)
    def wrapper(target):
        if target.__doc__ is None:
            target.__doc__ = ""
        target.__doc__ += original.__doc__
        return target
    return wrapper

def _insert(txt):
    def wrapper(target):
        if target.__doc__ is None:
            target.__doc__ = ""
        target.__doc__ = txt + target.__doc__
        return target
    return wrapper

def insert_str(txt):
    return _insert(txt)

def insert_doc(original):
    """
    Inserts the docstring from passed function ``original`` in the ``target`` function docstring.
    """
    return _insert(original.__doc__)
    def wrapper(target):
        if target.__doc__ is None:
            target.__doc__ = ""
        target.__doc__ = original.__doc__ + target.__doc__
        return target
    return wrapper

def insert_eq():
    """
    Inserts the function and its parameters and an equal sign
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


def table_sep(tabs=1):
    return "==============  ==============  ==============\n" +"\t".join(["" for i in range(0,tabs+1)])
def table(dic,top=True,bottom=True,init=True,tabs=1):
    """
    Add dict= {'key': [values...]} to a simple reST table.
    """
    t =  util.times("\t",tabs)
    rs = ""
    if init:
        rs += t
    if top:
        rs += table_sep(tabs=tabs)
    for k,vs in dic.items():
        rs += str(k) 
        p = str(k)
        for v in vs:
            rs += "".join([' ' for i in range(16-len(p))]) + str(v)
            p = str(v)
        rs += "\n" + t
    if bottom:
        rs += table_sep(tabs=tabs)
    else:
        rs += "\n"
    return rs


if __name__ == "__main__":
    import doctest
    doctest.testmod()