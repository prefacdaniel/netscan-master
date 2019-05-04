import csv
import matplotlib.pyplot as plt
import numpy
import DataNormalisation as dt
import kmean as km
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

MAX_ITERATIONS = 100


####################################         ###############################################################
#################################### K-means ###############################################################
####################################         ###############################################################

#
# def update_centroids(centroids, clusters):
#     assert (len(centroids) == len(clusters))
#     clusters = np.array(clusters)
#     for i, cluster in enumerate(clusters):
#         centroids[i] = sum(cluster) / len(cluster)
#     return centroids
#
#
# def check_converge(centroids, old_centroids, num_iterations, threshold=0):
#     if num_iterations > MAX_ITERATIONS:
#         return True
#     distances_between_new_and_old_centroids = np.array(
#         [euclidean_distance(n, o) for n, o in zip(centroids, old_centroids)])
#     if (distances_between_new_and_old_centroids <= threshold).all():
#         return True
#     return False
#
#
# def randomize_centroids(data, k):
#     indices = np.arange(len(data))  # generate a list from 0 to len(data)-1
#     np.random.shuffle(indices)  # shuffle the obtained list
#     random_indices = indices[:k]  # extact only first k indices
#     centroids = [data[i] for i in range(len(data)) if
#                  i in random_indices]  # todo  check if works with for i in random_indices
#     return centroids
#
#
# def kmeans(data, k=2, centroids=None):
#     data = np.array(data)
#     if not centroids:
#         centroids = randomize_centroids(data, k)
#
#     old_centroids = centroids[:]
#
#     iterations = 0
#
#     while True:
#         iterations += 1
#
#         clusters = [[] for i in range(k)]
#
#         for datapoint in data:
#             centroid_index = find_closest_centroid_index(datapoint, centroids)
#             clusters[centroid_index].append(datapoint)
#
#         old_centroids = centroids[:]
#
#         centroids = update_centroids(centroids, clusters)
#
#         if check_converge(centroids, old_centroids, iterations):
#             break
#
#     return centroids
#
#
# def euclidean_distance(p1, p2):
#     return np.sqrt(np.sum([(c1 - c2) ** 2 for c1, c2 in zip(p1, p2)]))
#
#
# def find_closest_centroid_index(datapoint, centroids):
#     return min(enumerate(centroids), key=lambda x: euclidean_distance(datapoint, x[1]))[0]


####################################                    ####################################################
#################################### DATA NORMALISATION ####################################################
####################################                    ####################################################
# def normalise_training_data_set(data_set, data_set_mean, data_set_std):
#     return np.array((data_set - data_set_mean) / data_set_std)
#
#
# def normalise_data_set(data_set):
#     data_set_mean = data_set.mean(axis=0)
#     data_set_std = data_set.std(axis=0)
#     return np.array((data_set - data_set_mean) / data_set_std), data_set_mean, data_set_std
#
#
# def eliminate_outlier_column(data, column, m=3):  # smaller the m, the sensitives became
#     mean = np.mean(data, axis=0)
#     sd = np.std(data, axis=0)
#     return np.array([x for x in data if (abs(x[column] - mean[column]) < m * sd[column]).any()])


################################################               #############################################
################################################ READ CSV FILE #############################################
################################################               #############################################
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


############################################################################################################
############################################################################################################
filePathRusia = 'C:\\Users\\dprefac\\PycharmProjects\\netscan-master\\csv\\pythonScript_1000_telekom_VPNRusia.csv'
filePathLocal = 'C:\\Users\\dprefac\\PycharmProjects\\netscan-master\\csv\\bruteForceWithValidPassword100Attempts200Status.csv'

features = [9, 10, 13, 14]

dataFromRusia = load_csv_and_extract_feature(filePathRusia, features, "RUSIA")
dataFromLocal = load_csv_and_extract_feature(filePathLocal, features, "LOCAL")

dataFromRusia = np.array(dataFromRusia)
dataFromLocal = np.array(dataFromLocal)

dataFromRusia = dt.DataNormalisation.eliminate_outlier_column(dataFromRusia, 0)
dataFromLocal = dt.DataNormalisation.eliminate_outlier_column(dataFromLocal, 0)
#
dataFromRusia = dt.DataNormalisation.eliminate_outlier_column(dataFromRusia, 1)
dataFromLocal = dt.DataNormalisation.eliminate_outlier_column(dataFromLocal, 1)

kMeanRusia = np.copy(dataFromRusia)
kMeanLocal = np.copy(dataFromLocal)

print(dataFromLocal.mean(axis=0))
print(dataFromLocal.std(axis=0))
print("old local")
print(dataFromLocal)
dataFromLocal, mean, std = dt.DataNormalisation.normalise_data_set(dataFromLocal)
print("new local")
print(dataFromLocal)
print(dataFromLocal.mean(axis=0))
print(dataFromLocal.std(axis=0))

print("old rusia data")
print(dataFromRusia)
dataFromRusia = dt.DataNormalisation.normalise_training_data_set(dataFromRusia, mean, std)
print("new rusia data")
print(dataFromRusia)

# dataFromRusia.concatenate(dataFromLocal)
#
# fig = plt.figure(1, figsize=(8, 8))
# plt.clf()
# ax = Axes3D(fig, rect=[0, 0, 1, 1], elev=8, azim=200)
# plt.cla()
# ax.scatter(dataFromLocal[:, 0], dataFromLocal[:, 1], dataFromLocal[:, 3], c="B")
# ax.scatter(dataFromRusia[:, 0], dataFromRusia[:, 1], dataFromRusia[:, 3], c="R")
# ax.w_xaxis.set_ticklabels([])
# ax.w_yaxis.set_ticklabels([])
# ax.w_zaxis.set_ticklabels([])
# ax.set_xlabel('Petal width')
# ax.set_ylabel('Sepal length')
# ax.set_zlabel('Petal length')
# plt.show()


####################################         ###############################################################
#################################### K-means ###############################################################
####################################         ###############################################################


print("k-mean")
print("k-local")
print(kMeanLocal)
print("k-rusia")
print(kMeanRusia)
k_data = numpy.concatenate([kMeanRusia, kMeanLocal])
k_data, mean, std = dt.DataNormalisation.normalise_data_set(k_data)
print("k-data")
print(k_data)

kmean = km.Kmean()

centers = kmean.kmeans(k_data, k=2)
labels = kmean.get_labels(k_data, centers)

# centers = kmeans(k_data, k=2)
# labels = [find_closest_centroid_index(p, centers) for p in k_data]
fig = plt.figure(1, figsize=(8, 8))
plt.clf()
ax = Axes3D(fig, rect=[0, 0, 1, 1], elev=8, azim=200)
plt.cla()
ax.scatter(k_data[:, 3], k_data[:, 0], k_data[:, 2], c=labels)
ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('Petal width')
ax.set_ylabel('Sepal length')
ax.set_zlabel('Petal length')

plt.show()
