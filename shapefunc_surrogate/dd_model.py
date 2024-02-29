from shapefunc_surrogate.preprocessing import *
from shapefunc_surrogate.postprocessing import *
import pickle as pk



class Standardisation:
    def __init__(self, l_mean = None, h_scale_xy = None, h_scale_w = None):
        self.l_mean = l_mean
        self.h_scale_xy = h_scale_xy
        self.h_scale_w = h_scale_w

    def set_l_mean(self, l_mean):
        self.l_mean = l_mean

    def set_h_scale_xy(self, h_scale_xy):
        self.h_scale_xy = h_scale_xy

    def set_h_scale_w(self, h_scale_w):
        self.h_scale_w = h_scale_w


def ann_predict(model, neigh_xy_d, neigh_coor, h, s, dtype='laplace'):

    neigh_xy_d = neigh_xy_d[1:, :]
    stand_feature, f_mean = non_dimension(neigh_xy_d, h)
    stand_feature = np.reshape(stand_feature, (1, -1))
    predicted_w = model.predict(stand_feature)
    scaled_w = rescale_output(predicted_w, neigh_xy_d, h)
    scaled_w = np.insert(scaled_w, 0, 0, axis=1)
    return scaled_w
