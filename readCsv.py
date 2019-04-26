import csv
import matplotlib.pyplot as plt
import numpy
from scipy import stats
from mpl_toolkits.mplot3d import Axes3D

import numpy as np


def eliminate_outlier_column(data, column, m=2):  # smaller the m, the sensible became
    mean = np.mean(data, axis=0)
    sd = np.std(data, axis=0)
    return np.array([x for x in data if (abs(x[column] - mean[column]) < m * sd[column]).any()])


def load_csv_and_extract_feature(fileName, indexs, label):
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        data = []
        for row in csv_reader:
            if line_count != 0:
                data.append([float(row[i]) for i in indexs])
            line_count += 1
        return data


filePathRusia = 'C:\\Users\\dprefac\\PycharmProjects\\KMeans\\csv\\pythonScript_1000_telekom_VPNRusia.csv'
filePathLocal = 'C:\\Users\\dprefac\\PycharmProjects\\KMeans\\csv\\bruteForceWithValidPassword100Attempts200Status.csv'



features = [9, 10, 12, 13, 14]

dataFromRusia = load_csv_and_extract_feature(filePathRusia, features, "RUSIA")
dataFromLocal = load_csv_and_extract_feature(filePathLocal, features, "LOCAL")

dataFromRusia = np.array(dataFromRusia)
dataFromLocal = np.array(dataFromLocal)

dataFromRusia = eliminate_outlier_column(dataFromRusia, 0)
dataFromLocal = eliminate_outlier_column(dataFromLocal, 0)
#
dataFromRusia = eliminate_outlier_column(dataFromRusia, 1)
dataFromLocal = eliminate_outlier_column(dataFromLocal, 1)

print(dataFromRusia)


fig = plt.figure(1, figsize=(8, 8))
plt.clf()
ax = Axes3D(fig, rect=[0, 0, 1, 1], elev=8, azim=200)
plt.cla()
ax.scatter(dataFromLocal[:, 0], dataFromLocal[:, 1], dataFromLocal[:, 4], c="B")
ax.scatter(dataFromRusia[:, 0], dataFromRusia[:, 1], dataFromRusia[:, 4], c="R")
ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('Petal width')
ax.set_ylabel('Sepal length')
ax.set_zlabel('Petal length')
plt.show()
