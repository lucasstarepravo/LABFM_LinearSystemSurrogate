from Sim_Functions import calc_h
from Nodes_Functions import create_nodes
from Nodes_Functions import neighbour_nodes
from Nodes_Functions import threshold
from Nodes_Functions import dist_nodes
from DO_Functions import calc_monomial
from DO_Functions import calc_abf
from DO_Functions import calc_m
import matplotlib as plt

'''Simulation over a unit plane'''


class Simulation:
    def __init__(self, total_nodes, s):
        self.total_nodes = total_nodes
        self.s = s
        self.polynomial = 2  # Order of approximation that will be used in monomial
        self.h = calc_h(self.s, self.total_nodes)
        self.nodes = Nodes(self.total_nodes, self.s, self.h)
        self.discrete_operator = DiscreteOperator(self.nodes, self.polynomial, self.h)


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


sim = Simulation(1000, 0.01)

# To check matrix condition
# import numpy as np
# np.linalg.cond(sim.discrete_operator.M[0])
