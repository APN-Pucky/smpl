import pathlib
#from io import StringIO
from smpl import debug
import numpy as np
import os
import sys
from pathlib import Path


def find_file(fname, up=0):
    """
    Searches for ``fname`` in all down folders or up folder to given order respectively.
    """

    p = Path(fname).parent
    n = Path(fname).name
    if (p / n).is_file():
        return str(p / n)
    for _ in range(up):
        p = p.parent

    for f in p.rglob(n):
        if f.is_file():
            return str(f)
    return None


def pwd():
    """
    Returns the path to the path of current file
    """
    pwd_ = "/".join(debug.get_line_number_file(split=False,
                    _back=1)[1].split("/")[:-1])
    return pwd_


def import_path(path='../..'):
    """
        Adds ``path`` to the ``sys.path``
    """
    sys.path.insert(0, os.path.abspath(path))


def gf(i):
    """
    Scientific format with ``i`` digits.

    Examples
    ========

    >>> gf(2)
    '{0:.2g}'
    >>> gf(2).format(789234578934)
    '7.9e+11'
    >>> gf(5).format(789234578934)
    '7.8923e+11'

    """
    return "{0:." + str(i) + "g}"


def mkdirs(fn):
    """
    Creates the neccessary directories above ``fn``.
    """
    pathlib.Path(fn).parent.mkdir(parents=True, exist_ok=True)


def pr(a, nnl=False):
    """
    Prints the passed ``a``.

    Parameters
    ==========
    nnl : bool
        no-new-line

    Returns
    =======
    a : any
        unchanged ``a``.

    Examples

    >>> 5 + pr(4)
    4
    9
    >>> 5 + pr(4, nnl=True)
    49

    """
    if nnl:
        print(a, end='')
    else:
        print(a)
    return a


def si(s, u="", fmt="{}"):
    """
    Get nuber with uncertainty and unit in ``si`` format for latex.

    Returns
    =======
    sistr : str
        latex SI string of the number with it's uncertainty and unit.

    Examples
    ========
    >>> import uncertainties as unc
    >>> si(unc.ufloat(2000,0.1))
    '\\SI{2000.00+-0.10}{}'
    >>> si(unc.ufloat(2000,0.1),"\\meter")
    '\\SI{2000.00+-0.10}{\\meter}'
    >>> si(unc.ufloat(2000,0.1),"\\meter", gf(2))
    '\\SI{2.0+-0.0e+03}{\\meter}'

    """
    return "\\SI{%s}{%s}" % ((fmt.format(s)).replace("/", "").replace("(", "").replace(")", ""), u)


def files(folder, ending):
    """
    Get all the files in ``folder`` ending with ``ending``.
    """
    r = []
    i = 0
    for file in os.scandir(folder):
        if file.path.endswith(ending):
            r.append((i, os.path.splitext(
                os.path.basename(file.path))[0], file.path))
            i = i+1
    return r


def out_si(fn, s, u="", fmt="{}"):
    mkdirs(fn)
    file = open(fn, "w")
    file.write(si(s, u, fmt))
    print(fn, ": ", fmt.format(s), u)
    file.close()


def out(fn, s):
    mkdirs(fn)
    file = open(fn, "w")
    file.write(("%s" % (s)).replace("/", ""))
    print(fn, ": ", "%s" % (s))
    file.close()


def out_si_line(fn, tab, skip=0):
    out_si_tab(fn, np.transpose([[t] for t in tab]), skip)


def out_si_tab(fn, tab, skip=0, fmt="{}"):
    mkdirs(fn)
    file = open(fn, "w")
    for i, ti in enumerate(tab):
        for j, tij in enumerate(ti):
            if(j != 0):
                file.write(pr("&", nnl=True))
            if(j >= skip):
                file.write(pr(si(tij, fmt=fmt), nnl=True))
            else:
                file.write(pr("%s" % (tij), nnl=True))
        file.write(pr("\\\\\n", nnl=True))
    file.close()


def dump_vars(fd):
    key = ""
    gl = globals()
    for key in gl:
        smart_out(fd + key, gl[key])
    # print(globals())


def iteri(a):
    return zip(range(len(a)), a)


def smart_out(fn, x):
    """TODO"""
    out_si(fn, x)


def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


def pn(a, nnl=False):
    gl = globals()
    for key in gl:
        if(gl[key] == a):
            print(key)
    if nnl:
        print("%s=%s" % (a.__name__, a), end='')
    else:
        print("%s=%s" % (a.__name__, a))
    return a
