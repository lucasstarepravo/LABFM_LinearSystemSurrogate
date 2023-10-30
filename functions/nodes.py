import numpy as np


def calc_h(s, polynomial):
    """

    :param s:
    :param polynomial:
    :return:
    """
    if polynomial == 2:
        h = 1.2 * s
    elif polynomial == 4:
        h = 1.5 * s
    elif polynomial == 6:
        h = 2.3 * s
    elif polynomial == 8:
        h = 2.5 * s
    else:
        raise ValueError("The polynomial argument must be 2, 4, 6, or 8")

    return h


def create_nodes(total_nodes, s, polynomial):
    """
    :param total_nodes: is a scalar that states the number of nodes we would like to have inside the domain
    :param s: is a scalar that determines the average distance between points inside the comp. stencil
    :return:
    coordinates: is a numpy array that contains all coordinates of nodes, the first and second column contain the x and
    y coordinates, respectively. It is possible to access the ith node with "coordinates[i]"
    """
    delta = 1.0 / (total_nodes - 1)  # Determine the spacing delta between the points in the original domain
    h = calc_h(s, polynomial)
    n = int(2 * h / delta)  # Calculate the number of points to be added on each side
    x = np.linspace(0 - 2 * h, 1 + 2 * h, total_nodes + 2 * n)  # Creates x coordinates with boundary
    y = np.linspace(0 - 2 * h, 1 + 2 * h, total_nodes + 2 * n)  # Creates y coordinates with boundary

    X, Y = np.meshgrid(x, y)  # Create a 2D grid of x and y coordinates

    # Perturb the coordinates
    X = X + (np.random.choice([1, -1], X.shape) * np.random.uniform(0, s / 4, X.shape))
    Y = Y + (np.random.choice([1, -1], Y.shape) * np.random.uniform(0, s / 4, Y.shape))

    # Stack the perturbed coordinates
    coordinates = np.column_stack((X.ravel(), Y.ravel()))
    coordinates = np.around(coordinates, 11)

    return coordinates


def neighbour_nodes(coordinates, ref_node, h):

    neigh_r_d = []
    neigh_xy_d = []
    neigh_coor = []

    for index, (x_i, y_i) in enumerate(coordinates):
        distance = ((x_i - ref_node[0]) ** 2 + (y_i - ref_node[1]) ** 2) ** 0.5
        if distance <= 2 * h:
            neigh_r_d.append([round(distance, 11)])
            neigh_xy_d.append([round(x_i - ref_node[0], 11), round(y_i - ref_node[1], 11)])
            neigh_coor.append([round(x_i, 11), round(y_i, 11)])
        else:
            continue
    return np.array(neigh_r_d), np.array(neigh_xy_d), np.array(neigh_coor)