from inspect import currentframe, getsource
import os
import numpy as np

# TODO comapare against logging module https://docs.python.org/3.5/library/logging.html

# TODO instead of hard coded global variables, use function arguments

"""
DEBUG_LEVEL=-1 no debug
DEBUG_LEVEL= 0 default level
DEBUG_LEVEL= 1,2,3 higher levels, more debug
"""
DEBUG_LEVEL = -1


#print prefix
DEBUG_PRE = "DBG"

# remove folders of files for print

# filename strings with .py (with folder if SPLIT_FILENAME==False)
WHITE_LIST_FILES = []
BLACK_LIST_FILES = []

active = debug = on = DEBUG_LEVEL >= 0
# count debug events by file+line
count_times = {}
cur_table_line = {}


def get_frame(_back=0):
    cf = currentframe()
    for _ in range(_back+1):
        cf = cf.f_back
    return cf


def once(_back=0):
    """
    Returns true only one time

    Examples
    --------
    >>> for i in range(10):
    ...     if once():
    ...         print(i)
    0

    """
    return times(1, _back=_back+1)

def times(t=1, _back=0):
    """
    Returns true if the count of the current line is greater than or equal to ``t``.
    
    Parameters
    ----------
    t : int
        The count to check against.
    _back : int
        Number of stack/frames to go back.

    Returns
    -------
    bool
        True if the count of the current line is greater than or equal to ``t``.

    Examples
    --------
    >>> reset_times()
    >>> for i in range(10):
    ...     if times(3):
    ...         print(i)
    0
    1
    2
    """
    line, fname = get_line_number_file(_back=_back+1)
    inc_count(line, fname)
    return check_count(line, fname, t)


def get_line_src(_back=0):
    """
    Gets the current line in the python source.

    Parameters
    ----------
    _back : int
        Number of stack/frames to go back.

    Returns
    -------
    src : str
        The current line in the python source.

    Examples
    --------
    >>> get_line_src()
    'get_line_src()'
    >>> "funky"+get_line_src()
    'funky"funky"+get_line_src()'
    """
    cf = get_frame(_back=_back+1)
    srcline = getsource(cf).split(
        "\n")[cf.f_lineno-cf.f_code.co_firstlineno].strip()
    return srcline


def get_line_number_file(split=True, _back=0):
    """
    Gets the current filename and the current linenumber within it.

    Parameters
    ----------
    split : bool
        Indicates whenever the folders above of the file should be included in the returned filename.
    _back : int
        Number of stack/frames to go back.

    Returns
    -------
    filenumber : int
        First element in the return array
    filename : str
        Second element in the return array

    Examples
    --------
    >>> get_line_number_file()
    (1, '<doctest smpl.debug.debug.get_line_number_file[0]>')
    >>> for i in range(2):
    ...     get_line_number_file()
    (2, '<doctest smpl.debug.debug.get_line_number_file[1]>')
    (2, '<doctest smpl.debug.debug.get_line_number_file[1]>')
    """
    cf = get_frame(_back=_back+1)
    fname = cf.f_code.co_filename
    if split:
        fname = cf.f_code.co_filename.split("/")[-1]
    return cf.f_lineno, fname


def get_line_number(_back=0):
    return get_line_number_file(_back=_back+1)[0]


def line(msg_, tag="", level=0, times=-1, _back=0, **kwargs):
    msg(msg_, tag=tag, level=level, times=times,
        line_=True, _back=_back+1, **kwargs)
# only once
def line1(msg_, tag="", level=0, times=1, _back=0, **kwargs):
    """
    Just like :func:`line` but ``times`` set to 1.

    Examples
    --------
    >>> for i in range(-2,2):
    ...     line1(i,level=-1)
    DBG::<doctest smpl.debug.debug.line1[0]>:2: line1(i,level=-1) = -2
    """
    msg1(msg_, tag=tag, level=level, times=times,
         line_=True, _back=_back+1, **kwargs)

# counting functions


def get_count(line, fname):
    """
    Returns the counts of the line.

    Parameters
    ----------
    line : int
        The line in the python source of ``fname``.
    fname : str
        The filename.

    Returns
    -------
    count : int
        The count of the current line.

    Examples
    --------
    >>> get_count(1, "debug.py")
    0
    """
    global count_times
    if fname+":"+str(line) in count_times:
        return count_times[fname+":"+str(line)]
    return 0


def inc_count(line, fname):
    """
    Increments the count of the line.

    Parameters
    ----------
    line : int
        The line in the python source of ``fname``.
    fname : str
        The filename.

    Examples
    --------
    >>> inc_count(1, "debug.py")
    """
    global count_times
    if fname+":"+str(line) in count_times:
        count_times[fname+":"+str(line)] += 1
    else:
        count_times[fname+":"+str(line)] = 1


def check_count(line, fname, t):
    """
    Returns true if the count of the line is greater than or equal to ``t``.

    Parameters
    ----------
    line : int
        The line in the python source of ``fname``.
    fname : str
        The filename.
    t : int
        The count to check against.

    Returns
    -------
    bool
        True if the count of the line is greater than or equal to ``t``.

    Examples
    --------
    >>> check_count(2, "debug.py", 0)
    True
    >>> inc_count(2, "debug.py")
    >>> check_count(2, "debug.py", 0)
    False

    """
    if t >= get_count(line, fname) or t == -1:
        if(not fname in BLACK_LIST_FILES and (len(WHITE_LIST_FILES) == 0 or fname in WHITE_LIST_FILES)):
            return True
    return False


# _line enables printint src line
# t stands for times
def msg(msg, tag="", level=0, times=-1, line_=False, _back=0,**kwargs):
    """
    Prints the message ``msg`` if level > debug_level and always returns the msg.

    Parameters
    ----------
    tag : str
        Sets a tag to be printed for the debug message.
    level : int
        Debug level.
    times : int
        How often should the message be printed if the function gets called multiple times (e.g. in a loop).
    _line : bool
        Print the current line in the python source.
    _back : int
        Number of stack/frames to go back.

    Examples
    --------
    >>> msg("hi", level = -9999)
    DBG::<doctest smpl.debug.debug.msg[0]>:1: hi
    'hi'
    >>> msg("hi")
    'hi'

    """
    if(level <= DEBUG_LEVEL):
        line, fname = get_line_number_file(_back=_back+1)
        src = ""
        if line_ == True:
            src = get_line_src(_back=_back+1)
            src = src+ " = "
        inc_count(line, fname)
        if(check_count(line, fname, times)):
            print(DEBUG_PRE + ":" + tag + ":" + fname +
                  ":" + str(line) + ": " + src + str(msg))
    return msg


def msg1(_msg, tag="", level=0, times=1, line_=False, _back=0, **kwargs):
    """
    Just like :func:`msg` but ``times`` set to 1.

    Parameters
    ----------
    tag : str
        Sets a tag to be printed for the debug message.
    level : int
        Debug level.
    times : int
        How often should the message be printed if the function gets called multiple times (e.g. in a loop).
    _line : bool
        Print the current line in the python source.
    _back : int
        Number of stack/frames to go back.

    Examples
    --------
    >>> for i in range(-2,2):
    ...     msg1(i, level = i)
    DBG::<doctest smpl.debug.debug.msg1[0]>:2: -2
    -2
    -1
    0
    1
    """
    return msg(_msg, level=level, tag=tag, times=times, line_=line_, _back=_back+1, **kwargs)


def file(key, value, level=0, times=-1, seperator=";", _print=True, _back=0, filename="debug.csv"):
    """
    Prints the message ``msg`` if level > debug_level to file ``filename``.
    """
    if(level <= DEBUG_LEVEL):
        line, fname = get_line_number_file(_back=_back+1)
        inc_count(line, fname)
        if(check_count(line, fname, times)):
            f = open(filename, "a+")
            if(_print):
                tag = "debug.file"
                print(DEBUG_PRE + ":" + tag + ":" + fname + ":" +
                      str(line) + ": " + key + seperator + value)
            f.write(key + seperator + value + "\n")
            f.close()
    return value


def file1(_key, _value, level=0, times=1, _back=0, **kwargs):
    """
    Just like :func:`file` but ``times`` set to 1.
    """
    return file(_key, _value, level=level, times=times, _back=_back+1, **kwargs)


def table_flush_header(filename="debug_table.csv", seperator=";"):
    """
    Saves the current keys from :func:`table` to ``filename``.
    """
    global cur_table_line
    f = open(filename, "a+")
    for key in sorted(cur_table_line):
        f.write(key + seperator)
    f.write('\n')
    f.close()


def table_flush_line(filename="debug_table.csv", seperator=";"):
    """
    Saves the current values from :func:`table` to ``filename``
    """
    global cur_table_line
    f = open(filename, "a+")
    itt = iter(cur_table_line)
    ok = False
    while not ok:
        cur = next(itt)
        ok = isinstance(cur_table_line[cur], np.ndarray)
    dim = len(cur_table_line[cur])
    for i in range(dim):
        for key in sorted(cur_table_line):
            if isinstance(cur_table_line[key], np.ndarray):
                f.write("%.30e" % cur_table_line[key][i] + seperator)
            else:
                f.write("%.30e" % cur_table_line[key] + seperator)
        f.write('\n')
    f.close()


def table(key, value, level=0, times=-1, seperator=";", _print=False, _back=0, filename="debug_table.csv"):
    """
    Saves ``key``:``value`` in ``filename``.
    """
    global cur_table_line
    if(level <= DEBUG_LEVEL):
        line, fname = get_line_number_file(_back=_back+1)
        inc_count(line, fname)
        if(check_count(line, fname, times)):
            if isinstance(value, np.ndarray):
                cur_table_line[key] = value.copy()
            else:
                cur_table_line[key] = value
    return value


def reset_times():
    """
    Resets global `count_times`.
    """
    global count_times
    count_times = {}


reset_count=reset_times

if os.path.exists("debug.csv"):
    os.remove("debug.csv")
if os.path.exists("debug_table.csv"):
    os.remove("debug_table.csv")

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
