"""Simplified statistics."""

from .stat import unv, usd, unv_lambda, poisson_dist, normalize, novar_mean, mean, noisy, no_dist

__all__ = ['unv',
           'usd',
           'unv_lambda', 'poisson_dist',
           'no_dist',
           'normalize', 'novar_mean',
           'mean', 'noisy'
           ]
