"""Simplified input and output."""

import contextlib
import os
import pathlib
import re
import shutil
import sys
from io import StringIO
from pathlib import Path

import requests

from .cat import *
from .grep import *
from .head import *
from .sed import *
from .tail import *


def read(to_be_read: str):
    """
    Open either a file or URI and return the content.
    Reads the file ``to_be_read``.

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
    >>> read("https://raw.githubusercontent.com/APN-Pucky/smpl_io/master/LICENSE").split("\\n")[0].strip()
    'GNU GENERAL PUBLIC LICENSE'

    """
    if to_be_read is sys.stdout:
        return ""
    if to_be_read.startswith("http"):
        return requests.get(to_be_read).text
    if to_be_read == "-":
        return sys.stdin.read()
    if not os.path.exists(to_be_read):
        return ""
    with open(to_be_read, "r") as f:  # TODO should be checked here
        return f.read()


@contextlib.contextmanager
def pushd(new_dir, tmp=False, cd=True):
    """
    Move to a new directory and return to the previous one after context.

    Parameters
    ----------
    new_dir : str
        new directory.
    tmp: bool, optional
        create the directory if it does not exist and delete after context, by default False
    cd: bool, optional
        change to (new) directory, by default True

    Examples
    --------
    >>> import os
    >>> p = os.getcwd()
    >>> with pushd("tmptest",tmp=True):
    ...     pp = os.getcwd()
    ...     pp.startswith(p) and pp.endswith("tmptest")
    True
    >>> import os
    >>> p = os.getcwd()
    >>> with pushd("tmptest",tmp=True,):
    ...     pp = os.getcwd()
    ...     pp.startswith(p) and pp.endswith("tmptest")
    True
    """

    previous_dir = os.getcwd()
    if tmp:
        abspath = os.path.abspath(new_dir)
        os.makedirs(abspath, exist_ok=False)
    if cd:
        os.chdir(new_dir)
    try:
        yield
    finally:
        if cd:
            os.chdir(previous_dir)
        if tmp:
            shutil.rmtree(abspath, ignore_errors=True)


def glob_re(pattern, path):
    """
    Returns all strings that match the regex pattern.

    Parameters
    ----------
    pattern : str
        regex pattern.
    path : str
        path to search in.

    Returns
    -------
    list
        list of filenames that match the regex pattern.

    Examples
    --------
    >>> import os
    >>> with pushd("tmptest",tmp=True,cd=False):
    ...     write("tmptest/test.txt","hi\\nho1\\n2\\n3\\n4\\n")
    ...     glob_re(".*[xt][xt][xt]", "tmptest")
    ['test.txt']

    """
    return list(filter(re.compile(pattern).match, os.listdir(path)))


def write(destination, content, mode="w+", create_dir=True):
    """
    Write to file by string or writable :obj:`destiantion`.

    Parameters
    ----------
    destination : str, writeable
        destination to write to.
    content : str
        text to be written.
    mode : str
        mode to open the file.
        Default is 'w+' (write and read).
    create_dir : bool
        create directory if it does not exist.

    Examples
    --------
    >>> write(sys.stdout,"hi")
    hi
    >>> write("-","hi")
    hi
    >>> write("test.out","hi")
    >>> read("test.out")
    'hi'
    """
    # TODO add http and other string based write methodes
    if isinstance(destination, str):
        if destination == "-":
            print(content)
            return
        if create_dir:
            try:
                os.makedirs(os.path.dirname(destination), exist_ok=True)
            except FileNotFoundError:
                # this happens when the path is a local path, ie. a single file
                pass
        with open(destination, mode) as f:
            f.write(content)
    else:
        destination.write(content)


def append(destination, content, mode="a+"):
    """
    Appends to file by string or writable :obj:`destiantion`.

    Parameters
    ----------
    destination : str, writeable
        destination to write to.
    content : str
        text to be written.
    mode : str
        mode to open the file.
        Default is 'a+' (append and read).

    Examples
    --------
    >>> append(sys.stdout,"hi")
    hi
    """
    write(destination, content, mode)


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

    Parameters
    ----------
    fname : str
        file name.
    up : int
        number of up folders to search.

    Returns
    -------
    str
        path to the file.

    Examples
    --------
    >>> import os
    >>> find_file("io.py",0)
    'smpl/io/io.py'
    >>> os.chdir("smpl/io")
    >>> find_file("io.py",0)
    'io.py'
    >>> find_file("Makefile",2)
    '../../Makefile'
    >>> os.chdir("../..")

    """
    p = Path(os.path.abspath(fname)).parent
    n = Path(os.path.abspath(fname)).name
    if (p / n).is_file():
        return str(os.path.relpath(p / n, os.path.abspath(".")))
    for _ in range(up):
        p = p.parent

    for f in p.rglob(n):
        if f.is_file():
            return str(os.path.relpath(f, os.path.abspath(".")))
    return None


def pwd() -> str:
    """
    Returns the path to the path of current file (in linux format).

    Returns
    -------
    str
        path to the path of current file.

    Examples
    --------
    >>> pwd().endswith("io")
    True

    """
    # pwd_ = "/".join(debug.get_line_number_file(split=False, _back=1)[1].split("/")[:-1])
    path = Path(__file__).parent.absolute()
    return str(path)


def import_path(path="../.."):
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
        print(a, end="")
    else:
        print(a)
    return a


def files(ending, folder="."):
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
    >>> files(".toml")
    [(0, 'pyproject', './pyproject.toml')]
    """
    r = []
    i = 0
    for file in os.scandir(folder):
        if file.path.endswith(ending):
            r.append((i, os.path.splitext(os.path.basename(file.path))[0], file.path))
            i = i + 1
    return r


def pn(a, nnl=False):
    """
    Find variable with the same value as ``a`` in globals.
    Then print its name and value.

    Parameters
    ----------
    a : any
        variable to find.
    nnl : bool
        no-new-line

    Returns
    -------
    a : any
        unchanged ``a``.
    """
    gl = globals()
    for key in gl:
        if gl[key] == a:
            print(key)
    if nnl:
        print(f"{a.__name__}={a}", end="")
    else:
        print(f"{a.__name__}={a}")
    return a


def remove(file):
    """
    Removes ``file``.

    Parameters
    ----------
    file : str
        file name.

    Examples
    --------
    >>> remove("test.out")
    """
    if os.path.exists(file):
        os.remove(file)


alias_open = open


def open(to_be_read: str, mode="r"):
    """
    Return opened buffer of either file or URI.

    Parameters
    ----------
    to_be_read : str
        file name or URI.
    mode : str
        mode to open the file.

    Returns
    -------
    buffer
        opened buffer.
    """
    if mode != "r":
        return alias_open(to_be_read, mode)
    if to_be_read.startswith("http"):
        return StringIO(requests.get(to_be_read).text)
    if not os.path.exists(to_be_read):
        return StringIO("")
    return alias_open(to_be_read, "r")
