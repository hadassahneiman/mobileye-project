import matplotlib.pyplot as plt

import part1
import part2
import part3


class TFLManager:
    def __init__(self):
        self.prev_result = None

    def run_on_frame(self, image_path, data_holder, model):
        fig, (light_src, tfl, distances) = plt.subplots(1, 3, figsize=(12, 6))
        res = dict()
        res['light_src'] = (self.find_light_src(image_path, light_src))

        params = {'image_path': image_path,
                  'candidates': res['light_src']['candidates'], 'auxiliary': res['light_src']['auxiliary']}
        res['tfls'] = (self.verify_tfl(params, tfl, model))

        assert len(res['light_src']['candidates']) >= len(res['tfls']['candidates'])

        if not self.prev_result:
            self.prev_result = res['tfls']['candidates']
            plt.show()
            return res

        params = {'image_path': image_path,
                  'data_holder': data_holder,
                  'curr_candidates': res['tfls']['candidates']}

        res['distances'] = (self.find_distances(params, distances))

        self.prev_result = res['tfls']['candidates']
        plt.show()
        return res

    @staticmethod
    def find_light_src(image_path, fig):
        return part1.find_light_src(image_path, fig)

    @staticmethod
    def verify_tfl(params, fig, model):
        image_path = params['image_path']
        candidates = params['candidates']
        auxiliary = params['auxiliary']
        return part2.verify_tfl(image_path, candidates, auxiliary, fig, model)

    def find_distances(self, params, fig):
        image_path = params['image_path']
        curr_candidates = params['curr_candidates']
        data_holder = params['data_holder']
        return part3.calc_distances(image_path, curr_candidates, self.prev_result, data_holder, fig)

