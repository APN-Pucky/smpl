"""
Simplified Fitting

Uses scipy.curve_fit (no x errors) or scipy.odr (with x errors).
"""
from .fit import fit,auto,fit_kwargs,data_split
__all__ = ['fit','auto','fit_kwargs', 'data_split']