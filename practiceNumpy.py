import numpy as np
from scipy import stats


def eliminate_outlier_column(data, column, m=2):  # smaller the m, the sensible became
    mean = np.mean(data, axis=0)
    sd = np.std(data, axis=0)
    print("mean is: ", mean)
    print("sd is: ", sd)
    return np.array([x for x in data if (abs(x[column] - mean[column]) < m * sd[column]).any()])


data = np.array([[600, 700, 4],
                 [500, 504, 5],
                 [600, 400, 6],
                 [1, 500, 5],
                 [500, 1, 3],
                 [600, 560, 4]])

print("Initial print:")
print(data)
# data = np.array([x for x in data if (abs(x - np.mean(data)) < 2 * np.std(data)).all()]) #for all

# mean = np.mean(data, axis=0)
# print("mean is: ", mean)
## print("sd is: ", sd)
# sd = np.std(data, axis=0)
# print("sd is: ", sd)
#
# data = np.array([x for x in data if (abs(x[0] - mean[0]) < 2 * sd[0]).all()]) #eliminare outlier pt o coloana
# data = np.array([x for x in data if (abs(x - mean) < 2 * sd).all()])#eliminare outlier pt tot arrayu

data = eliminate_outlier_column(data, 1)

print("After eliminating outlayers form col 0:")
print(data)

data = eliminate_outlier_column(data, 0)

print("After eliminating outlayers form col 1:")
print(data)
