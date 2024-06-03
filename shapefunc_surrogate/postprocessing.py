import numpy as np
import math


def rescale_output(predicted_psi, h, dtype):
    if dtype not in ['laplace', 'x', 'y']:
        raise ValueError('dtype variable must be "laplace", "x" or "y"')

    if dtype == 'laplace':
        h = h**2

    scaled_psi = predicted_psi/h

    return scaled_psi
