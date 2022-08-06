import pathlib
#from io import StringIO
from smpl import debug
import os
import sys
from pathlib import Path

from smpl.doc.doc import append

def read(fname):
    """
    Reads the file ``fname``.

    Parameters
    ----------
    fname : str
        file name.

    Returns
    -------
    str
        content of the file.

    Examples
    --------
    >>> read("nonexistent.txt")
    ''
    >>> write("test.out","hi")
    >>> read("test.out")
    'hi'
    """
    if(not os.path.exists(fname)):
        return ""
    with open(fname, 'r') as f:
        return f.read()

def append(destination,content):
    """
    Write to file by string or writable :obj:`destiantion`.

    Parameters
    ----------
    destination : str, writeable
        destination to write to.
    content : str
        text to be written.

    Examples
    --------
    >>> append(sys.stdout,"hi")
    hi
    >>> append("test.out","hi")
    >>> read("test.out")
    'hi'
    """
    # TODO add http and other string based write methodes
    if isinstance(destination,str):
        with open(destination, 'w+') as f:
            f.write(content)
    else:
        destination.write(content)
write = append

def gf(i=3):
    """
    Scientific number format.

    Parameters
    ----------
    i : int
        Number of digits.

    Returns
    -------
    str
        Scientific number format string.

    Examples
    --------
    >>> gf(2)
    '{0:.2g}'
    >>> gf(2).format(789234578934)
    '7.9e+11'
    >>> gf(5).format(789234578934)
    '7.8923e+11'

    """
    return "{0:." + str(i) + "g}"


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
    Returns the path to the path of current file (in linux format).

    Returns
    -------
    str
        path to the path of current file.
    """
    #TODO better use pathlib.Path.cwd()
    pwd_ = "/".join(debug.get_line_number_file(split=False,
                    _back=1)[1].split("/")[:-1])
    return pwd_


def import_path(path='../..'):
    """
    Adds ``path`` to the ``sys.path``.

    Parameters
    ----------
    path : str
        path to add.

    Examples
    --------
    >>> import_path('../../smpl')
    """
    sys.path.insert(0, os.path.abspath(path))


def mkdirs(fn):
    """
    Creates the neccessary directories above ``fn``.

    Parameters
    ----------
    fn : str    
        file name.

    Examples
    --------
    >>> mkdirs("test.out")
    """
    pathlib.Path(fn).parent.mkdir(parents=True, exist_ok=True)


def pr(a, nnl=False):
    """
    Prints the passed ``a``.

    Parameters
    ----------
    nnl : bool
        no-new-line

    Returns
    -------
    a : any
        unchanged ``a``.

    Examples
    --------
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


def files(folder, ending):
    """
    Get all the files in ``folder`` ending with ``ending``.

    Parameters
    ----------
    folder : str
        folder name.    
    ending : str
        ending of the files.

    Returns
    -------
    list
        list of files.

    Examples
    --------
    >>> files(".",".py")
    [(0, 'setup', './setup.py')]
    """
    r = []
    i = 0
    for file in os.scandir(folder):
        if file.path.endswith(ending):
            r.append((i, os.path.splitext(
                os.path.basename(file.path))[0], file.path))
            i = i+1
    return r


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
