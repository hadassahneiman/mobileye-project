import numpy as np
from scipy import signal as sg
from scipy.ndimage.filters import maximum_filter
from PIL import Image

import phase4.plots as plots


def high_pass_filter(img):
    highpass_filter = np.array([[-1 / 9, -1 / 9, -1 / 9],
                                [-1 / 9, 8 / 9, -1 / 9],
                                [-1 / 9, -1 / 9, -1 / 9]])

    return sg.convolve2d(img.T, highpass_filter, boundary='symm', mode='same')


def filter_by_color(img, color):
    return high_pass_filter(img[:, :, color])


def find_tfl_lights(c_image: np.ndarray):
    highpass_red_filter = filter_by_color(c_image, 0)
    max_red_filter = maximum_filter(highpass_red_filter, 20)
    red_candidates = [(i, j) for i in range(0, len(max_red_filter)) for j in range(0, len(max_red_filter[0])) if max_red_filter[i][j] == highpass_red_filter[i][j] and max_red_filter[i][j] > 30]
    x_red, y_red = [red_candidate[0] for red_candidate in red_candidates], [red_candidate[1] for red_candidate in red_candidates]

    highpass_green_filter = filter_by_color(c_image, 1)
    max_green_filter = maximum_filter(highpass_green_filter, 20)
    green_candidates = [(i, j) for i in range(0, len(max_green_filter)) for j in range(0, len(max_green_filter[0])) if max_green_filter[i][j] == highpass_green_filter[i][j] and max_green_filter[i][j] > 30]
    x_green, y_green = [green_candidate[0] for green_candidate in green_candidates], [green_candidate[1] for green_candidate in green_candidates]

    return x_red, y_red, x_green, y_green


def find_light_src(image_path, fig):
    image = np.array(Image.open(image_path[:-1]))
    red_x, red_y, green_x, green_y = find_tfl_lights(image)
    candidates = [(x, y) for x, y in zip(red_x, red_y)]
    candidates += [(x, y) for x, y in zip(green_x, green_y)]
    auxiliary = ['red'] * len(red_x) + ['green'] * len(green_x)
    plots.mark_tfls(image, np.array(candidates), fig, len(red_x), 'light_src')
    return {'candidates': candidates, 'auxiliary': auxiliary}

