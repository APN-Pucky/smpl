class ReadBuffer(object):
    """
    Buffer for reading from a file if ``open`` is ``True``.
    """
    def __init__(self, input,open=False,**kwargs):
        self.input = input
        self.open = open
        self.file = None
     
    def __enter__(self):
        if open and isinstance(self.input, str):
            self.file = open(self.input, 'r')
            return self.file
        else:
            return self.input
 
    def __exit__(self, *args):
        if open and isinstance(self.input, str):
            self.file.close()