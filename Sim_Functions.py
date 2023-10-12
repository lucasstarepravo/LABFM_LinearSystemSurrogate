import numpy as np
import math


def calc_h(s, total_nodes):
    """FOR NOW THIS WILL BE LEFT 0.1 for now"""
    h = 0.05  # s*()
    return h


def pointing_v(m, approximation):
    """

    :param m:
    :param approximation:
    :return:
    """
    n = (m**2 + 3*m)/2
    cd = np.zeros((n,1))
    if approximation == 'x':
        cd[0] = 1
    elif approximation == 'y':
        cd[1] = 1
    elif approximation == 'Laplace':
        cd[2] = 2
        cd[4] = 4
    return cd


def solve_weights(m, cd, approximation):

    return