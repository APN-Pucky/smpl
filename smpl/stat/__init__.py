"""Simplified statistics."""

from .stat import unv, usd, unv_lambda, poisson_dist, normalize, novar_mean, mean, noisy, no_dist,R2,Chi2,fft, get_interesting_domain,average_deviation

__all__ = ['unv',
           'usd',
           'unv_lambda', 'poisson_dist',
           'no_dist',
           'normalize', 'novar_mean',
           'mean', 'noisy',
           'R2','Chi2','fft',
           'get_interesting_domain',
           'average_deviation'
          ]
