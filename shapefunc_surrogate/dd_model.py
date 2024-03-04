import numpy as np

from shapefunc_surrogate.preprocessing import *
from shapefunc_surrogate.postprocessing import *
import pickle as pk


def ann_predict(model, neigh_xy_dict, neigh_coor, h, s, dtype='laplace'):

    ref_nodes = []
    distances = []

    for key in neigh_xy_dict:
        ref_nodes.append(key)
        distances.append(neigh_xy_dict[key])

    distances_array = np.array(distances)
    distances_array = distances_array[:, 1:, :]

    stand_feature, f_mean, f_std = stdv_normalisation(distances_array)
    stand_feature = stand_feature.reshape(stand_feature.shape[0], -1)

    predicted_w = model.predict(stand_feature)
    scaled_w = rescale_output_stdv(predicted_w, f_std, dtype=dtype)

    scaled_w = np.insert(scaled_w, 0, 0, axis=1)
    scaled_w = scaled_w.T

    scaled_w_dict = {}
    loop = 0

    for ref_node_coor in ref_nodes:
        scaled_w_dict[ref_node_coor] = scaled_w[:, loop]
        loop = loop + 1

    return scaled_w_dict
