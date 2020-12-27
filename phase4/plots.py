def mark_tfls(img, candidates, fig, green, title):
    fig.set_title(title)
    fig.imshow(img)
    if green > 0:
        fig.plot(candidates[:green, [0]], candidates[:green, [1]], 'ro', color='r', markersize=4)

    if green != len(candidates):
        fig.plot(candidates[green:, [0]], candidates[green:, [1]], 'ro', color='g', markersize=4)


def mark_distances(img, candidates, fig, traffic_lights_3d_location, foe, rot_pts):
    fig.set_title('distances')
    fig.imshow(img)
    fig.plot(candidates[:, 0], candidates[:, 1], 'b+')

    for i in range(len(candidates)):
        fig.plot([candidates[i, 0], foe[0]], [candidates[i, 1], foe[1]], 'b', linewidth=0.2)
        # if curr_container.valid[i]:
        fig.text(candidates[i, 0], candidates[i, 1],
                      r'{0:.1f}'.format(traffic_lights_3d_location[i, 2]), color='r', fontsize=5)
    fig.plot(foe[0], foe[1], 'r+')
    fig.plot(rot_pts[:, 0], rot_pts[:, 1], 'g+')