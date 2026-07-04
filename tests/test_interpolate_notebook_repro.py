import importlib
import sys
import warnings
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path = [p for p in sys.path if Path(p or ".").resolve() != REPO_ROOT]

for module_name in list(sys.modules):
    if module_name == "smpl" or module_name.startswith("smpl."):
        del sys.modules[module_name]

interp = importlib.import_module("smpl.interpolate")


def test_bivariatespline_notebook_repro():
    smpl_package = importlib.import_module("smpl")
    assert not Path(smpl_package.__file__).resolve().is_relative_to(REPO_ROOT)

    xvalues = np.linspace(-10, 10, 10)
    yvalues = xvalues * 2
    xx = xvalues
    yy = yvalues
    xx = np.append(xx, xx)
    yy = np.append(yy, -yy)
    zz = xx**2 + yy**2

    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        interp.interpolate(xx, yy, zz, interpolator="bivariatespline")
