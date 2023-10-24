import numpy as np
import matplotlib.pyplot as plt
from Test_Functions import create_dict


def show_neighbours(nodes, size):
    neigh_coor = nodes.neighbours_coor
    coor = nodes.coordinates
    out_domain = []

    keys_array = np.array(list(neigh_coor.keys()))

    while True:
        sample = keys_array[np.random.choice(len(keys_array))]
        if 0 <= sample[0] <= 1 and 0 <= sample[1] <= 1:
            ref_node = sample
            break

    for x_i, y_i in coor:
        if x_i < 0 or x_i > 1 or y_i < 0 or y_i > 1:
            out_domain.append([x_i, y_i])

    neigh = np.array(neigh_coor[tuple(ref_node)])
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


def plot_weights(nodes, discrete_operator, size, derivative):
    coor = nodes.coordinates
    while True:
        sample = coor[np.random.choice(coor.shape[0])]
        if 0 <= sample[0] <= 1 and 0 <= sample[1] <= 1:
            ref_node = sample
            break

    ref_neigh = np.array(nodes.neighbours_coor[tuple(ref_node)])
    index_to_delete = np.where((ref_neigh == ref_node).all(axis=1))
    mask = ~np.all(ref_neigh == ref_node, axis=1)
    ref_neigh = ref_neigh[mask]

    if derivative == 'dtdx':
        ref_weights = discrete_operator.w_difX[tuple(ref_node)]
    elif derivative == 'dtdy':
        ref_weights = discrete_operator.w_difY[tuple(ref_node)]

    ref_weights = np.delete(ref_weights, index_to_delete[0])

    plt.scatter(ref_node[0], ref_node[1], c='black', label='Reference Node', s=size)
    plt.scatter(ref_neigh[:, 0], ref_neigh[:, 1], c=ref_weights, label='Neighbour nodes', s=size, cmap='bwr')
    plt.colorbar()
    plt.legend()
    plt.show()
    return
