from typing import List
import numpy as np


def si(s, u:str="", fmt:str="{}"):
    """
    Get number with uncertainty and unit in ``si`` format for latex.

    Parameters
    ----------
    s : ufloat
        number to be returned in a latex compatible format.
    u : str
        unit of that number.
    fmt : str
        format string for the numbers.

    Returns
    -------
    str
        latex SI string of the number with it's uncertainty and unit.

    Examples
    --------
    >>> import uncertainties as unc
    >>> from smpl import io
    >>> si(unc.ufloat(2000,0.1))
    '\\\\SI{2000.00+-0.10}{}'
    >>> si(unc.ufloat(2000,0.1),"\\meter")
    '\\\\SI{2000.00+-0.10}{\\\\meter}'
    >>> si(unc.ufloat(2000,0.1),"\\meter", io.gf(2))
    '\\\\SI{2.0+-0.0e+03}{\\\\meter}'

    """
    return "\\SI{%s}{%s}" % ((fmt.format(s)).replace("/", "").replace("(", "").replace(")", ""), u)


def si_line(a, skip:int=0, fmt:str="{}"):
    """
    Get array ``a`` in the format of a line of a latex table.

    Examples
    --------
    >>> si_line([1,2,3,])
    '\\\\SI{1}{}&\\\\SI{2}{}&\\\\SI{3}{}\\\\\\\\\\n'

    """
    return si_tab(np.transpose([[t] for t in a]), skip, fmt)


def si_ttab(tab, skip:int=0, fmt:str="{}"):
    """
    Transposed :func:`si_tab`.

    Parameters
    ----------
    tab : array_like
        Array containing the values of the table
    skip : number
        Skip this many table lines
    fmt : str
        format string for the numbers

    Returns
    -------
    tabstr : str
        table latex string

    Examples
    --------
    >>> si_ttab([[1,2],[3,4]])
    '\\\\SI{1}{}&\\\\SI{3}{}\\\\\\\\\\n\\\\SI{2}{}&\\\\SI{4}{}\\\\\\\\\\n'

    """
    return si_tab(np.transpose(tab), skip, fmt)


def si_tab(tab, skip=0, fmt="{}"):
    """
    Get arrays of (uncertainty) numbers in  a latex table compatible form.

    Parameters
    ----------
    tab : array_like
        Array containing the values of the table
    skip : number
        Skip this many table lines
    fmt : str
        format string for the numbers

    Returns
    -------
    str
        

    Examples
    --------
    >>> si_tab([[1,2],[3,4]])
    '\\\\SI{1}{}&\\\\SI{2}{}\\\\\\\\\\n\\\\SI{3}{}&\\\\SI{4}{}\\\\\\\\\\n'

    """
    # mkdirs(fn)
    #file = open(fn,"w")
    s = ""
    for _, ti in enumerate(tab):
        for j, tij in enumerate(ti):
            if(j != 0):
                s += "&"
            if(j >= skip):
                s += si(tij, fmt=fmt)
            else:
                s += "%s" % (tij)
        s += "\\\\\n"
    return s