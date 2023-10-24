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
    norm = np.sqrt(np.array([dt_analy[ref_node] ** 2 for ref_node in dt_analy]))
    l2 = np.sqrt(np.sum(l2))/np.sum(norm)
    return l2
