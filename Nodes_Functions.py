from Sim_Functions import calc_h
import numpy as np


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


def threshold(coordinates):  # check whether the node is inside or outside the domain
    """
    This function assumes that the domain is from 0 to 1 in the dimensions x and y. This function allows you to access
    the nodes which are inside the domain and which nodes will be used as boundary
    :param coordinates: list of lists containing the coordinates of all nodes
    :return: return a list stating whether a point is inside the domain or not (i.e., it is a reference node or not)
    """
    in_domain = {}
    for x_i, y_i in coordinates:
        if x_i > 1 or x_i < 0 or y_i > 1 or y_i < 0:
            in_domain[(x_i, y_i)] = False
        else:
            in_domain[(x_i, y_i)] = True

    return in_domain


def dist_nodes(coordinates, in_domain):
    """

    :param coordinates:
    :param in_domain:
    :return: distance(dict): For points that are outside the domain (Boundary
    points), the value of the key will be None. Since we don't need to calculate the distance of nodes outside the
    boundary to every other node. For nodes within the domain, for each key, there will be a list, each value of the
    list, is another list with 2 items. The first item is the x distance from the reference point, the second item is
    the y distance from the point
    """

    distance = {}
    for x_i, y_i in coordinates:
        distance[(x_i, y_i)] = []
        if not in_domain[(x_i, y_i)]:
            distance[(x_i, y_i)] = None
        else:
            for x_j, y_j in coordinates:
                x_dist = (x_j - x_i)
                y_dist = (y_j - y_i)
                distance[(x_i, y_i)].append([x_dist, y_dist])

    return distance


def neighbour_nodes(distance, h, coordinates):
    """
    :param coordinates:
    :param h:
    :param distance:
    :return:
    neighbours(dict): each key of the dictionary refers to a node. If the value of the key is None, it means the particle
    is outside the domain. if the node is inside the domain, the value of the key will be a list, where each value of the
    list corresponds to the radial distance between the reference point and the neighbours. Note that inside the neighbours
    list there will also be the reference point inside, with distance (0,0)
    """
    neighbours_radius = {}
    neighbours_cartesian = {}
    neighbours_coordinates = {}

    for index, (key, neigh_dist) in enumerate(distance.items()):
        if neigh_dist is None:
            neighbours_radius[key] = neighbours_cartesian[key] = neighbours_coordinates[key] = None
        else:
            neighbours_radius[key] = []
            neighbours_cartesian[key] = []
            neighbours_coordinates[key] = []

            for dis_x, dis_y in neigh_dist:
                r_distance = (dis_x ** 2 + dis_y ** 2) ** 0.5
                if r_distance <= 2 * h:
                    neighbours_radius[key].append(round(r_distance, 11))
                    neighbours_cartesian[key].append([round(dis_x, 11), round(dis_y, 11)])
                    neighbours_coordinates[key].append(
                        [round(dis_x + key[0], 11), round(dis_y + key[1], 11)])

    return neighbours_radius, neighbours_cartesian, neighbours_coordinates
