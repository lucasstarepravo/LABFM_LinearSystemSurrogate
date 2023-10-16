import numpy as np
import math


def calc_h(s, total_nodes):
    """FOR NOW THIS WILL BE LEFT 0.1 for now"""
    h = 0.05  # s*()
    return h


def pointing_v(polynomial, d):
    """

    :param polynomial:
    :param d:
    :return:
    """

    if d not in ["x", "y", "Laplace"]:
        raise ValueError("The valid_string argument must be 'x', 'y', or 'Laplace'")

    n = int((polynomial ** 2 + 3 * polynomial) / 2)
    cd = np.zeros((n, 1))
    if d == 'x':
        cd[0] = 1
    elif d == 'y':
        cd[1] = 1
    elif d == 'Laplace':
        cd[2] = 2
        cd[4] = 4
    return cd


def do_weights(m, abf, polynomial, d):
    """

    :param m:
    :param abf:
    :param polynomial:
    :param d:
    :return:
    """
    w_dif = {}
    cd = pointing_v(polynomial, d)

    for ref_node_i in m:
        w_dif[ref_node_i] = np.zeros((abf[ref_node_i].shape[0], 1))
        psi_w = np.linalg.solve(m[ref_node_i], cd)
        w_dif[ref_node_i] = abf[ref_node_i] @ psi_w

    return w_dif
