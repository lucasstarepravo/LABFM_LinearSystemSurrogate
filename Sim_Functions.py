import numpy as np


def calc_h(s, polynomial):
    """

    :param s:
    :param polynomial:
    :return:
    """
    if polynomial == 2:
        h = 1.2 * s
    elif polynomial == 4:
        h = 1.5 * s
    elif polynomial == 6:
        h = 2 * s
    elif polynomial == 8:
        h = 2.5 * s
    else:
        raise ValueError("The polynomial argument must be 2, 4, 6, or 8")

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


def calc_l2(test_function, derivative):

    if derivative not in ['dtdx', 'dtdy']:
        raise ValueError("Invalid derivative type")

    if derivative == 'dtdx':
        dt_analy = test_function.dtdx_true
        dt_aprox = test_function.dtdx_DO
    elif derivative == 'dtdy':
        dt_analy = test_function.dtdy_true
        dt_aprox = test_function.dtdy_DO
    #else:
    #    dx_analy = test_function.laplace_true
    #    dx_aprox = test_function.laplace_DO

    l2 = np.array([(dt_analy[ref_node] - dt_aprox[ref_node]) ** 2 for ref_node in dt_aprox])
    l2 = np.sqrt(np.sum(l2) / l2.size)
    return l2
