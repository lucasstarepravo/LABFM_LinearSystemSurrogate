from Nodes_Functions import *
from DO_Functions import *
from Sim_Functions import *
from Plot_Functions import *
from Test_Functions import *

'''Simulation over a unit plane'''


class Simulation:
    def __init__(self, total_nodes, polynomial):
        self.total_nodes       = total_nodes
        self.s                 = 1.0 / (total_nodes - 1)
        self.polynomial        = polynomial
        self.h                 = calc_h(self.s, self.polynomial)
        self.nodes             = Nodes(self.total_nodes, self.s, self.h, self.polynomial)
        self.discrete_operator = DiscreteOperator(self.nodes, self.polynomial, self.h)
        self.test_function     = TestFunction(self.nodes, self.discrete_operator)

    def plot_neighbours(self, size=8):
        return show_neighbours(self.nodes, self.h, size)

    def plot_l2(self, size=8):
        return show_l2(self.nodes, self.test_function, size)


class Nodes:
    def __init__(self, total_nodes, s, h, polynomial):
        self.coordinates = create_nodes(total_nodes, s, polynomial)
        self.in_domain   = threshold(self.coordinates)
        self.dist_nodes  = dist_nodes(self.coordinates, self.in_domain)
        self.neighbours_r, self.neighbours_xy, self.neighbours_coor = neighbour_nodes(self.dist_nodes, h, self.coordinates)


class DiscreteOperator:
    def __init__(self, nodes, polynomial, h):
        self.monomial  = calc_monomial(nodes, polynomial, h)
        self.ABF       = calc_abf(nodes, h, polynomial)
        self.M         = calc_m(self.ABF, self.monomial)
        self.w_difX    = do_weights(self.M, self.ABF, polynomial, 'x')
        self.w_difY    = do_weights(self.M, self.ABF, polynomial, 'y')
        self.w_Laplace = do_weights(self.M, self.ABF, polynomial, 'Laplace')


class TestFunction:
    def __init__(self, nodes, discrete_operator):
        self.surface_value = test_function(nodes)
        self.dtdx_true     = dif_analytical(nodes, 'dtdx')
        self.dtdy_true     = dif_analytical(nodes, 'dtdy')
        self.laplace_phi   = laplace_phi(nodes)
        self.dT_dx_DO      = dif_do(nodes, discrete_operator, self.surface_value, 'dtdx')
        self.dT_dy_DO      = dif_do(nodes, discrete_operator, self.surface_value, 'dtdy')
        #self.laplace_DO    = laplace_do(nodes, discrete_operator, self.surface_value)


sim = Simulation(40, 4)

# To check matrix condition
# import numpy as np
# np.linalg.cond(sim.discrete_operator.M[0])
