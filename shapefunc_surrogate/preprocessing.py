import numpy as np


def non_dimension(features, h):
    f_mean = np.mean(features, axis=0, keepdims=True)
    stand_feature = (features - f_mean) / h

    return stand_feature, f_mean
