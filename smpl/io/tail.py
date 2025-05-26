from io import StringIO

from smpl import doc

from .read_buffer import ReadBuffer


def tail(*inps, open=True, n=1):
    """
    Returns the last ``n`` lines of ``fname``.

    Parameters
    ----------
    inps : buffer, str, array_like
        object to read from
    n : int, optional
        number of lines to return, by default 1

    Returns
    -------
    StringIO
        A `StringIO` object containing the last ``n`` lines of ``fname``.

    Examples
    --------

    >>> from smpl import io
    >>> import pandas as pd
    >>> io.write("test.txt","hi\\n1\\n2\\n3\\n4\\n")
    >>> pd.read_csv(tail("test.txt",n=2))
       3
    0  4
    >>> pd.read_csv(tail("test.txt",n=3))
       2
    0  3
    1  4

    """
    ret = StringIO()
    for inp in inps:
        with ReadBuffer(inp, open=open) as inp:
            ret.write("\n".join(inp.readlines()[-n:]))
    ret.seek(0, 0)
    return ret


tailf = doc.deprecated(
    version="1.0.6.1",
    removed_in="2.0.0",
    reason="Use :func:`smpl.io.tail(..., open=True)` instead.",
)(tail)
