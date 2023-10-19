from Nodes_Functions import *
from DO_Functions import *
from Sim_Functions import *
from Plot_Functions import *

'''Simulation over a unit plane'''


class Simulation:
    def __init__(self, total_nodes, polynomial):
        self.total_nodes = total_nodes
        self.s = 1.0 / (total_nodes - 1)
        self.polynomial = polynomial
        self.h = calc_h(self.s, self.total_nodes)
        self.nodes = Nodes(self.total_nodes, self.s, self.h)
        self.discrete_operator = DiscreteOperator(self.nodes, self.polynomial, self.h)

    def plot_domain(self):
        return plot_nodes(self.nodes)

    def plot_neighbours(self, size=8):
        return show_neighbours(self.nodes, self.h, size)


class Nodes:
    def __init__(self, total_nodes, s, h):
        self.coordinates = create_nodes(total_nodes, s)
        self.in_domain = threshold(self.coordinates)
        self.dist_nodes = dist_nodes(self.coordinates, self.in_domain)
        self.neighbours_r, self.neighbours_xy = neighbour_nodes(self.dist_nodes, h)


class DiscreteOperator:
    def __init__(self, nodes, polynomial, h):
        self.monomial = calc_monomial(nodes, polynomial, h)
        self.ABF = calc_abf(nodes, h, polynomial)
        self.M = calc_m(self.ABF, self.monomial)
        self.w_difX = do_weights(self.M, self.ABF, polynomial, 'x')
        self.w_difY = do_weights(self.M, self.ABF, polynomial, 'y')
        self.w_Laplace = do_weights(self.M, self.ABF, polynomial, 'Laplace')


sim = Simulation(50, 2)


# To check matrix condition
# import numpy as np
# np.linalg.cond(sim.discrete_operator.M[0])
