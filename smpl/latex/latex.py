import pathlib
import glob
import pathlib
#from io import StringIO
from smpl import debug
import numpy as np
import os
import sys
from smpl.io import mkdirs

def gf(i):
    """
    Scientific format with ``i`` digits.
    """
    return "{0:." + str(i) + "g}"

def si(s,u="",fmt="{}"):
    """
    Get number with uncertainty and unit in ``si`` format for latex.

    Parameters
    ==========
    s : ufloat
        number to be returned in a latex compatible format
    u : str
        unit of that number
    fmt : str
        format string for the numbers

    Returns
    =======
    sistr : str
        latex SI string of the number with it's uncertainty and unit.
    """
    return "\\SI{%s}{%s}"%((fmt.format(s)).replace("/","").replace("(","").replace(")",""),u)

def si_line(a,skip = 0,fmt="{}"):
    """
    Get array ``a`` in the format of a line of a latex table.
    """
    return si_tab(np.transpose([[t] for t in a]),skip,fmt)
def si_ttab(tab,skip=0, fmt="{}"):
    """
    Transposed :func:`si_tab`.
    """
    return si_tab(np.transpose(tab),skip,fmt)
def si_tab(tab,skip=0, fmt="{}"):
    """
    Get arrays of (uncertainty) numbers in  a latex table compatible form.

    Parameters
    ==========
    tab : array_like
        Array containing the values of the table
    skip : number
        Skip this many table lines
    fmt : str
        format string for the numbers

    Returns
    =======
    tabstr : str
        table latex string
    """
    #mkdirs(fn)
    #file = open(fn,"w")
    s = ""
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            if(j!=0):
                s += "&"
            if(j>=skip):
                s+=si(tab[i][j],fmt=fmt)
            else:
                s+="%s"%(tab[i][j])
        s += "\\\\\n"
    return s

