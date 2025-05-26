"""Simplified python code documentation."""

import warnings

from deprecation import deprecated as _deprecated


def append(txt):
    """
    Append ``txt`` in the ``target`` function docstring.

    Examples
    --------
    >>> @append('hi')
    ... def ho(): pass
    >>> ho.__doc__
    'hi'
    >>> @append(ho)
    ... def hi(): pass
    >>> hi.__doc__
    'hi'
    """
    if isinstance(txt, str):
        return append_str(txt)
    if hasattr(txt, "__doc__"):
        return append_doc(txt)
    warnings.warn(
        f"Can't append docstring from type {type(txt)}",
        stacklevel=2,  # Points to the caller of this function
    )
    return None


def append_str(txt):
    """
    Append ``txt`` in the ``target`` function docstring.

    Parameters
    ----------
    txt : ``str``
        ``txt`` is inserted to the ``__doc__`` of the ``target``

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

    def wrapper(target):
        if target.__doc__ is None:
            target.__doc__ = ""
        target.__doc__ += txt
        return target

    return wrapper


def append_doc(original):
    """
    Append doc string of ``original`` to ``target`` object.

    Parameters
    ----------
    original : ``class`` or ``function``
        ``original.__doc__`` is appended to the ``__doc__`` of the ``target``

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
    return append_str(original.__doc__ if original.__doc__ is not None else "")


def insert(txt):
    """
    Insert ``txt`` in the ``target`` function docstring.

    Examples
    --------
    >>> @insert('hi')
    ... def ho(): pass
    >>> ho.__doc__
    'hi'
    >>> @insert(ho)
    ... def hi(): pass
    >>> hi.__doc__
    'hi'
    """
    if isinstance(txt, str):
        return insert_str(txt)
    if hasattr(txt, "__doc__"):
        return insert_doc(txt)
    warnings.warn(
        f"Can't append docstring from type {type(txt)}",
        stacklevel=2,  # Points to the caller of this function
    )
    return None


def insert_str(txt):
    """
    Insert ``txt`` in the ``target`` function docstring.

    Parameters
    ----------
    txt : ``str``
        ``txt`` is inserted to the ``__doc__`` of the ``target``

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

    def wrapper(target):
        if target.__doc__ is None:
            target.__doc__ = ""
        target.__doc__ = txt + target.__doc__
        return target

    return wrapper


def insert_doc(original):
    """
    Inserts the docstring from passed function ``original`` in the ``target``
    function docstring.

    Parameters
    ----------
    original : ``class`` or ``function``
        ``original.__doc__`` is inserted to the ``__doc__`` of the ``target``

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
    return insert_str(original.__doc__)


def deprecated(
    version=None,
    deprecated_in=None,
    removed_in=None,
    reason=None,
    details=None,
):
    """
    Decorator to mark a function as deprecated.

    Parameters
    ----------
    version : ``str``
        Version of the package when the function was deprecated.
    deprecated_in : ``str``
        Version of the package when the function was deprecated.
    removed_in : ``str``
        Version of the package when the function will be removed.
    reason : ``str``
        Reason for deprecation.
    details : ``str``
        Details about the deprecation.

    Examples
    --------
    >>> @deprecated('0.0.0',removed_in='0.2.0')
    ... def ho():
    ...     '''Ho'''
    ...     print(ho.__doc__)
    >>> ho()
    Ho
    <BLANKLINE>
    .. deprecated:: 0.0.0
       This will be removed in 0.2.0.

    """
    # merge details and reason
    if details is None:
        details = reason
    elif reason is not None:
        details = reason + " " + details

    # merge deprecated_in and version
    if version is None:
        version = deprecated_in

    # increment minor version
    # if removed_in is None:
    #    removed_in = ".".join(
    #        [version.split(".")[0]]
    # + [str(int(version.split(".")[1]) + 2)] + ["0"]
    #    )

    return _deprecated(
        deprecated_in=version,
        removed_in=removed_in,
        # current_version=_version("pyfeyn2"),
        details=details,
    )


tab_len = 20


def table_sep(tabs=1):
    return (
        "=" * (tab_len - 2)
        + "  "
        + "=" * (tab_len - 2)
        + "  "
        + "=" * (tab_len - 2)
        + "\n"
        + "\t".join(["" for i in range(tabs + 1)])
    )


@deprecated(
    version="1.0.3.1",
    removed_in="?.?.?",
    reason="Use :func:`smpl_doc.array_table` instead.",
)
def table(dic, top=True, bottom=True, init=True, tabs=1):
    """
    Add dict= {'key': [values...]} to a simple reST table.

    Parameters
    ----------
    dic : ``dict``
        Dictionary to be converted to a table.
    top : ``bool``
        If ``True`` a top line is added.
    bottom : ``bool``
        If ``True`` a bottom line is added.
    init : ``bool``
        If ``True`` a tab is added at the beginning of the line.
    tabs : ``int``
        Number of tabs to be added at the beginning of the line.

    Returns
    -------
    ``str``
        The table as a string.
    >>> table({'a': [1, 2, 3], 'b': [4, 5, 6]})
    '\\t==================  ==================  ==================\\n\
\\ta                   1                   2                   3\\n\
\\tb                   4                   5                   6\\n\
\\t==================  ==================  ==================\\n\\t\\n'
    """
    t = "\t" * tabs
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
    return "\n".join([ll.rstrip() for ll in s.split("\n")])


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
    >>> print(trim_eol_spaces(array_table([["a","b"],["hihi", "hoho"]]\
        ,tabs=0)))
    ====== ======
    a      b
    ====== ======
    hihi   hoho
    ====== ======
    <BLANKLINE>
    >>> print(trim_eol_spaces(array_table({"a":["hihi",2],"b": ["hoho",3]}\
        ,tabs=0,header=False)))
    === ====== ===
    a   hihi   2
    b   hoho   3
    === ====== ===
    <BLANKLINE>

    """
    if isinstance(arr, dict):
        arr = dict_to_table(arr)
    width = len(arr[0])
    height = len(arr)
    widths = [0 for i in range(width)]
    # maximum width of each column
    for i in range(width):
        for j in range(height):
            widths[i] = max(len(str(arr[j][i])), widths[i])
    rs = ""
    if init:
        rs += "\t" * tabs
    if top:
        rs += " ".join(["=" * (widths[i] + 2) for i in range(width)]) + "\n"

    for i in range(height):
        rs += "\t" * tabs
        for j in range(width):
            rs += str(arr[i][j]) + " " * (widths[j] - len(str(arr[i][j])) + 3)
        rs += "\n"
        if header and i == 0:
            rs += (
                "\t" * tabs
                + " ".join(["=" * (widths[i] + 2) for i in range(width)])
                + "\n"
            )

    if bottom:
        rs += "\t" * tabs
        rs += " ".join(["=" * (widths[i] + 2) for i in range(width)]) + "\n"
    return rs


if __name__ == "__main__":
    import doctest

    doctest.testmod()
