import matplotlib
import numpy as np

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def plot_nodes(nodes):
    plt.scatter(nodes.coordinates[:, 0], nodes.coordinates[:, 1], marker='o')

    return plt.show()


def show_neighbours(nodes, h):
    coor = nodes.coordinates
    neigh = []


    ref_index = np.random.randint(0, len(coor))
    ref_node = coor[ref_index]

    while True:
        sample = coor[np.random.choice(coor.shape[0])]
        if 0 <= sample[0] <= 1 and 0 <= sample[1] <= 1:
            ref_node = sample
            break

    for x_j, y_j in coor:
        r_distance = ((x_j - ref_node[0]) ** 2 + (y_j - ref_node[1]) ** 2) ** .5
        if r_distance <= 2 * h:
            neigh.append([x_j, y_j])

    neigh = np.array(neigh)
    plt.scatter(coor[:, 0], coor[:, 1], c='blue', label='All Nodes')
    plt.scatter(neigh[:, 0], neigh[:, 1], c='red', label='Neighbours')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.title('Nodes and Neighbours')
    plt.legend()
    plt.axis('equal')
    plt.grid(True)

    return plt.show()
