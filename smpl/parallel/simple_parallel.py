from multiprocessing import Process,Queue

def queued(q,f,*args,**kwargs):
    q.put(f(*args,**kwargs))
def res(a):
    return next(a)
def gen(f,*args,**kwargs):
    q = Queue()
    p = Process(target=queued,args=(q,f,*args),kwargs=kwargs)
    yield p.start()
    yield [q.get(),p.join()][0]
def calc(f,*args,**kwargs):
    g=gen(f,*args,**kwargs)
    next(g)
    return g
