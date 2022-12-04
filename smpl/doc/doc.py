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
    """TODO split cases doc/txt/plot?"""
    return None


def append_str(txt):
    return _append(txt)


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


def append_doc(original):
    """
    Append doc string of ``original`` to ``target`` object.

    Parameters
    ----------
    original : ``class`` or ``function``
        ``orignal.__doc__`` is appended to the ``__doc__`` of the ``target``

    Examples
    --------
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

    Parameters
    ----------
    original : ``class`` or ``function``
        ``orignal.__doc__`` is inserted to the ``__doc__`` of the ``target``

    Examples
    --------
    >>> def ho():
    ...     '''Ho'''
    ...     print(ho.__doc__)
    >>> @insert_doc(ho)
    ... def hi():
    ...     '''Hi'''
    ...     print(hi.__doc__)
    >>> hi()
    HoHi
    """
    return _insert(original.__doc__)


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


tab_len = 20


def table_sep(tabs=1):
    return (
        "=" * (tab_len - 2)
        + "  "
        + "=" * (tab_len - 2)
        + "  "
        + "=" * (tab_len - 2)
        + "\n"
        + "\t".join(["" for i in range(0, tabs + 1)])
    )


def table(dic, top=True, bottom=True, init=True, tabs=1):
    """
    Add dict= {'key': [values...]} to a simple reST table.

    ..deprecated:: 0.0.0

    """
    t = util.times("\t", tabs)
    rs = ""
    if init:
        rs += t
    if top:
        rs += table_sep(tabs=tabs)
    for k, vs in dic.items():
        rs += str(k)
        p = str(k)
        for v in vs:
            sv = str(v)
            if "<function " in sv and "at 0x" in sv:
                sv = sv.split("<function ")[1].split("at 0x")[0]
            rs += "".join([" " for i in range(tab_len - len(p))]) + sv
            p = sv
        rs += "\n" + t
    if bottom:
        rs += table_sep(tabs=tabs) + "\n"
    else:
        rs += ""
    return rs


def dict_to_table(dic):
    rt = []
    for k, vs in dic.items():
        rt += [[k, *vs]]
    return rt


def trim_eol_spaces(s):
    """
    Trim spaces at the end of lines.

    This is only needed for the docstrings, because black does trim them.

    """
    return "\n".join([l.rstrip() for l in s.split("\n")])


def array_table(arr, top=True, bottom=True, init=True, tabs=1, header=True):
    """
    Produces a reST table from a numpy array or normal 2d array.

    Parameters
    ----------
    arr : ``numpy.ndarray``, ``list`` or ``dict``
        2d array or dict
    top : ``bool``
        If ``True`` a top line is added.
    bottom : ``bool``
        If ``True`` a bottom line is added.
    init : ``bool``
        If ``True`` a tab is added at the beginning of each line.
    tabs : ``int``
        Number of tabs at the beginning of each line.
    header : ``bool``
        If ``True`` the first row is used as header.

    Examples
    --------
    >>> print(trim_eol_spaces(array_table([["a","b"],["hihi", "hoho"]],tabs=0)))
    ====== ======
    a      b
    ====== ======
    hihi   hoho
    ====== ======
    <BLANKLINE>

    """
    if type(arr) is dict:
        arr = dict_to_table(arr)
    width = len(arr[0])
    height = len(arr)
    widths = [0 for i in range(width)]
    # maximum width of each column
    for i in range(0, width):
        for j in range(0, height):
            if len(str(arr[j][i])) > widths[i]:
                widths[i] = len(str(arr[j][i]))
    rs = ""
    if init:
        rs += "\t" * tabs
    if top:
        rs += " ".join(["=" * (widths[i] + 2) for i in range(0, width)]) + "\n"

    for i in range(0, height):
        rs += "\t" * tabs
        for j in range(0, width):
            rs += str(arr[i][j]) + " " * (widths[j] - len(str(arr[i][j])) + 3)
        rs += "\n"
        if header and i == 0:
            rs += (
                "\t" * tabs
                + " ".join(["=" * (widths[i] + 2) for i in range(0, width)])
                + "\n"
            )

    if bottom:
        rs += "\t" * tabs
        rs += " ".join(["=" * (widths[i] + 2) for i in range(0, width)]) + "\n"
    return rs


if __name__ == "__main__":
    import doctest

    doctest.testmod()
