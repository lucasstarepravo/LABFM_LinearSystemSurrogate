import numpy as np
from shapefunc_surrogate.preprocessing import *
from shapefunc_surrogate.postprocessing import *
import math
import torch
import pickle as pk
import time

def monomial_power(polynomial):
    """

    :param polynomial:
    :return:
    """
    monomial_exponent = [(total_polynomial - i, i)
                         for total_polynomial in range(1, polynomial + 1)
                         for i in range(total_polynomial + 1)]
    return np.array(monomial_exponent)


def calc_moments(neigh_xy_d, scaled_w, polynomial):
    mon_power = monomial_power(polynomial)
    monomial = []
    for power_x, power_y in mon_power:
        monomial.append((neigh_xy_d[:, :, 0] ** power_x * neigh_xy_d[:, :, 1] ** power_y) /
                        (math.factorial(power_x) * math.factorial(power_y)))
    moments = np.array(monomial) * scaled_w
    moments = np.sum(moments, axis=2)
    return moments.T


def moments_normalised(stand_feature, predicted_w):
    stand_feature1 = stand_feature.reshape(stand_feature.shape[0], -1, 2)
    moments = calc_moments(stand_feature1, predicted_w, polynomial=2)
    return moments


def ann_predict(model, m_matrix_dict, h, dtype='laplace'):
    total_laplace_time = 0
    ref_nodes = []
    m_matrices = []
    start_time = time.time()
    for key in m_matrix_dict:
        ref_nodes.append(key)
        m_matrices.append(m_matrix_dict[key])

    m_matrices = np.array(m_matrices)
    m_matrices = torch.tensor(m_matrices, dtype=torch.float32)
    m_matrices = m_matrices.reshape(m_matrices.shape[0], -1)

    # For higher orders of polynomials, the preprocessing of features will be in this line

    pred_psi = model.predict(m_matrices)
    scaled_psi = rescale_output(pred_psi, h, dtype=dtype)
    scaled_psi = scaled_psi.t()
    scaled_psi = scaled_psi.detach().numpy()

    scaled_psi_dict = {}
    loop = 0

    for ref_node_coor in ref_nodes:
        scaled_psi_dict[ref_node_coor] = scaled_psi[:, loop]
        loop = loop + 1

    end_time = time.time()
    total_laplace_time += (end_time - start_time)
    return scaled_psi_dict, total_laplace_time
