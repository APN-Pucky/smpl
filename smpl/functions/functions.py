import numpy as np
import scipy
import uncertainties.unumpy as unp

from smpl import doc


# allgemeine Fitfunktionen
@doc.insert_eq()
@doc.append_plot(4)
def const(x,m):
    '''m'''
    return (np.ones(np.shape(x))*m)

@doc.insert_eq()
@doc.append_plot(2)
def linear(x,m): # lineare Funktion mit f(x) = m * x
    '''mx'''
    return(m*x)

@doc.insert_eq()
@doc.append_plot(2,-1)
def line(x, a, b): # gerade mit = f(x) = m * x + b
    '''ax+b'''
    return (a*x + b)
#Gerade=line
#Line=line

@doc.insert_eq()
@doc.append_plot(3,0.02,3)
def cos_abs(x, a, f, phi):
    '''$a|\\cos(2πf(x-\\phi))|$'''
    return a * np.abs(unp.cos(2*np.pi*f*(x-phi)))

@doc.insert_eq()
@doc.append_plot(3,0.02,3)
def cos(x, a, f, phi):
    '''$a\\cos(2πf(x-\\phi))$'''
    return a * unp.cos(2*np.pi*f*(x-phi))
@doc.insert_eq()
@doc.append_plot(3,0.02,3)
def sin(x, a, f, phi):
    '''$a\\sin(2πf(x-\\phi))$'''
    return a * unp.sin(2*np.pi*f*(x-phi))
@doc.insert_eq()
@doc.append_plot(3,0.02,3)
def tan(x, a, f, phi):
    '''$\\tan(2πf(x-\\phi))a$'''
    return a * unp.tan(2*np.pi*f*(x-phi))

@doc.insert_eq()
@doc.append_plot(0,5,3,0)
def lorentz(x,x_0,A,d,y):
    '''$\\frac{A}{\\pi d (1+ (\\frac{x-x_0}{d})^2)} + y$'''
    return 1/(np.pi*d*(1+(x-x_0)**2/d**2))*A + y
#Lorentz=lorentz


@doc.insert_eq()
@doc.append_plot(0,5,3,0)
def gauss(x, x_0, A, d, y):
    '''$A\\cdot \\exp\\left(\\frac{-(x-x_0)^2}{2d^2}\\right)+y$'''
    return A * unp.exp(-(x - x_0)**2 / 2 / d**2) + y
Gauss=gauss


@doc.insert_eq()
@doc.append_plot(0.5,4)
def exponential(x, c, y_0):
    '''$\\exp(cx)y_0$'''
    return unp.exp(c * x) * y_0
exp=exponential

@doc.insert_eq()
@doc.append_plot(0.5,4,xmin=0.1)
def log(x, c, y_0):
    '''$\\log(cx)y_0$'''
    return unp.log(c * x) * y_0

@doc.insert_eq()
@doc.append_plot(1,5,0)
def square(x,x_0,A,y):
    '''$A(x-x_0)^2+y$'''
    return A*(x-x_0)**2+y
def quadratic_(x,A,y):
    '''A*(x)**2+y'''
    return A*(x)**2+y
quadratic=square
Quadratisch=quadratic_

@doc.insert_eq()
@doc.append_plot(1,5,0,-2)
def cube(x,a,b,c,d):
    '''$ax^3+bx^2+cx+d$'''
    return a*x**3+b*x**2+c*x+d


@doc.insert_eq()
@doc.append_plot(1,3.3,0)
def order(x,A,k,y):
    '''A*(x)**k+y'''
    return A*(x)**k+y


@doc.insert_eq()
@doc.append_plot(1,3.3,0,xmin=0)
def sqrt(x,a,b,c):
    '''$a\\sqrt{x+b}+c$'''
    return a*unp.sqrt(x+b)+c


def Gauß(x, x0, A, d):
    '''$A\\cdot \\exp\\left(\\frac{-(x-x0)^2}{2d^2}\\right)$'''
    return A * unp.exp(-(x - x0)**2 / 2 / d**2)
def Two_Gauss(x, x0, A0, d0, x1, A1, d1,y):
    '''$A\\cdot \\exp\\left(\\frac{-(x-x0)^2}{2d^2}\\right)+y$'''
    #return A0 * np.exp(-(x - x0)**2 / 2 / d0**2) + y0 + A1 * np.exp(-(x - x1)**2 / 2 / d1**2) + y1
    return gauss(x,x0,A0,d0,y)+gauss(x,x1,A1,d1,0)
def Six_Gauss(x, x0, A0, d0, x1, A1, d1,x2, A2, d2,x3, A3, d3,x4, A4, d4, x5, A5, d5,y):
    '''$A\\cdot \\exp\\left(\\frac{-(x-x0)^2}{2d^2}\\right)+y$'''
    #return A0 * np.exp(-(x - x0)**2 / 2 / d0**2) + y0 + A1 * np.exp(-(x - x1)**2 / 2 / d1**2) + y1
    return gauss(x,x0,A0,d0,y)+gauss(x,x1,A1,d1,0)+gauss(x,x2,A2,d2,0)+gauss(x,x3,A3,d3,0)+gauss(x,x4,A4,d4,0)+gauss(x,x5,A5,d5,0)
def Two_Exp(x,A0,A1,l0,l1):
    '''A0*exp(-l0*x)+A1*exp(-l1*x)'''
    return exponential(x,-l0,A0)+exponential(x,-l1,A1)

def Two_Lorentz(x, x0, A0, d0, x1, A1, d1,y):
    '''$\\frac{A}{\\pi d (1+ (\\frac{x-x0}{d})^2)} + y$'''
    return lorentz(x,x0,A0,d0,y)+lorentz(x,x1,A1,d1,0)

def Split_Gauss(x,x0,A0,d0,d1,y):
    '''\n$A\\cdot \\exp\\left(\\frac{-(x-x0)^2}{2d0^2}\\right)+y$, für x>x0\n$A\\cdot \\exp\\left(\\frac{-(x-x0)^2}{2d1^2}\\right)+y$, sonst'''
    return np.where(x>x0,gauss(x,x0,A0,d0,y) ,gauss(x,x0,A0,d1,y))