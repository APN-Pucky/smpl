import matplotlib.pyplot as plt
import numpy as np
import pytest
import tqdm

from smpl_animation import animation
from smpl import plot, stat
from smpl.functions import fac
from smpl.plot import init_plot

# from smpl.animation.animation import FigAnimation

# @pytest.mark.line_profile.with_args(plot.function,plot.fit,init_plot,FigAnimation.__init__)
@pytest.mark.line_profile.with_args(plot.function, plot.fit, init_plot)
def test_animation():
    plt.ioff()

    def update(a):
        plot.function(lambda x: a * x**2, xmin=0, xmax=5, init=True, tight=False)

    ani = animation.animate(
        update=update, frames=np.linspace(0, 10, 200), interval=10, blit=True
    )
    plt.show(block=False)
    plt.pause(10)
    plt.close("all")
    plt.ioff()
    for a in tqdm.tqdm(np.linspace(0, 10, 200)):
        plot.function(lambda x: a * x**2, xmin=0, xmax=5, init=True, tight=False)
        animation.frame()

    ani = animation.animate(interval=10, blit=True)
    plt.show(block=False)
    plt.pause(10)
    plt.close("all")
    ani.save("test.gif")


c = 0
datax = 0
datay = 0
bahnh = 0
bahnhs = 0

# @pytest.mark.line_profile.with_args(plot.function,plot.fit,init_plot,FigAnimation.__init__)
@pytest.mark.line_profile.with_args(plot.function, plot.fit, init_plot)
def test_histogram():
    global c, datax, datay, bahnh, bahnhs
    n = 13
    bahnhs = 13
    bahnh = np.array(range(bahnhs)) * 0
    datax = np.array(range(1, 14))
    datay = datax * 0
    c = 0

    def update(a):
        global c, bahnh
        c += 1
        bahnh = bahnh * 0
        for i in range(n):
            bahnh[np.random.randint(0, bahnhs)] += 1
            if np.any(np.greater(bahnh, 1)):
                datay[i] += 1
        plot.data(
            datax,
            stat.poisson_dist(datay) / c,
            init=True,
            tight=False,
            fmt="hist",
            ylabel="P(>1 Gäste bei beliebigem Bahnhof)",
            xlabel="$n$ Gäste",
            capsize=0,
        )
        plot.function(
            lambda ni: 1.0 - fac(bahnhs) / (fac(bahnhs - ni) * bahnhs**ni),
            xmin=0,
            xmax=13,
            label="$\\frac{b!}{(b-n)!b^n}$",
            function_color="orange",
        )

    animation.animate(
        update=update, frames=np.linspace(0, 20, 2000), interval=10, blit=False
    )
    plt.show(block=False)
    plt.pause(10)
    plt.close("all")


# @pytest.mark.line_profile.with_args(plot.function,plot.fit,init_plot,FigAnimation.__init__)
@pytest.mark.line_profile.with_args(plot.function, plot.fit, init_plot)
def test_subplots():
    plt.ioff()
    for a in tqdm.tqdm(np.linspace(0, 10, 200)):
        fig, axs = plot.subplots(1, 3, figsize=(12, 8), sharey=True)
        fig.subplots_adjust(wspace=0)
        plot.function(lambda x: a * x**2, axes=axs[0], tight=False, xmin=0, xmax=1)
        plot.function(lambda x: a * x**5, axes=axs[0], tight=False, xmin=0, xmax=1)
        plot.function(
            lambda x: a * x**3, axes=axs[1], logx=True, tight=False, xmin=0, xmax=1
        )
        plot.function(lambda x: a * x**1, axes=axs[2], tight=False, xmin=0, xmax=1)
        animation.frame()
    animation.animate(interval=10, blit=True)
    plt.show(block=False)
    plt.pause(10)
    plt.close("all")
    animation.clear()
    for a in tqdm.tqdm(np.linspace(0, 10, 100)):
        fig, axs = plot.subplots(1, 3, figsize=(12, 8), sharey=True)
        fig.subplots_adjust(wspace=0)
        plot.function(lambda x: a * x**3, axes=axs[1], logx=True, xmin=0, xmax=1)
        plot.function(lambda x: a * x**2, axes=axs[0], xmin=0, xmax=1)
        plot.function(lambda x: a * x**5, axes=axs[0], xmin=0, xmax=1)
        plot.function(lambda x: a * x**1, axes=axs[2], xmin=0, xmax=1)
        animation.frame()
    animation.animate(interval=10, blit=True)
    plt.show(block=False)
    plt.pause(10)
    plt.close("all")
