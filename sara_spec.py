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


def trace_order(data, y_start, width = 6, x_middle=1000):
    '''
    Find the location of the order starting from the order position in the middle of the detector

    For each orders, I start with column x_middle(=1000),
    take a few rows around the central value (width = 6),
    and then find the peak again.
    If the new peak is more than a few pixels from the previous pixel,
    I ignore this value.
    The integer peak value for each column is then passed to a low order polyfit.
    The float value of the polyfit for each column is written to a file.

    :param data: the image to be traced (2D numpy array)
    :param y_start: the pixel position of the order at cross-dispersion coordinate x_middle
    :param width: width of cross-dispersion pixel width for peak finding (default=6)
    :param x_middle: the cross-dispersion column that was used to find y_start.
    :rtype (xx, yo_img): xx column index array, yo_img: position of the trace for each column. 

'''

    #x_middle = 1000 # This is where the peak is found in the code below
    nx = data.shape[1] # The number of wavelength column. The overscan values have been masked by the previous notebook

    yo_est = [] # Empty arrays to store the peak pixels
    xo_est = []

    #start with the right side
    y = copy(y_start) # keep a copy of y for each iteration, as the next will use a few pixels above and below
    for xi in range(x_middle, nx): # go from the x_middle to the end of the CCD

        yindex = np.arange( y-width, y+width+1, 1 ) # select a few pixels on each side of the current y value
        peaks, props = find_peaks( data[yindex,xi] ) # use the find_peak function to find the peak

        if peaks.size > 0: # if at least a peak is found
            toto = yindex[peaks[0]] #select the first peak
            if np.abs(toto-y) < 2: #if the new peak is not too far from the older peak
                yo_est.append(toto) # keep the value
                xo_est.append(xi)
                y = toto # update the y location of the current peak

    y = copy(y_start)
    for xi in range(x_middle-1, 0, -1):

        yindex = np.arange( y-width, y+width+1, 1 )
        peaks, props = find_peaks( data[yindex,xi] )

        if peaks.size > 0:
            toto = yindex[peaks[0]]
            if np.abs(toto-y) < 2:
                yo_est.append(toto)
                xo_est.append(xi)
                y = toto

    # create a low order polyfit of the peak values.
    trace_fit = np.polyfit(xo_est, yo_est, 4) # this function returns the best fit coefficients.
    # Create a polynomial function based on the best fit poly coefficients
    trace_poly = np.poly1d(trace_fit)
    # Create a x array for all the columns
    xx = np.arange(0,nx,1)
    # get the y value from the fit for each column.
    yo_img = trace_poly(xx)

    return(xx, yo_img)
