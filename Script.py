import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Define the number of nodes
total_nodes = 100

# Generate the first list of random values
'''Here the dimensions of the domain go from 0 to 1, which means that the current domain is a plate of 1x1'''
x = np.random.uniform(0, 1, total_nodes)
y = np.random.uniform(0, 1, total_nodes)

# Defining parameters
h = 0.05
pi = 3.141592653589793238462643383279
# r = np.sqrt(np.square(x) + np.square(y))


N_inside = {} # N_inside has the values 
'''First, we need to determine which points are inside the computational stencil'''
''' The loop line below scales with O(N^2)'''
for i in range(total_nodes):                                    # Looping each reference particle
    N_inside[i] = []
    for j in range(total_nodes):                                # Looping in all particles in the domain to see which ones are inside the comp. domain
        dis_bet_points = ((x[j]-x[i])**2+(y[j]-y[i])**2)**0.5   # Measuring distance between nodes
        if j == 0:
            N_inside[i] = [[x[i], y[i]]]
        if abs(dis_bet_points) <= 2*h:                               # Checking if nodes are inside the comp stencil
            N_inside[i].append([x[j], y[j]])                       # if nodes are inside the computational stencil of particle i, it will be saved in a dictonary, where the key is the reference particle and the values are all the particles within the stencil


def calculate_Wji(x,r,j):

    return

def calculate_scaled_monomial(x,y,N_inside,m): #This only works for m = 1
    """

    :param x: Nodal coordinates at x
    :param y: Nodal coordinates at y
    :param j:
    :param m: order of monomial
    :return:
    """
    for i in range(m):

    return X_ij

# Defining the ABF
"""Lets assume for now we are only interested in the first spatial derivatives.
So we will consider only the cases where d=x and d=y"""
for j in range(total_nodes):
    W_ji = 1

