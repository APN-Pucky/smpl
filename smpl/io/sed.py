import re
from io import StringIO

from .read_buffer import ReadBuffer


def sed(pattern, replace, *inps, open=True):
    """
    Replace ``pattern`` in ``inp``.

    >>> from smpl import io
    >>> io.write("test.txt","hi\\n")
    >>> sed("hi","cool","test.txt").read()
    'cool\\n'
    """
    r = StringIO()
    for inp in inps:
        with ReadBuffer(inp, open=open) as f:
            lines = f.readlines()
            for _, line in enumerate(lines):
                r.write(re.sub(pattern, replace, line))
    r.seek(0, 0)
    return r
