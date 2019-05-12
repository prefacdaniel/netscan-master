import numpy as np
from scipy import stats


def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2 == 0] = 1
    return a / np.expand_dims(l2, axis)


def eliminate_outlier_column(data, column, m=2):  # smaller the m, the sensible became
    mean = np.mean(data, axis=0)
    sd = np.std(data, axis=0)
    print("mean is: ", mean)
    print("sd is: ", sd)
    return np.array([x for x in data if (abs(x[column] - mean[column]) < m * sd[column]).any()])


def eliminate_outlier(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]


def reject_outliers(data, m=2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / mdev if mdev else 0.
    return data[s < m]


def normalise_data_set(data_set):
    return np.array((data_set - data_set.mean(axis=0)) / data_set.std(axis=0))


def detect_outlier(data_1, m=2):
    outliers = []
    threshold = m
    mean_1 = np.mean(data_1, axis=0)
    std_1 = np.std(data_1, axis=0)

    for y in data_1:
        z_score = (y - mean_1) / std_1
        if (np.abs(z_score) > threshold).any():
            outliers.append(y)
    return outliers


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

#
# data = np.array([[600, 700, 4],
#                  [500, 504, 5],
#                  [600, 400, 6],
#                  [1, 500, 5],
#                  [500, 1, 3],
#                  [600, 560, 1]])
# print("Initial print:")
# # data = np.array([x for x in data if (abs(x - np.mean(data)) < 2 * np.std(data)).all()]) #for all
#
# # mean = np.mean(data, axis=0)
# # print("mean is: ", mean)
# ## print("sd is: ", sd)
# # sd = np.std(data, axis=0)
# # print("sd is: ", sd)
# #
# # data = np.array([x for x in data if (abs(x[0] - mean[0]) < 2 * sd[0]).all()]) #eliminare outlier pt o coloana
# # data = np.array([x for x in data if (abs(x - mean) < 2 * sd).all()])#eliminare outlier pt tot arrayu
#
# print(data)
#
# data = eliminate_outlier_column(data, 1)
# data = eliminate_outlier_column(data, 0)
# # data = normalized(data, 0)
# # print(data)
#
# print(data)
#
#
# normed = normalise_data_set(data)
# print(normed)
#
# print(normed.std(axis=0))
# print(normed.mean(axis=0))
