import numpy as np
import uncertainties.unumpy as unp

from smpl import doc


# allgemeine Fitfunktionen
@doc.append_plot(4)
@doc.insert_str("const(x) = $m$")
def const(x, m):
    return x-x + m


@doc.append_plot(2)
@doc.insert_latex_eq()
def linear(x, m):  # lineare Funktion mit f(x) = m * x
    return(m*x)


@doc.append_plot(2, -1)
@doc.insert_latex_eq()
def line(x, a, b):  # gerade mit = f(x) = m * x + b
    return (a*x + b)
# Gerade=line
# Line=line


@doc.append_plot(3, 0.02, 3)
@doc.insert_latex_eq()
def cos_abs(x, a, f, phi):
    return a * np.abs(unp.cos(2*np.pi*f*(x-phi)))


@doc.append_plot(3, 0.02, 3)
@doc.insert_latex_eq()
def cos(x, a, f, phi):
    return a * unp.cos(2*np.pi*f*(x-phi))


@doc.append_plot(3, 0.02, 3)
@doc.insert_latex_eq()
def sin(x, a, f, phi):
    return a * unp.sin(2*np.pi*f*(x-phi))


@doc.append_plot(3, 0.02, 3)
@doc.insert_latex_eq()
def tan(x, a, f, phi):
    return a * unp.tan(2*np.pi*f*(x-phi))


@doc.append_plot(0, 5, 3, 0)
@doc.insert_latex_eq()
def lorentz(x, x_0, a, d, y):
    return a/(np.pi*d*(1+(x-x_0)**2/d**2)) + y
# Lorentz=lorentz


@doc.append_plot(0, 5, 3, 0)
@doc.insert_latex_eq()
def gauss(x, x_0, a, d, y):
    return a * unp.exp(-(x - x_0)**2 / 2 / d**2) + y


Gauss = gauss


@doc.append_plot(0.5, 4)
@doc.insert_latex_eq()
def exponential(x, c, y_0):
    return unp.exp(c * x) * y_0


exp = exponential


@doc.append_plot(0.5, 4, xmin=0.1)
@doc.insert_latex_eq()
def log(x, c, y_0):
    return unp.log(c * x) * y_0


@doc.append_plot(1, 5, 0)
@doc.insert_latex_eq()
def square(x, x_0, a, y):
    return a*(x-x_0)**2+y


@doc.append_plot(1, 5, 0, -2)
@doc.insert_latex_eq()
def cube(x, a, b, c, d):
    return a*x**3+b*x**2+c*x+d


@doc.append_plot(1, 3.3, 0)
@doc.insert_latex_eq()
def order(x, a, k, y):
    return a*(x)**k+y


@doc.append_plot(1, 3.3, 0, xmin=0)
@doc.insert_latex_eq()
def sqrt(x, a, b, c):
    return a*unp.sqrt(x+b)+c
