import matplotlib.pyplot as plt
import numpy as np
import phase4.plots as plots


def predict(images, model):
    assert len(images)
    predictions = model.predict(images)
    return predictions


def find_edges(x, y, image):
    length, width = len(image), len(image[0])
    top, bottom = (0, 81) if (x < 40) else (length - 81, length) if (x > length - 41) else (x - 40, x + 41)
    left, right = (0, 81) if (y < 40) else (width - 81, width) if (y > width - 41) else (y - 40, y + 41)
    return top, bottom, left, right


def verify_tfl(img_path, candidates, auxiliary, fig, model):
    tfl, tfl_auxiliary = [], []
    image = plt.imread(img_path[:-1])
    crops = []

    for x, y in candidates:
        top, bottom, left, right = find_edges(x, y, image)
        crops.append(image[top:bottom, left:right])

    predictions = predict(np.array(crops), model)

    for i, p in enumerate(predictions):
        if p[0] > 0.99:
            tfl.append(candidates[i])
            tfl_auxiliary.append(auxiliary[i])

    green = tfl_auxiliary.index('green') if 'green' in tfl_auxiliary else len(tfl_auxiliary)
    plots.mark_tfls(image, np.array(tfl), fig, green, 'tfls')

    return {'candidates': tfl, 'auxiliary': tfl_auxiliary}
