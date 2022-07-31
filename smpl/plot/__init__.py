"""Simplified plotting."""

from .plot import data, fit, function, unv, usd, auto, plot_kwargs
from .plot2d import plot2d, plot2d_kwargs
__all__ = ['data', 'fit', 'function', 'unv', 'usd',
           'auto', 'plot_kwargs', 'plot2d', 'plot2d_kwargs']
from matplotlib.pyplot import *