import numpy as np


def non_dimension(features, dx):
    dx = 1.5 * dx # The scaling factor for s needs to be consistent for the value used in fortran

    f_mean = np.mean(features, axis=0, keepdims=True)
    stand_feature = (features - f_mean) / dx

    return stand_feature, f_mean
