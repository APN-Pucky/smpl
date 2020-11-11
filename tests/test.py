import numpy as np
import matplotlib.pyplot as plt
from simple import plot
from simple import functions as f

from simple import test



data = np.loadtxt('tests/test_linear.txt')
ff = plot.fit(data[:,0], data[:,1], fmt='.', function=f.Gerade, p0=[1,2], sigmas=1,lpos=2)
plt.show()
