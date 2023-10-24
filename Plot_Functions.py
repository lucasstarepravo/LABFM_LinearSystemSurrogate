import numpy as np
import matplotlib.pyplot as plt
from Test_Functions import create_dict


def show_neighbours(nodes, h, size):
    coor = nodes.coordinates
    neigh = []
    out_domain = []

    while True:
        sample = coor[np.random.choice(coor.shape[0])]
        if 0 <= sample[0] <= 1 and 0 <= sample[1] <= 1:
            ref_node = sample
            break

    for x_j, y_j in coor:
        r_distance = ((x_j - ref_node[0]) ** 2 + (y_j - ref_node[1]) ** 2) ** .5
        if r_distance <= 2 * h:
            neigh.append([x_j, y_j])

    for x_i, y_i in coor:
        if x_i < 0 or x_i > 1 or y_i < 0 or y_i > 1:
            out_domain.append([x_i, y_i])

    neigh = np.array(neigh)
    out_domain = np.array(out_domain)

    plt.scatter(coor[:, 0], coor[:, 1], c='blue', label='All Nodes', s=size)
    plt.scatter(out_domain[:, 0], out_domain[:, 1], c='grey', label='Out of Domain', s=size)
    plt.scatter(neigh[:, 0], neigh[:, 1], c='red', label='Neighbours', s=size)
    plt.scatter(ref_node[0], ref_node[1], c='yellow', label='Reference Node', s=size)
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.title('Nodes and Neighbours')
    plt.legend()
    plt.axis('equal')
    plt.grid(True)
    plt.show()

    return


def plot_weights(nodes, discrete_operator, size):
    coor = nodes.coordinates
    while True:
        sample = coor[np.random.choice(coor.shape[0])]
        if 0 <= sample[0] <= 1 and 0 <= sample[1] <= 1:
            ref_node = sample
            break

    w_difx = create_dict(discrete_operator.w_difX, nodes.coordinates, nodes.in_domain)

    ref_weights = np.array(discrete_operator.w_difX[tuple(ref_node)])
    ref_neigh = np.array(nodes.neighbours_coor[np.where(coor == ref_node)[0][0]])
    plt.scatter(ref_node[0], ref_node[1], c='blue', label='Reference Node', s=size)
    plt.scatter(ref_neigh[:, 0], ref_neigh[:, 1], c=ref_weights, label='Neighbour nodes', s=size, cmap='viridis')
    plt.colorbar()
    plt.legend()
    plt.show()
    return