import uncertainties as unc
# everything in iminuit is done through the Minuit object, so we import it
from iminuit import Minuit

# we also need a cost function to fit and import the LeastSquares function
from iminuit.cost import LeastSquares
from iminuit.util import Matrix


def _fit_minuit_leastsquares(datax, datay, function, yerr, params=[], **kwargs):
    # TODO check/add params
    least_squares = LeastSquares(datax, datay, yerr, function)
    m = Minuit(least_squares, *params)
    m.migrad()
    m.hesse()
    # print(m.values)
    # print(m.covariance)
    # print("chi2 = ", m.fval)
    # print("ndof = ", len(datax) - m.nfit)

    # fix slice issue from iminuites rewritten __getitem__ by using super
    return unc.correlated_values(m.values, super(Matrix, m.covariance))
