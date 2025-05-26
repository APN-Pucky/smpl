from .doc import *

## Functions below are not in the smpl.doc package since they are very specific but fit in doc perfectly.


def append_plot(*args, xmin=-5, xmax=5):
    """Append a plot to a function."""
    # return _append("\n\n\t.. plot::\n\t\t:include-source:\n\n\t\t>>> from " + target.__module__ + " import " +target.__name__ + "\n\t\t>>> from smpl import plot\n\t\t>>> plot.function("+ target.__name__ + "," + ','.join([str(a) for a in args]) + ",xmin="+str(xmin) + ",xmax=" + str(xmax)+")")

    def wrapper(target):
        if target.__doc__ is None:
            target.__doc__ = ""
        target.__doc__ += (
            "\n\n\t.. plot::\n\t\t:include-source:\n\n\t\t>>> from "
            + target.__module__
            + " import "
            + target.__name__
            + "\n\t\t>>> from smpl import plot\n\t\t>>> plot.function("
            + target.__name__
            + ("," + ",".join([str(a) for a in args]) if len(args) > 0 else "")
            + ",xmin="
            + str(xmin)
            + ",xmax="
            + str(xmax)
            + ")"
        )
        # print(target.__doc__)
        return target

    return wrapper


def insert_eq():
    """Inserts the function and its parameters and an equal sign."""

    def wrapper(target):
        if target.__doc__ is None:
            target.__doc__ = ""
        safe = target.__doc__
        target.__doc__ = target.__name__ + "("
        for v in target.__code__.co_varnames:
            target.__doc__ += v + ","
        target.__doc__ = target.__doc__[:-1]
        target.__doc__ += ") = " + safe
        return target

    return wrapper


def insert_latex_eq():
    """Inserts latexed code of a oneline function with parameters."""
    return lambda f: insert_eq()(insert_latex()(f))


def insert_latex():
    """Inserts latexed code of a oneline function."""
    from smpl import wrap

    def wrapper(target):
        if target.__doc__ is None:
            target.__doc__ = wrap.get_latex(target)
        return target

    return wrapper
