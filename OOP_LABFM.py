from Nodes_Functions import *
from DO_Functions import *
from Sim_Functions import *
from Plot_Functions import *

'''Simulation over a unit plane'''


class Simulation:
    def __init__(self, total_nodes, s):
        self.total_nodes = total_nodes
        self.s = s
        self.polynomial = 2  # Order of approximation that will be used in monomial
        self.h = calc_h(self.s, self.total_nodes)
        self.nodes = Nodes(self.total_nodes, self.s, self.h)
        self.discrete_operator = DiscreteOperator(self.nodes, self.polynomial, self.h)
        self.plot = Plot(self.nodes, self.h)


class Nodes:
    def __init__(self, total_nodes, s, h):
        self.coordinates = create_nodes(total_nodes, s)
        self.in_domain = threshold(self.coordinates)
        self.dist_nodes = dist_nodes(self.coordinates, self.in_domain)  # this attribute might be in
        self.neighbours_r, self.neighbours_xy = neighbour_nodes(self.dist_nodes, h)


class DiscreteOperator:
    def __init__(self, nodes, polynomial, h):
        self.monomial = calc_monomial(nodes, polynomial, h)
        self.ABF = calc_abf(nodes, h,
                            polynomial)  # When calculating the weights, should radius be magnitude or have a direction?
        self.M = calc_m(self.ABF, self.monomial)


class Plot:
    def __init__(self, nodes, h):
        self._nodes = nodes
        self._h = h
        self._domain = None
        self._neighbours = None

    @property
    def domain(self):
        if self._domain is None:
            self._domain = plot_nodes(self._nodes)
        return self._domain

    @property
    def neighbours(self):
        if self._neighbours is None:
            self._neighbours = show_neighbours(self._nodes, self._h)
        return self._neighbours


sim = Simulation(30, 0.05)

# To check matrix condition
# import numpy as np
# np.linalg.cond(sim.discrete_operator.M[0])
