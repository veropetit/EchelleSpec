# Module for functions related to the sara-spec reduction tools

import matplotlib.pyplot as plt
from copy import copy
import numpy as np



def get_cmap():
    '''Return red cmap with masked values in purple'''
    cmap = copy(plt.cm.Reds)
    cmap.set_bad('purple', 1.0) # the masked values are masked (the 1 is for the alpha)
    return(cmap)
    
def get_cmap_sat():
    '''Return red cmap with masked values in purple and over/under in green/blue'''
    cmap_sat = copy(plt.cm.Reds)
    cmap_sat.set_over('green', 1.0)
    cmap_sat.set_under('blue', 1.0)
    cmap_sat.set_bad('purple', 1.0) # the masked values are masked (the 1 is for the alpha)
    return(cmap_sat)

def write_overscan(length, width, left, right):
    '''Write the CCD size and overscan information to a file
    
    The overscan is written as 01-CalibrationMasters/overscan.dat
    
    :param length: the long size of the CCD (the dispersion direction, columns)
    :param width: the short size of the CCD (the cross-dispersion direction, rows)
    :param left: the column at which the overscan ends on the left size of the ccd (thus ignoring column 0-left)
    :param right: the column at which the overscan stars on the right size of the ccd (thus ignoring column right-length)
    
    .. todo:: Add checks that right<left, and right <= length
    
    '''
    np.savetxt( '01-CalibrationMasters/overscan.dat', np.array([length, width, left, right], dtype='int').T )

def read_overscan(file='01-CalibrationMasters/overscan.dat'):
    '''Read in the overscan information written by write_overscan
    
    :param file: the name of the overscanfile
    :returns: length, width, left, right overscan parameters.
    
    '''
    overscan = np.loadtxt(file)
    length = int(overscan[0])
    width = int(overscan[1])
    left = int(overscan[2])
    right = int(overscan[3])
    return(length, width, left, right)
