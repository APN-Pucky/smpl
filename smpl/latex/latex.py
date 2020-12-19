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
    Transposed ``si_tab``.
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

def out_si(fn,s,u="",fmt="{}"):
    mkdirs(fn)
    file = open(fn,"w")
    file.write(si(s,u,fmt))
    print(fn,": ", fmt.format(s), u)
    file.close()
def out(fn,s):
    mkdirs(fn)
    file = open(fn,"w")
    file.write(("%s"%(s)).replace("/",""))
    print(fn,": ", "%s"%(s))
    file.close()


def out_si_line(fn,tab,skip=0):
    out_si_tab(fn,np.transpose([[t] for t in tab]),skip)
def out_si_tab(fn, tab,skip=0, fmt="{}"):
    mkdirs(fn)
    file = open(fn,"w")
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            if(j!=0):
                file.write(pr("&",nnl=True))
            if(j>=skip):
                file.write(pr(si(tab[i][j],fmt=fmt),nnl=True))
            else:
                file.write(pr("%s"%(tab[i][j]),nnl=True))
        file.write(pr("\\\\\n",nnl=True))
    file.close()

def dump_vars(fd):
    key = ""
    gl = globals()
    for key in gl:
        smart_out(fd + key,gl[key])
    #print(globals())
def iter(a):
    return zip(range(len(a)),a)

def smart_out(fn,x):
    '''TODO'''
    out_si(fn,x)
    '''if isinstance(x,list):
        out_si_tab(fn,x)
    elif isinstance(x,types.FunctionType):
        out(fn,inspect.getsourcelines(x)[0])
    else:
        out_si(fn,x)
    '''

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump


def pn(a,nnl=False):
    gl = globals()
    for key in gl:
        if(gl[key]==a):
            print(key)
    if nnl:
        print("%s=%s"%(a.__name__,a),end='')    
    else:
        print("%s=%s"%(a.__name__,a))
    return a
def pr(a,nnl=False):
    if nnl:
        print(a,end='')    
    else:
        print(a)
    return a

