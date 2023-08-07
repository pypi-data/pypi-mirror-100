cimport csample  # Import the pxd "header"
# Note for Numpy imports, the C import most come AFTER the Python import
# import numpy as np  # Import the Python Numpy
# cimport numpy as np  # Import the C Numpy

# Import some functionality from Python and the C stdlib
from cpython.pycapsule cimport *

# Python wrapper functions.
# Note that types can be delcared in the signature

def add(int a,int b):
    '''
    TODO: Python docstring
    '''
    # Call the imported DLL functions on the parameters.
    # Notice that we are passing a pointer to the first element in each array
    return csample.add(a,b)

def sub(int a,int b):
    '''
    TODO: Python docstring
    '''
    return csample.sub(a,b)
