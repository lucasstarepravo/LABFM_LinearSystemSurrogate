from Sim_Functions import calc_h
import numpy as np
import math


def create_nodes(total_nodes, s):
    """

    :param total_nodes: is a scalar that states the number of nodes we would like to have inside the domain
    :param s: is a scalar that determines the average distance between points inside the comp. stencil
    :return:
    coordinates: is a numpy array that contains all coordinates of nodes, the first and second column contain the x and
    y coordinates, respectively. It is possible to access the ith node with "coordinates[i]"
    """
    delta = 1.0 / (total_nodes - 1)  # Determine the spacing delta between the points in the original domain
    h = calc_h(s, total_nodes)
    n = int(2 * h / delta)  # Calculate the number of points to be added on each side
    x = np.linspace(0 - 2 * h, 1 + 2 * h, total_nodes + 2 * n)  # Creates x coordinates with boundary
    y = np.linspace(0 - 2 * h, 1 + 2 * h, total_nodes + 2 * n)  # Creates y coordinates with boundary
    for i in range(len(x)):  # This perturbs the initial position of the points
        x[i] = x[i] + np.random.choice([1, -1]) * np.random.uniform(0, s / 2)
        y[i] = y[i] + np.random.choice([1, -1]) * np.random.uniform(0, s / 2)
    coordinates = np.column_stack((x, y))
    return coordinates


def threshold(coordinates):  # check whether the node is inside or outside the domain
    """
    This function assumes that the domain is from 0 to 1 in the dimensions x and y. This function allows you to access
    the nodes which are inside the domain and which nodes will be used as boundary
    :param coordinates: list of lists containing the coordinates of all nodes
    :return: return a list stating whether a point is inside the domain or not (i.e., it is a reference node or not)
    """
    in_domain = []
    for x_i, y_i in coordinates:  # Looping for every node
        if x_i > 1 or x_i < 0 or y_i > 1 or y_i < 0:
            in_domain.append(False)
        else:
            in_domain.append(True)
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
    index = 0
    for x_i, y_i in coordinates:
        distance[index] = []
        if not in_domain[index]:
            distance[index] = None
            index = index + 1
        else:  # The resulting matrix when calculating x_i and x_j is symmetric, so there might be a way to improve comp. efficiency
            # the distance from the first to the second value is of equal magnitude but with opposite sign to the distance of the second to the first
            for x_j, y_j in coordinates:
                x_dist = (x_j - x_i)
                y_dist = (y_j - y_i)
                distance[index].append([x_dist, y_dist])
            index = index + 1
    return distance


def neighbour_nodes(distance, h):
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
    neighbours_radius = {}  # N_inside has the values
    neighbours_cartesian = {}
    index = 0
    for i in range(len(distance)):
        neighbours_radius[index] = []
        neighbours_cartesian[index] = []
        if not distance[i]:
            neighbours_radius[index] = None
            neighbours_cartesian[index] = None
            index = index + 1
        else:
            for dis_x, dis_y in distance[i]:
                r_distance = (dis_x ** 2 + dis_y ** 2) ** .5
                if r_distance <= 2 * h:
                    # I can add here a way to pop the items out of the distance list, the items that are out of bounds.
                    # This would make the neighbour dictionary in cartesian coordinates only to contain nodes that will
                    # be reference nodes
                    neighbours_radius[index].append(r_distance)
                    neighbours_cartesian[index].append([dis_x, dis_y])
            index = index + 1
    return neighbours_radius, neighbours_cartesian