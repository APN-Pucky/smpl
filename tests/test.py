import numpy as np
import matplotlib.pyplot as plt
from smpl import plot
from smpl import functions as f

from smpl import test
from smpl.parallel import *
import smpl




data = np.loadtxt('tests/test_linear.txt')
ff = plot.fit(data[:,0], data[:,1], fmt='.', function=f.Gerade, units=["l","b"],sigmas=1,lpos=2,residue=True,residue_err=False,xaxis="t",yaxis="s")

plt.show()

testl = lambda x,a,b : a*x+b
print(testl.__code__.co_argcount)
def long_calc(x):
    if x > 50:
        for i in range(1000000):
            i = i+x
            i = i*x
            i = i/x
            i = i-x
    return x*x

print(res([calc(long_calc,x) for x in range(1,100)]))
print(par(long_calc,x=range(1,100)))

print(smpl.__version__)
