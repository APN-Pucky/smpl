import numpy as np
import uncertainties as unc
import uncertainties.unumpy as unp

# %% Konstanten fuer einheitliche Darstellung
unv=unp.nominal_values
usd=unp.std_devs
def unv_lambda(f):
    return lambda *a : unv(f(*a))

# mathe Funktionen
def poisson_dist(N):
    return unp.uarray(N,np.sqrt(N))
def find_nearest_index(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx
def find_nearest(array, value):
    array[find_nearest_index(array,value)]
def normalize(ydata):
   return (ydata-np.amin(ydata))/(np.amax(ydata)-np.amin(ydata))
def novar_mean(f):
    return np.sum(f)/len(f)
def mean(n):
    # find the mean value and add uncertainties
    k = np.mean(n)
    err = stat.variance(unv(n))
    return unc.ufloat(unv(k), math.sqrt(usd(k)**2 + err))

def fft(y):
    N = len(y)
    fft = scipy.fftpack.fft(y)
    return 2 * abs(fft[:N//2]) / N

    # allgemeine Fitfunktionen
def const(x,m):
    '''m'''
    return (np.ones(np.shape(x))*m)
def linear(x,m): # lineare Funktion mit f(x) = m * x
    '''mx'''
    return(m*x)

def line(x, a, b): # gerade mit = f(x) = m * x + b
    '''a*x+b'''
    return (a*x + b)
Gerade=line
Line=line

def cos_abs(x, a, f, phi):
    '''a*|cos(2*π*f*(x-phi))|'''
    return a * np.abs(unp.cos(2*np.pi*f*(x-phi)))

def cyclicOff(x, a, f, phi, offset):
    return cyclic(x, a, f, phi) + offset
def Lorentz(x,x0,A,d,y):
    '''$\\frac{A}{\\pi d (1+ (\\frac{x-x0}{d})^2)} + y$'''
    return 1/(np.pi*d*(1+(x-x0)**2/d**2))*A + y
def Two_Lorentz(x, x0, A0, d0, x1, A1, d1,y):
    '''$\\frac{A}{\\pi d (1+ (\\frac{x-x0}{d})^2)} + y$'''
    return Lorentz(x,x0,A0,d0,y)+Lorentz(x,x1,A1,d1,0)
def Six_Lorentz(x, x0, A0, d0, x1, A1, d1,y):
    '''$\\frac{A}{\\pi d (1+ (\\frac{x-x0}{d})^2)} + y$'''
    return Lorentz(x,x0,A0,d0,y)+Lorentz(x,x1,A1,d1,0)+Lorentz(x,x2,A2,d2,0)+Lorentz(x,x3,A3,d3,0)+Lorentz(x,x4,A4,d4,0)+Lorentz(x,x5,A5,d5,0)

def Split_Gauss(x,x0,A0,d0,d1,y):
    '''\n$A\\cdot \\exp\\left(\\frac{-(x-x0)^2}{2d0^2}\\right)+y$, für x>x0\n$A\\cdot \\exp\\left(\\frac{-(x-x0)^2}{2d1^2}\\right)+y$, sonst'''
    return np.where(x>x0,gauss(x,x0,A0,d0,y) ,gauss(x,x0,A0,d1,y))
def Gauss(x, x0, A, d, y):
    '''$A\\cdot \\exp\\left(\\frac{-(x-x0)^2}{2d^2}\\right)+y$'''
    return A * unp.exp(-(x - x0)**2 / 2 / d**2) + y
gauss=Gauss
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
def exponential(x, c, y0):
    return np.exp(c * x) * y0
def quadratic(x,x0,A,y):
    '''A*(x-x0)**2+y'''
    return A*(x-x0)**2+y
def quadratic_(x,A,y):
    '''A*(x)**2+y'''
    return A*(x)**2+y
def order(x,A,k,y):
    '''A*(x)**k+y'''
    return A*(x)**k+y
    
Quadratisch=quadratic_


