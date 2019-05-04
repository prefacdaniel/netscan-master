import numpy as np


class DataNormalisation:
    def __init__(self):
        pass

    def normalise_training_data_set(data_set, data_set_mean, data_set_std):
        return np.array((data_set - data_set_mean) / data_set_std)

    def normalise_data_set(data_set):
        data_set_mean = data_set.mean(axis=0)
        data_set_std = data_set.std(axis=0)
        return np.array((data_set - data_set_mean) / data_set_std), data_set_mean, data_set_std

    def eliminate_outlier_column(data, column, m=3):  # smaller the m, the sensitives became
        mean = np.mean(data, axis=0)
        sd = np.std(data, axis=0)
        return np.array([x for x in data if (abs(x[column] - mean[column]) < m * sd[column]).any()])
