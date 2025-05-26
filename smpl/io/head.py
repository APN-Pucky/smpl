from io import StringIO

from smpl import doc

from .read_buffer import ReadBuffer


def head(*inps, open=True, n=1):
    """
    Returns the first ``n`` lines of ``fname``.

    Parameters
    ----------
    inps : str, array_like, buffer
        object to read from
    n : int, optional
        number of lines to return, by default 1

    Returns
    -------
    StringIO
        A file-like object containing the first ``n`` lines of ``fname``.

    Examples
    --------
    >>> from smpl import io
    >>> import pandas as pd
    >>> io.write("test.txt","hi\\n1\\n2\\n3\\n4\\n")
    >>> pd.read_csv(head("test.txt",n=2))
       hi
    0   1
    >>> pd.read_csv(head("test.txt",n=3))
       hi
    0   1
    1   2

    """
    r = StringIO()
    for inp in inps:
        with ReadBuffer(inp, open=open) as inp:
            r.write("\n".join(inp.readlines()[:n]))
    r.seek(0, 0)
    return r


headf = doc.deprecated(
    version="1.0.6.1",
    removed_in="2.0.0",
    reason="Use :func:`smpl.io.head(..., open=True)` instead.",
)(head)
