"""Simplified statistics."""

from .stat import (
    R2,
    Chi2,
    average_deviation,
    fft,
    get_interesting_domain,
    mean,
    no_dist,
    noisy,
    normalize,
    novar_mean,
    poisson_dist,
    unv,
    unv_lambda,
    usd,
)

__all__ = [
    "unv",
    "usd",
    "unv_lambda",
    "poisson_dist",
    "no_dist",
    "normalize",
    "novar_mean",
    "mean",
    "noisy",
    "R2",
    "Chi2",
    "fft",
    "get_interesting_domain",
    "average_deviation",
]
