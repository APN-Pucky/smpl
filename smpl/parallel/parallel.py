from multiprocessing import Process, Queue
import multiprocessing

import numpy as np
from smpl.doc import append_doc


def queued(q, f, *args, **kwargs):
    q.put(f(*args, **kwargs))


def res(a):
    """
    Parallel evaluation of the list generator from :func:`gen`.

    Return parallel executed values.

    Examples
    --------
    >>> def twice(x):
    ...     return x+x
    >>> for r in [calc(twice,i) for i in range(0,5)]:
    ...     print(res(r))
    0
    2
    4
    6
    8
    >>> res([calc(lambda x : x**3, i) for i in range(0,5)])
    [0, 1, 8, 27, 64]

    """
    if isinstance(a, list):
        return [next(k) for k in a]
    return next(a)


def gen(f, *args, **kwargs):
    """Generates parallel execution list generator."""
    q = Queue()
    p = Process(target=queued, args=(q, f, *args), kwargs=kwargs)
    yield p.start()
    yield [q.get(), p.join()][0]


@append_doc(res)
def calc(f, *args, **kwargs):
    g = gen(f, *args, **kwargs)
    next(g)
    return g


def par(f, *args, **kwargs):
    """
    Parallel execution of f on each element of args and kwargs

    Examples
    --------
    >>> par(lambda x : x**2, range(0,5))
    [0, 1, 4, 9, 16]

    """
    return res([calc(f, *[args[k][i] for k in range(len(args))], **{k: v[i] for k, v in kwargs.items()}) for i in range(len(args[0]) if len(args) > 0 else len(next(iter(kwargs.values()))))])

# TODO rework to same properties as par
def partitioned_parallel(f,arr,n_jobs=None):
    """
    Parallel execution of f on each element of args

    Examples
    --------
    >>> partitioned_parallel(lambda x : x**2, range(0,5))
    [0, 1, 4, 9, 16]

    """
    n_jobs = n_jobs or multiprocessing.cpu_count()
    sa = np.array_split(np.array(arr),len(arr)/n_jobs)
    res = []
    for i in range(len(sa)):
        res += par(f,sa[i])
    return res

parallel = partitioned_parallel

if __name__ == "__main__":
    import doctest
    doctest.testmod()
