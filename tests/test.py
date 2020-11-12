import numpy as np
import matplotlib.pyplot as plt
from smpl import plot
from smpl import functions as f

from smpl import test



data = np.loadtxt('tests/test_linear.txt')
ff = plot.fit(data[:,0], data[:,1], fmt='.', function=f.Gerade, sigmas=1,lpos=2)
plt.show()


testl = lambda x,a,b : a*x+b
print(testl.__code__.co_argcount)