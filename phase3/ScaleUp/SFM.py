import numpy as np
from math import sqrt


def calc_TFL_dist(prev_container, curr_container, focal, pp):
    norm_prev_pts, norm_curr_pts, R, foe, tZ = prepare_3D_data(prev_container, curr_container, focal, pp)
    if abs(tZ) < 10e-6:
        print('tz = ', tZ)
    elif norm_prev_pts.size == 0:
        print('no prev points')
    elif norm_prev_pts.size == 0:
        print('no curr points')
    else:
        curr_container.corresponding_ind, curr_container.traffic_lights_3d_location, curr_container.valid = calc_3D_data(norm_prev_pts, norm_curr_pts, R, foe, tZ)
    return curr_container


def prepare_3D_data(prev_container, curr_container, focal, pp):
    norm_prev_pts = normalize(prev_container.traffic_light, focal, pp)
    norm_curr_pts = normalize(curr_container.traffic_light, focal, pp)
    R, foe, tZ = decompose(np.array(curr_container.EM))
    return norm_prev_pts, norm_curr_pts, R, foe, tZ


def calc_3D_data(norm_prev_pts, norm_curr_pts, R, foe, tZ):
    norm_rot_pts = rotate(norm_prev_pts, R)
    pts_3D = []
    corresponding_ind = []
    validVec = []
    for p_curr in norm_curr_pts:
        corresponding_p_ind, corresponding_p_rot = find_corresponding_points(p_curr, norm_rot_pts, foe)
        Z = calc_dist(p_curr, corresponding_p_rot, foe, tZ)
        valid = (Z > 0)
        if not valid:
            Z = 0
        validVec.append(valid)
        P = Z * np.array([p_curr[0], p_curr[1], 1])
        pts_3D.append((P[0], P[1], P[2]))
        corresponding_ind.append(corresponding_p_ind)
    return corresponding_ind, np.array(pts_3D), validVec


def normalize(pts, focal, pp):
    return np.array([((point[0] - pp[0]) / focal, (point[1] - pp[1]) / focal, 1) for point in pts])
    # transform pixels into normalized pixels using the focal length and principle point


def unnormalize(pts, focal, pp):
    return np.array([(point[0]*focal + pp[0], point[1]*focal + pp[1], focal) for point in pts])
    # transform normalized pixels into pixels using the focal length and principle point


def decompose(EM):
    R = EM[:3, :3]
    t = EM[:3, 3]
    foe = [t[0]/t[2], t[1]/t[2]]
    tZ = t[2]
    return R, foe, tZ
    # extract R, foe and tZ from the Ego Motion


def rotate(pts, R):
    return np.array([R @ point for point in pts])
    # rotate the points - pts using R


def distance(point, m, n):
    return abs((m * point[0] + n - point[1])/(sqrt(m**2+1)))


def find_corresponding_points(p, norm_pts_rot, foe):
    m = (foe[1] - p[1]) / (foe[0] - p[0])
    n = p[1] * foe[0] - (p[0] * foe[1]) / (foe[0] - p[0])
    curr_closest, corr_point, index = float('inf'), (0, 0, 0), -1

    for i, point in enumerate(norm_pts_rot):
        d = distance(point, m, n)
        if d < curr_closest:
            curr_closest, corr_point, index = d, point, 1

    return index, corr_point
    # compute the epipolar line between p and foe
    # run over all norm_pts_rot and find the one closest to the epipolar line
    # return the closest point and its index


def calc_dist(p_curr, p_rot, foe, tZ):
    x_move = abs(p_rot[0] - p_curr[0])
    y_move = abs(p_rot[1] - p_curr[1])

    x_d = (tZ * (foe[0] - p_rot[0])) / x_move
    y_d = (tZ * (foe[1] - p_rot[1])) / y_move
    # return (x_move * x_d + y_move * y_d) / (x_move + y_move)
    return np.average([x_d, y_d], weights=[abs(p_rot[0] - p_curr[0]), abs(p_rot[1] - p_curr[1])])

    # calculate the distance of p_curr using x_curr, x_rot, foe_x and tZ
    # calculate the distance of p_curr using y_curr, y_rot, foe_y and tZ
    # combine the two estimations and return estimated Z
