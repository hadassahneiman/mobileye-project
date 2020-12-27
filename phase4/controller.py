import pickle
from tensorflow.python.keras.models import load_model
from phase4.data_holder import DataHolder
from phase4.tfl_man import TFLManager


class Controller:
    @staticmethod
    def run(pls_file, model_path):
        model = load_model(model_path)
        pkl_file, frames = Controller.load_pls_data(pls_file)
        focal, pp, EMs = Controller.load_pickle_data(pkl_file, frames)
        tfl_manager = TFLManager()
        data_holder = DataHolder(pp, focal)
        for i, frame in enumerate(frames[:-1]):
            data_holder.EM = EMs[i]
            yield tfl_manager.run_on_frame(frame, data_holder, model)

    @staticmethod
    def load_pls_data(path):
        with open(path, "r") as file:
            data = file.readlines()

        return data[0][:-1], data[1:]

    @staticmethod
    def load_pickle_data(pkl_file, frames):
        with open(pkl_file, 'rb') as pklfile:
            data = pickle.load(pklfile, encoding='latin1')
        focal = data['flx']
        pp = data['principle_point']
        id = int(frames[0][-23:-17])
        EMs = [data['egomotion_' + str(id + i) + '-' + str(id + i + 1)] for i in range(len(frames)-1)]
        return focal, pp, EMs














