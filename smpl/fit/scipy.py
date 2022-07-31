import warnings
import numpy as np
from scipy import optimize
from scipy.odr.odrpack import ODR, Model, RealData
import uncertainties as unc

from smpl import debug
from smpl.util import util
# fittet ein dataset mit gegebenen x und y werten, eine funktion und ggf. anfangswerten und y-Fehler
# gibt die passenden parameter der funktion, sowie dessen unsicherheiten zurueck
#
# https://stackoverflow.com/questionsquestions/14581358/getting-standard-errors-on-fitted-parameters-using-the-optimize-leastsq-method-i#
# Updated on 4/6/2016
# User: https://stackoverflow.com/users/1476240/pedro-m-duarte


def _fit_curvefit(datax, datay, function, params=None, yerr=None, **kwargs):
    try:
        pfit, pcov = \
            optimize.curve_fit(function, datax, datay, p0=params,
                               sigma=yerr, epsfcn=util.get("epsfcn", kwargs, 0.0001), **kwargs, maxfev=util.get("maxfev", kwargs, 10000))
    except RuntimeError as e:
        debug.msg(str(e))
        return params
    error = []
    for i in range(len(pfit)):
        try:
            error.append(np.absolute(pcov[i][i])**0.5)
        except Exception as e:
            warnings.warn(str(e))
            error.append(0.00)
    # print(pcov)
    # restore cov: unc.covariance_matrix([*ff])
    return unc.correlated_values(pfit, pcov)

# https://stackoverflow.com/a/52592811


def _fit_odr(datax, datay, function, params=None, yerr=None, xerr=None):
    model = Model(lambda p, x: function(x, *p))
    realdata = RealData(datax, datay, sy=yerr, sx=xerr)
    odr = ODR(realdata, model, beta0=params)
    out = odr.run()
    # This was the old wrong way! Now use correct co. matrix through unc-package!
    # Note Issues on scipy odr and curve_fit, regarding different definitions/namings of standard deviation or error and covaraince matrix
    # https://github.com/scipy/scipy/issues/6842
    # https://github.com/scipy/scipy/pull/12207
    # https://stackoverflow.com/questions/62460399/comparison-of-curve-fit-and-scipy-odr-absolute-sigma
    return unc.correlated_values(out.beta, out.cov_beta)
