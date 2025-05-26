from io import StringIO

from smpl.io.read_buffer import ReadBuffer


def cat(*inps, open=True):
    """
    Read all ``inps`` and return them as a single string.

    Parameters
    ----------
    inps : str, array_like, buffer
        object to read from

    Returns
    -------
    StringIO
        all ``inps`` as a StringIO buffer.

    Examples
    --------
    >>> from smpl import io
    >>> io.write("test.txt","hi\\nho1\\n2\\n3\\n4\\n")
    >>> io.cat("test.txt").getvalue()
    'hi\\nho1\\n2\\n3\\n4\\n'
    """
    r = StringIO()
    for inp in inps:
        with ReadBuffer(inp, open=open) as f:
            r.write(f.read())
    r.seek(0, 0)
    return r
