import numpy as np


def eliminate_outlier_with_z_score(data_1, m=2):
    data = []
    threshold = m
    mean_1 = np.mean(data_1, axis=0)
    std_1 = np.std(data_1, axis=0)
    for y in data_1:
        z_score = (y - mean_1) / std_1
        if not (np.abs(z_score) > threshold).any():
            data.append(y)
    return data


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
