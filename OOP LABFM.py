import numpy as np
from Functions_LABFM import calc_h
from Functions_LABFM import create_nodes
from Functions_LABFM import neighbour_nodes
from Functions_LABFM import threshold
from Functions_LABFM import dist_nodes
from Functions_LABFM import calc_monomial


'''Simulation over a unit plane'''


class Simulation:
    def __init__(self, total_nodes, s):
        self.total_nodes = total_nodes
        self.s           = s
        self.polynomial  = 1  # Order of polynomial we want to approximate
        self.h           = calc_h(self.s, self.total_nodes)
        self.nodes       = Nodes(self.total_nodes, self.s, self.h)
        self.discrete_operator = DiscreteOperator(self.nodes,self.polynomial)


class Nodes:
    def __init__(self, total_nodes, s, h):
        self.h           = h
        self.coordinates = create_nodes(total_nodes, s)
        self.in_domain   = threshold(self.coordinates)
        self.dist_nodes  = dist_nodes(self.coordinates,self.in_domain)  # this attribute might be in
        self.neighbours_r, self.neighbours_xy = neighbour_nodes(self.dist_nodes, self.h)


class DiscreteOperator:
    def __init__(self, nodes, polynomial):
        self.monomial = calc_monomial(nodes, polynomial)
        #self.M = calc_M(nodes) # Still need to be written



sim = Simulation(100,0.01)