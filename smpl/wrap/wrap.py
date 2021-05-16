from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application
from sympy.parsing.sympy_parser import parse_expr
import sympy
from sympy.printing.pycode import pycode
import uncertainties.unumpy as unp

import numpy as np

def get_lambda(expr,xvar):
    if isinstance(expr,str):
        return str_get_lambda(expr,xvar)
    else:
        return fnc_get_lambda(expr,xvar)

def fnc_get_lambda(expr,xvar):
    __l__ = eval("lambda " + ','.join(get_varnames(expr,xvar)) + ": expr(" + ','.join(expr.__code__.co_varnames) + ")",{"expr":expr})
    __l__.__doc__ = expr.__doc__
    return __l__

def str_get_lambda(expr,xvar):
    parsed_expr = str_get_expr(expr)
    pc = pycode(parsed_expr)
    for s in unp.__all__:
        pc = pc.replace("math." + s, "unp."+s)
    # old direct way. Doesn't use unp.
    #__l__ = sympy.lambdify(get_varnames(expr),parsed_expr)
    __l__ = eval("lambda " + ','.join(get_varnames(expr,xvar)) + ": "+ pc)
    #exec("global __l__; __l__ = lambda " + ','.join(get_varnames(expr)) + ": "+ pc)
    return __l__

def get_varnames(expr,xvar):
    if isinstance(expr,str):
        return str_get_varnames(expr,xvar)
    else:
        return fnc_get_varnames(expr,xvar)
#def get_argcount(expr):
#    return len(get_varnames(expr))

def str_get_varnames(expr,xvar):
    """
    Returns a list of variables used in the ``str`` math-expression via sympy.
    """

    parsed_expr = str_get_expr(expr)
    
    new_locals = [sym.name
                  for sym in parsed_expr.atoms(sympy.Symbol)]
    new_locals = sorted(new_locals)
    if xvar is None:
        return np.roll(new_locals,1)
    else:
        vars = new_locals
        assert(xvar in vars)
        vars.remove(xvar)
        return [xvar,*vars]


def fnc_get_varnames(func,xvar):
    if xvar is None:
        return func.__code__.co_varnames
    else:
        vars = [s for s in func.__code__.co_varnames]
        assert(xvar in vars)
        vars.remove(xvar)
        return [xvar,*vars]

def str_get_expr(expr):
    expr = expr.replace("unp.","").replace("np.","")
    parsed_expr = sympy.parsing.sympy_parser.parse_expr(
        expr,
        local_dict=None,
        transformations=(standard_transformations + (implicit_multiplication_application,)),
        evaluate=False
    )
    return parsed_expr