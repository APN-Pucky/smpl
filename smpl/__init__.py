"""A collection of simplified utilities."""

import pkg_resources as pkg  # part of setuptools

package = "smpl"

try:
    version = pkg.require(package)[0].version
except pkg.DistributionNotFound:
    version = "dirty"

__version__ = version