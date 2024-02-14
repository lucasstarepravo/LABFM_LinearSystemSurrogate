from keras.models import load_model
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


def ann_predict(neigh_xy_d, neigh_coor, dx, dtype='laplace'):

    with open('/home/combustion/python/pythonProject/stand_info.pk', 'rb') as f:
        stand_info = pk.load(f) # This variable should contain the average of the trained weights, the standard dev
                                # that will be used to rescale the weights and the standard dev that will be used to
                                # rescale the input x and y distances

    #h_scale_xy = stand_info.h_scale_xy
    h_scale_w = stand_info.h_scale_w
    l_mean = stand_info.l_mean

    stand_feature, f_mean = non_dimension(neigh_xy_d, dx)
    stand_feature = stand_feature.reshape(-1, 1)


    weights =  1

    return weights