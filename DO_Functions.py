import numpy as np
import math


def scaling_matrix(monomial_exponent, h):
    """

    :param monomial_exponent:
    :param h:
    :return:
    """
    scaling_m = np.zeros((len(monomial_exponent), 1))
    index = 0
    for exp_x, exp_y in monomial_exponent:
        exp_h = -(exp_x + exp_y)
        scaling_m[index] = h ** exp_h
        index = index + 1
    return scaling_m


def monomial_power(polynomial):
    """

    :param polynomial:
    :return:
    """
    monomial_exponent = [(total_polynomial - i, i)
                         for total_polynomial in range(1, polynomial + 1)
                         for i in range(total_polynomial + 1)]
    return np.array(monomial_exponent)


def calc_monomial(nodes, m, h):
    """

    :param h:
    :param nodes:
    :param m:
    :return:
    """
    neighbours = nodes.neighbours_xy
    monomials = {}
    m_power = monomial_power(m)

    for key1 in neighbours:
        if neighbours[key1] is None:
            monomials[key1] = None
        else:
            index1 = 0
            monomials[key1] = np.zeros((len(neighbours[key1]), len(m_power)))
            for power_x, power_y in m_power:
                monomials[key1][:, index1] = (np.array(neighbours[key1])[:, 0] ** power_x * np.array(neighbours[key1])[:, 1] ** power_y) / (
                                                     math.factorial(power_x) * math.factorial(power_y))
                index1 = index1 + 1

    scaling_v = scaling_matrix(m_power, h).reshape(-1, 1)

    for key in monomials:
        if monomials[key] is None:
            continue
        else:
            for row in range(len(monomials[key])):
                monomials[key][row, :] = monomials[key][row, :] * scaling_v.T

    return monomials


def calc_hp(exp_a, coordinates, h):
    """
    This function gives the first 10 expansions of the Hermite polynomial
    :param exp_a:
    :param coordinates:
    :param h:
    :return:
    """

    z = coordinates / (h * (2 ** .5))

    if exp_a == 0:
        h = 1

    elif exp_a == 1:
        h = 2 * z

    elif exp_a == 2:
        h = 4 * z ** 2 - 2

    elif exp_a == 3:
        h = 8 * z ** 3 - 12 * z

    elif exp_a == 4:
        h = 16 * z ** 4 - 48 * z ** 2 + 12

    elif exp_a == 5:
        h = 32 * z ** 5 - 160 * z ** 3 + 120 * z

    elif exp_a == 6:
        h = 64 * z ** 6 - 480 * z ** 4 + 720 * z ** 2 - 120

    elif exp_a == 7:
        h = 128 * z ** 7 - 1344 * z ** 5 + 3360 * z ** 3 - 1680 * z

    elif exp_a == 8:
        h = 256 * z ** 8 - 3584 * z ** 6 + 13440 * z ** 4 - 13440 * z ** 2 + 1680

    elif exp_a == 9:
        h = 512 * z ** 9 - 9216 * z ** 7 + 48384 * z ** 5 - 80640 * z ** 3 + 30240 * z

    elif exp_a == 10:
        h = 1024 * z ** 10 - 23040 * z ** 8 + 161280 * z ** 6 - 403200 * z ** 4 + 302400 * z ** 2 - 30240

    else:
        raise ValueError("Invalid value for polynomial. The polynomial must be a polynomial that can be handled by "
                         "the simulation. Try lowering the value of the polynomial")

    return h


def gaussian_rbf(neighbours_r, h):
    """

    :param neighbours_r:
    :param h:
    :return:
    """

    q = neighbours_r / h

    w_ji = (9 / math.pi) * math.exp(-9 * (q ** 2))

    return w_ji


def calc_abf(nodes, h, polynomial):  # Needs to be written
    """

    :param polynomial:
    :param nodes:
    :param h:
    :return:
    """
    neigh_r = nodes.neighbours_r
    neigh_xy = nodes.neighbours_xy
    basis_func = {}
    m_power = monomial_power(polynomial)
    n = len(m_power)

    for ref_node in neigh_r:
        if neigh_r[ref_node] is None:
            basis_func[ref_node] = None
        else:
            basis_func[ref_node] = np.zeros((len(neigh_r[ref_node]), n))
            for j in range(len(neigh_r[ref_node])):
                w_jid = []
                for k in range(n):
                    w_jid.append(
                        gaussian_rbf(neigh_r[ref_node][j], h) / ((2 ** (m_power[k, 0] + m_power[k, 1])) ** .5) * \
                        calc_hp(m_power[k, 0], neigh_xy[ref_node][j][0], h) * \
                        calc_hp(m_power[k, 1], neigh_xy[ref_node][j][1], h))
                basis_func[ref_node][j, :] = np.array(w_jid)

    return basis_func


def calc_m(basis_func, monomial):
    """

    :param monomial:
    :param basis_func:
    :return:
    """
    m = {}
    for ref_node in basis_func:
        if basis_func[ref_node] is None:
            m[ref_node] = None
        else:
            m[ref_node] = np.zeros((basis_func[ref_node].shape[1], monomial[ref_node].shape[1]))
            for j in range(len(basis_func[ref_node])):
                m[ref_node] = m[ref_node] + np.outer(monomial[ref_node][j], basis_func[ref_node][j])

    return m


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
        cd[2] = 1
        cd[4] = 1
    return cd


def do_weights(m, abf, polynomial, h, derivative):
    """

    :param derivative:
    :param h:
    :param m:
    :param abf:
    :param polynomial:
    :return:
    """
    w_dif = {}
    cd = pointing_v(polynomial, derivative)
    m_power = monomial_power(polynomial)
    scaling_v = scaling_matrix(m_power, h).reshape(-1, 1)
    cd = cd * scaling_v

    for ref_node in m:
        if m[ref_node] is None:
            w_dif[ref_node] = None
        else:
            w_dif[ref_node] = np.zeros((abf[ref_node].shape[0], 1))
            psi_w = np.linalg.solve(m[ref_node], cd)
            w_dif[ref_node] = abf[ref_node] @ psi_w

    return w_dif
