def test_function(nodes):
    """
    :param nodes:
    :return:
    """
    x = nodes.coordinates[:, 0] - .1453
    y = nodes.coordinates[:, 1] - .16401
    return 1 + (x * y) ** 4 + (x * y) ** 8 + x ** 2 + y ** 2 + sum([x**n + y**n for n in range(1, 7)])


def dt_dx_analytical(nodes):
    """
    :param nodes:
    :return:
    """
    x = nodes.coordinates[:, 0] - .1453
    y = nodes.coordinates[:, 1] - .16401

    # Terms from the derived expression
    term1 = 1
    term2 = 2 * x
    term3 = 3 * x ** 2
    term4 = 4 * x ** 3
    term5 = 5 * x ** 4
    term6 = 6 * x ** 5
    term7 = 4 * x ** 3 * y ** 4
    term8 = 8 * x ** 7 * y ** 8

    return term1 + term2 + term3 + term4 + term5 + term6 + term7 + term8


def dt_dy_analytical(nodes):
    """
    :param nodes:
    :return:
    """
    x = nodes.coordinates[:, 0] - .1453
    y = nodes.coordinates[:, 1] - .16401

    # Terms from the derived expression for dϕ/dy0
    term1 = 1
    term2 = 2 * y
    term3 = 3 * y ** 2
    term4 = 4 * y ** 3
    term5 = 5 * y ** 4
    term6 = 6 * y ** 5
    term7 = 4 * y ** 3 * x ** 4
    term8 = 8 * y ** 7 * x ** 8

    return term1 + term2 + term3 + term4 + term5 + term6 + term7 + term8


def laplace_phi(nodes):
    """
    :param nodes:
    :return:
    """
    x = nodes.coordinates[:, 0] - .1453
    y = nodes.coordinates[:, 1] - .16401

    # Terms from the derived Laplacian of ϕ
    term1 = 4
    term2 = 6 * x
    term3 = 12 * x ** 2
    term4 = 20 * x ** 3
    term5 = 30 * x ** 4
    term6 = 6 * y
    term7 = 12 * y ** 2
    term8 = 12 * x ** 4 * y ** 2
    term9 = 20 * y ** 3
    term10 = 30 * y ** 4
    term11 = 12 * x ** 2 * y ** 4
    term12 = 56 * x ** 8 * y ** 6
    term13 = 56 * x ** 6 * y ** 8

    return term1 + term2 + term3 + term4 + term5 + term6 + term7 + term8 + term9 + term10 + term11 + term12 + term13





def dt_dx_do(nodes, discrete_operator, surface_value):
    """

    :param surface_value:
    :param nodes:
    :param discrete_operator:
    :return:
    """
    w_difx = discrete_operator.w_difX
    for i in w_difx:




    return


def dt_dy_do(nodes, discrete_operator, surface_value):
    """

    :param surface_value:
    :param nodes:
    :param discrete_operator:
    :return:
    """

    return


def laplace_do(nodes, discrete_operator, surface_value):
    """

    :param nodes:
    :param discrete_operator:
    :param surface_value:
    :return:
    """
    return