from Functions_LABFM import calc_h
from Functions_LABFM import create_nodes
from Functions_LABFM import neighbour_nodes
from Functions_LABFM import threshold
from Functions_LABFM import dist_nodes
from Functions_LABFM import calc_monomial
from Functions_LABFM import calc_abf


'''Simulation over a unit plane'''


class Simulation:
    def __init__(self, total_nodes, s):
        self.total_nodes = total_nodes
        self.s           = s
        self.polynomial  = 1  # Order of approximation that will be used in monomial
        self.h           = calc_h(self.s, self.total_nodes)
        self.nodes       = Nodes(self.total_nodes, self.s, self.h)
        self.discrete_operator = DiscreteOperator(self.nodes, self.polynomial, self.h)


class Nodes:
    def __init__(self, total_nodes, s, h):
        self.coordinates = create_nodes(total_nodes, s)
        self.in_domain   = threshold(self.coordinates)
        self.dist_nodes  = dist_nodes(self.coordinates,self.in_domain)  # this attribute might be in
        self.neighbours_r, self.neighbours_xy = neighbour_nodes(self.dist_nodes, h)


class DiscreteOperator:
    def __init__(self, nodes, polynomial, h):
        self.monomial = calc_monomial(nodes, polynomial)
        self.ABF      = calc_abf(nodes, h, polynomial)
        #self.M = calc_M(nodes) # Still need to be written



sim = Simulation(100,0.01)