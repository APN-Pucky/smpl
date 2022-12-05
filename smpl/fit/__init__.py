"""
Simplified Fitting.

Uses scipy.curve_fit (no x errors) or scipy.odr (with x errors).
"""
from .fit import R2, Chi2, Fitter, auto, data_split, fit, fit_kwargs, fit_split

__all__ = [
    "Fitter",
    "fit",
    "auto",
    "fit_kwargs",
    "data_split",
    "fit_split",
    "Chi2",
    "R2",
]
