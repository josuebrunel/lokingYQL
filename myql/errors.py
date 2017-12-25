class NoTableSelectedError(Exception):
    
    '''Error raised when no table has been selected '''
    def __init__(self, msg=None):
        self.msg = msg

    ''' A better __str__ version '''
    def __str__(self):
        return "NoTableSelectedError('{}')".format(self.msg)
    
    ''' defining the special function __repr__ '''
    def __repr__(self):
        return '{}'.format(self.msg)
 
