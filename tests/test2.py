import numpy as np
import matplotlib.pyplot as plt
from smpl import plot
from smpl import functions as f

from smpl import test
from smpl import io
from smpl.parallel import *
import smpl


def gompertz(N,a,b):
    return -a * N * np.log(b*N)
def solution_gompertz(t,a,b,c):
    return 1/b*np.exp(np.exp(-t*a)*c)
for a in [1,2]:
    for b in [1,2]:
        plot.function( gompertz, a,b, xaxis="$N$", yaxis="$\\dot N$",xmin=0, xmax=5 ,init=False )
plt.show()

for a in [1,2]:
    for b in [1,2]:
        for c in [1,2]:
            plot.function( solution_gompertz, a,b,c, xaxis="$N$", yaxis="$\\dot N$",xmin=0, xmax=5,init=False )
plt.show()