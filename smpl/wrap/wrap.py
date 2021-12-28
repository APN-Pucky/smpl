from tokenize import TokenError
import warnings
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
import sympy
from sympy.printing.pycode import pycode
import uncertainties.unumpy as unp
import inspect
import numpy as np


def get_varnames(expr, xvar):
    """
    Returns a list of variables used in the ``str`` math-expression via sympy and puts ``xvar`` to the front.

    Examples
    --------
    >>> get_varnames("a**x*b+c","x")
    ['x', 'a', 'b', 'c']

    """
    if isinstance(expr, str):
        return str_get_varnames(expr, xvar)
    else:
        return fnc_get_varnames(expr, xvar)


def get_latex(function):
    """
    Return a latex string for passed function.


    Parameters
    ----------
    function : function_like
        function as str lambda or (oneline) function

    Examples
    --------
    >>> get_latex(lambda a,b,c,x : (a+b+c)*x,)
    '$x \\\\left(a + b + c\\\\right)$'
    >>> get_latex("(a+b+c)*x")
    '$x \\\\left(a + b + c\\\\right)$'
    >>> def fun(a,b,x,c):
    ...     return (a+b+c)*x
    >>> get_latex(fun)
    '$x \\\\left(a + b + c\\\\right)$'

    """
    if isinstance(function, str):
        l = "$" + sympy.latex(str_get_expr(function)) + "$"
    else:
        l = function.__name__
    if l == "<lambda>":
        try:
            try:
                cc, li = inspect.findsource(function)
                f = ''.join(cc[li:]).split('lambda')[1].split(':')[1].split(',')[
                    0].replace("\n", "")
                l = "$" + sympy.latex(str_get_expr(f)) + "$"
            except TokenError:
                raise Exception(
                    "Make sure there is a ',' behind the lambda expression and no commas are in the lambda expression and no newlines")
        except OSError:
            l = "$\\lambda$(" + ','.join(function.__code__.co_varnames) + ")"
    elif not isinstance(function, str):
        if function.__doc__ is not None:
            l = function.__doc__.split('\n')[0]
        else:
            try:
                cc, li = inspect.findsource(function)
                s = ''.join(cc[li:]).split('return')[1].split('\n')[0]
                l = "$" + sympy.latex(str_get_expr(s)) + "$"
            except OSError:
                l = function.__name__

    return l


def get_lambda_argd(expr, xvar, *args):
    function = get_lambda(expr, xvar)
    return lambda x: function(x, *args)


def get_lambda(expr, xvar):
    """
    Returns a lambda of given ``str``/``function``/``lambda`` expression with ``__doc__`` set to the latex expression. ``xvar`` is moved to the front.

    Examples
    --------
    >>> l = get_lambda(lambda a,b,c,x : (a+b+c)*x,'x')
    >>> l(4,1,1,1)
    12
    >>> l = get_lambda("(a+b+c)*x",'x')
    >>> l(4,1,1,1)
    12
    >>> def fun(a,b,x,c):
    ...     return (a+b+c)*x
    >>> l = get_lambda(fun,'x')
    >>> l(4,1,1,1)
    12

    """
    if isinstance(expr, str):
        return str_get_lambda(expr, xvar)
    else:
        return fnc_get_lambda(expr, xvar)


def fnc_get_lambda(expr, xvar):
    __l__ = eval("lambda " + ','.join(get_varnames(expr, xvar)) +
                             ": expr(" + ','.join(expr.__code__.co_varnames) + ")", {"expr": expr})
    __l__.__doc__ = expr.__doc__
    return __l__


def str_get_lambda(expr, xvar):
    parsed_expr = str_get_expr(expr)
    pc = pycode(parsed_expr)
    for s in unp.__all__:
        pc = pc.replace("math." + s, "unp."+s)
    # old direct way. Doesn't use unp.
    #__l__ = sympy.lambdify(get_varnames(expr),parsed_expr)
    __l__ = eval(
        "lambda " + ','.join(get_varnames(expr, xvar)) + ": " + pc)
    #exec("global __l__; __l__ = lambda " + ','.join(get_varnames(expr)) + ": "+ pc)
    return __l__


def str_get_varnames(expr, xvar):

    parsed_expr = str_get_expr(expr)

    new_locals = [sym.name
                  for sym in parsed_expr.atoms(sympy.Symbol)]
    new_locals = sorted(new_locals)
    if xvar is None:
        return np.roll(new_locals, 1)
    else:
        varss = new_locals
        assert(xvar in varss)
        varss.remove(xvar)
        return [xvar, *varss]


def fnc_get_varnames(func, xvar):
    if xvar is None:
        return func.__code__.co_varnames
    else:
        varss = [s for s in func.__code__.co_varnames]
        assert(xvar in varss)
        varss.remove(xvar)
        return [xvar, *varss]


def str_get_expr(expr):
    """
    Convert a pythonic string expression ot a sympy expression.

    Only works with np or unp naming.
    """
    expr = expr.replace("math.abs(", "Abs(").replace(
        "np.abs(", "Abs(").replace("unp.abs(", "Abs(")
    expr = expr.replace("math.", "").replace("unp.", "").replace("np.", "")
    try:
        parsed_expr = sympy.parsing.sympy_parser.parse_expr(
            expr,
            local_dict=None,
            transformations=(standard_transformations +
                             (implicit_multiplication_application,)),
            evaluate=False
        )
    except Exception as e:
        warnings.warn(
            "Illegal variable/function name (try uncap. letters) " + expr)
        raise e
    return parsed_expr
