"""
Simplified Fitting.

Uses scipy.curve_fit (no x errors) or scipy.odr (with x errors).
"""
from .fit import Fitter, fit, auto, fit_kwargs, data_split, fit_split, Chi2, R2
__all__ = ['Fitter', 'fit', 'auto', 'fit_kwargs',
           'data_split', 'fit_split', 'Chi2', 'R2']
