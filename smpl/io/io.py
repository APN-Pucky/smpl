import pathlib
import glob
import pathlib
#from io import StringIO
from smpl import debug
import numpy as np
import os
import sys

def pwd():
    """
        Returns the path to the path of current file
    """
    pwd_="/".join(debug.get_line_number_file(split=False,_back=1)[1].split("/")[:-1])
    return pwd_

def import_path(path='../..'):
    """
        Adds ``path`` to the ``sys.path``
    """
    sys.path.insert(0, os.path.abspath(path))


def gf(i):
    """
    Scientific format with ``i`` digits.
    """
    return "{0:." + str(i) + "g}"
def mkdirs(fn):
    '''
    Creates the neccessary directories above ``fn``.
    '''
    pathlib.Path(fn).parent.mkdir(parents=True, exist_ok=True)

def pr(a,nnl=False):
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
    """
    if nnl:
        print(a,end='')    
    else:
        print(a)
    return a
def si(s,u="",fmt="{}"):
    """
    Get nuber with uncertainty and unit in ``si`` format for latex.
    Returns
    =======
    sistr : str
        latex SI string of the number with it's uncertainty and unit.
    """
    return "\\SI{%s}{%s}"%((fmt.format(s)).replace("/","").replace("(","").replace(")",""),u)

def files(folder,ending):
    """
    Get all the files in ``folder`` ending with ``ending``.
    """
    r = []
    i=0
    for file in os.scandir(folder):
        if file.path.endswith(ending):
            r.append((i,os.path.splitext(os.path.basename(file.path))[0],file.path))
            i=i+1
    return r


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

