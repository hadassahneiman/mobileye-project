import numpy as np
import matplotlib.pyplot as plt

from phase3 import SFM
import phase4.plots as plots


def visualize(prev_container, curr_container, focal, pp, fig):
    norm_prev_pts, norm_curr_pts, R, norm_foe, tZ = SFM.prepare_3D_data(prev_container, curr_container, focal, pp)
    norm_rot_pts = SFM.rotate(norm_prev_pts, R)
    rot_pts = SFM.unnormalize(norm_rot_pts, focal, pp)
    foe = np.squeeze(SFM.unnormalize(np.array([norm_foe]), focal, pp))

    plots.mark_distances(curr_container.img, curr_container.traffic_light, fig, curr_container.traffic_lights_3d_location, foe, rot_pts)


class FrameContainer(object):
    def __init__(self, img_path=None):
        self.img = plt.imread(img_path[:-1]) if img_path else None
        self.traffic_light = []
        self.traffic_lights_3d_location = []
        self.EM = []
        self.corresponding_ind = []
        self.valid = []


def calc_distances(image_path, curr_candidates, prev_candidates, data_holder, fig):
    curr_container, prev_container = FrameContainer(image_path), FrameContainer()
    curr_container.traffic_light, prev_container.traffic_light = np.array(curr_candidates), np.array(prev_candidates)
    curr_container.EM = data_holder.EM
    curr_container = SFM.calc_TFL_dist(prev_container, curr_container, data_holder.focal, data_holder.principle_point)
    visualize(prev_container, curr_container, data_holder.focal, data_holder.principle_point, fig)
