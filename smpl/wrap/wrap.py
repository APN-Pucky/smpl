from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application
from sympy.parsing.sympy_parser import parse_expr
import sympy
import numpy as np

def get_lambda(expr):
    if isinstance(expr,str):
        return str_get_lambda(expr)
    else:
        return expr

def str_get_lambda(expr):
    parsed_expr = str_get_expr(expr)
    return sympy.lambdify(get_varnames(expr),parsed_expr)

def get_varnames(expr):
    if isinstance(expr,str):
        return str_get_varnames(expr)
    else:
        return fnc_get_varnames(expr)
def get_argcount(expr):
    return len(get_varnames(expr))

def str_get_varnames(expr):
    """
    Returns a list of variables used in the ``str`` math-expression via sympy.
    """
    parsed_expr = str_get_expr(expr)
    
    new_locals = [sym.name
                  for sym in parsed_expr.atoms(sympy.Symbol)]
    new_locals = sorted(new_locals)
    return np.roll(new_locals,1)

def fnc_get_varnames(func):
    return func.__code__.co_varnames

def str_get_expr(expr):
    expr = expr.replace("unp.","").replace("np.","")
    parsed_expr = sympy.parsing.sympy_parser.parse_expr(
        expr,
        local_dict=None,
        transformations=(standard_transformations + (implicit_multiplication_application,)),
        evaluate=False
    )
    return parsed_expr