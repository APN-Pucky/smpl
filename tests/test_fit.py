import pytest
import numpy as np
import matplotlib.pyplot as plt
from smpl import plot
from smpl import functions as f

from smpl.parallel import res, par, calc
import smpl
from smpl.plot.plot import init_plot

@pytest.mark.line_profile.with_args(plot.fit,plot.function,init_plot)
def test_fit():
    plot.function(lambda n, a, b: -a * n * np.log(b*n), 1, 1,
                  xaxis="$N$", yaxis="$\\dot N$", xmin=0, xmax=100)
    plot.show(block=False)
    plot.close()
    # print(io.pwd())


    data = np.loadtxt('tests/test_linear.txt')
    ff = plot.fit(data[:, 0], data[:, 1], fmt='.', function=f.linear, units=[
                  "l", "b"], sigmas=1, lpos=2, residue=True, residue_err=False, xaxis="t", yaxis="s")
    ff = plot.fit(data[:, 0], data[:, 1], fmt='.', function=f.line, units=[
                  "l", "b"], sigmas=1, lpos=2, residue=True, residue_err=False, xaxis="t", yaxis="s", b=0)

    plt.show(block=False)
    plot.close()