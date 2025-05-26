import re
from io import StringIO

from smpl import doc

from .read_buffer import ReadBuffer


def grep(pattern, *inps, regex=False, open=True, A=0, B=0):
    """
    Searches for ``pattern`` in ``inp``.

    >>> from smpl import io
    >>> io.write("test.txt","hi\\nho1\\n2\\n3\\n4\\n")
    >>> grep("h","test.txt").read()
    'hi\\nho1\\n'
    >>> grep("h.*\\\\d","test.txt",regex=True).read()
    'ho1\\n'
    """
    r = StringIO()
    for inp in inps:
        with ReadBuffer(inp, open=open) as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                match = False
                for j in range(
                    (i - A if float("inf") != A else 0),
                    (i + B + 1 if float("inf") != B else len(lines)),
                ):
                    if j < 0 or j >= len(lines):
                        continue
                    if pattern in lines[j] or (regex and re.search(pattern, lines[j])):
                        match = True
                if match:
                    r.write(line)
    r.seek(0, 0)
    return r


grepf = doc.deprecated(
    version="1.0.6.1",
    removed_in="2.0.0",
    reason="Use :func:`smpl.io.grep(..., open=True)` instead.",
)(grep)


def between(pattern1, pattern2, *inps, regex=False, open=True):
    """
    Searches for ``pattern1`` and ``pattern2`` in ``inp`` and returns the lines between them.

    >>> from smpl import io
    >>> io.write("test.txt","hi\\nho1\\n2\\n3\\n4\\n")
    >>> between("hi","2","test.txt").read()
    'ho1\\n'
    """
    r = StringIO()
    for inp in inps:
        with ReadBuffer(inp, open=open) as f:
            lines = f.readlines()
            start = -1
            for i, line in enumerate(lines):
                if pattern1 in line or (regex and re.search(pattern1, line)):
                    start = i
                if pattern2 in line or (regex and re.search(pattern2, line)):
                    end = i
                    # only write after a closed block if a new block is found before
                    if start > -1:
                        r.write("".join(lines[start + 1 : end]))
                    start = -1
    r.seek(0, 0)
    return r
