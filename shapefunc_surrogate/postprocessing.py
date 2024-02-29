import numpy as np
import math


def rescale_output(predicted_w, neigh_xy_d, h):

    c = 2.22204350233 # This was obtained from the pythonProject file when optimising c for avg_w = 1/(c*s)**2

    avg_dist = np.mean(abs(neigh_xy_d))
    avg_weight = 1/(c*avg_dist)**2
    predicted_w = predicted_w/h**2 + avg_weight
    return predicted_w
