
from io import StringIO

from smpl_io.read_buffer import ReadBuffer


def cat(*inps):
    """
    Read all ``inps`` and return them as a single string.

    Parameters
    ----------
    inps : str, array_like, buffer
        object to read from
    
    Returns
    -------
    str
        all ``inps`` as a single string.

    Examples
    --------
    >>> from smpl_io import io
    >>> io.write("test.txt","hi\\nho1\\n2\\n3\\n4\\n")
    >>> io.cat("test.txt")
    'hi\\nho1\\n2\\n3\\n4\\n'
    """
    r = StringIO()
    for inp in inps:
        with ReadBuffer(inp) as f:
            r.write(f.read())
    r.seek(0, 0)
    return r
