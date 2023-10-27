from Nodes_Functions import *
from DO_Functions import *
from Sim_Functions import *
from Plot_Functions import *
from Test_Functions import *

'''Simulation over a unit plane'''


class Simulation:
    def __init__(self, total_nodes, polynomial):
        self.total_nodes = total_nodes
        self.s = 1.0 / total_nodes
        self.polynomial = polynomial
        self.h = calc_h(self.s, self.polynomial)
        self.nodes = Nodes(self.total_nodes, self.s, self.h, self.polynomial)
        self.discrete_operator = DiscreteOperator(self.nodes, self.polynomial, self.h)
        self.test_function = TestFunction(self.nodes, self.discrete_operator)
        self.dtdx_l2 = calc_l2(self.test_function, 'dtdx')
        self.dtdy_l2 = calc_l2(self.test_function, 'dtdy')
        self.laplace_l2 = calc_l2(self.test_function, 'Laplace')

    def plot_neighbours(self, size=8):
        return show_neighbours(self.nodes, size)

    def plot_weights(self, size=80, derivative='dtdx'):
        return plot_weights(self.nodes, self.discrete_operator, size, derivative)


class Nodes:
    def __init__(self, total_nodes, s, h, polynomial):
        self.coordinates = create_nodes(total_nodes, s, polynomial)
        self.in_domain = threshold(self.coordinates)
        self.dist_nodes = dist_nodes(self.coordinates, self.in_domain)
        self.neighbours_r, self.neighbours_xy, self.neighbours_coor = neighbour_nodes(self.dist_nodes, h,
                                                                                      self.coordinates)


class DiscreteOperator:
    def __init__(self, nodes, polynomial, h):
        self.monomial = calc_monomial(nodes, polynomial, h)
        self.ABF = calc_abf(nodes, h, polynomial)
        self.M = calc_m(self.ABF, self.monomial)
        self.w_difX = do_weights(self.M, self.ABF, polynomial, h, 'x')
        self.w_difY = do_weights(self.M, self.ABF, polynomial, h, 'y')
        self.w_Laplace = do_weights(self.M, self.ABF, polynomial, h, 'Laplace')


class TestFunction:
    def __init__(self, nodes, discrete_operator):
        self.surface_value = test_function(nodes)
        self.dtdx_true = dif_analytical(nodes, 'dtdx')
        self.dtdy_true = dif_analytical(nodes, 'dtdy')
        self.laplace_true = laplace_phi(nodes)
        self.dtdx_DO = dif_do(nodes, discrete_operator, self.surface_value, 'dtdx')
        self.dtdy_DO = dif_do(nodes, discrete_operator, self.surface_value, 'dtdy')
        self.laplace_DO = dif_do(nodes, discrete_operator, self.surface_value, 'Laplace')


def run(total_nodes_list, polynomial_list):
    result = {}
    for total_nodes, polynomial in zip(total_nodes_list, polynomial_list):
        sim = Simulation(total_nodes, polynomial)
        result[(total_nodes, polynomial)] = sim
    return result


if __name__ == "__main__":
    total_nodes_list = [10, 10, 10, 50, 50, 50]
    polynomial_list = [2, 4, 6, 2, 4, 6]
    results = run(total_nodes_list, polynomial_list)
