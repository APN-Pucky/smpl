from multiprocessing import Process,Queue

def queued(q,f,*args,**kwargs):
    q.put(f(*args,**kwargs))
def res(a):
    if isinstance(a,list):
        return [next(k) for k in a]
    return next(a)
def gen(f,*args,**kwargs):
    """
        Generates parallel execution list generator
    """
    q = Queue()
    p = Process(target=queued,args=(q,f,*args),kwargs=kwargs)
    yield p.start()
    yield [q.get(),p.join()][0]
def calc(f,*args,**kwargs):
    """
        Parallel evaluation of the list generator from :func:`gen`
    """
    g=gen(f,*args,**kwargs)
    next(g)
    return g
def par(f,*args,**kwargs):
    """
        Parallel execution of f on each element of args and kwargs
    """
    return res([calc(f,*[args[k][i] for k in range(len(args))],**{k:v[i] for k,v in kwargs.items()}) for i in range(len(args[0]) if len(args)>0 else len(next(iter(kwargs.values()))))])
 
 
 
 