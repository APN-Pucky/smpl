import pathlib
import glob
from pathlib import Path
from io import StringIO
# %% Ouput
def gf(i):
    return "{0:." + str(i) + "g}"
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
def si(s,u="",fmt="{}"):
    return "\\SI{%s}{%s}"%((fmt.format(s)).replace("/","").replace("(","").replace(")",""),u)


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
def mkdirs(fn):
    pathlib.Path(fn).parent.mkdir(parents=True, exist_ok=True)
def dump_vars(fd):
    key = ""
    gl = globals()
    for key in gl:
        smart_out(fd + key,gl[key])
    #print(globals())
def iter(a):
    return zip(range(len(a)),a)
def files(folder,ending):
    r = []
    i=0
    for file in os.scandir(folder):
        if file.path.endswith(ending):
            r.append((i,os.path.splitext(os.path.basename(file.path))[0],file.path))
            i=i+1
    return r
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

