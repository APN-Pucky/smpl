class ReadBuffer:
    """
    Buffer for reading from a file if ``open`` is ``True``.
    """

    def __init__(self, input, open=False, **kwargs):
        self.input = input
        self.open = open
        self.file = None

    def __enter__(self):
        if self.open and isinstance(self.input, str):
            self.file = open(self.input)
            return self.file
        return self.input

    def __exit__(self, *args):
        if self.open and isinstance(self.input, str):
            self.file.close()
