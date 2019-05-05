import csv
import matplotlib.pyplot as plt
import numpy
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from pandas import DataFrame
import kmean as km
import CSVReader as cr
import DataNormalisation as dt

MAX_ITERATIONS = 100

filePathRusia = 'C:\\Users\\dprefac\\PycharmProjects\\netscan-master\\csv\\pythonScript_1000_telekom_VPNRusia.csv'
filePathLocal = 'C:\\Users\\dprefac\\PycharmProjects\\netscan-master\\csv\\bruteForceWithValidPassword100Attempts200Status.csv'

features = [9, 10, 13, 14]

csvReader = cr.CSVReader()

dataFromRusia = csvReader.load_csv_and_extract_feature(filePathRusia, features, "RUSIA")
dataFromLocal = csvReader.load_csv_and_extract_feature(filePathLocal, features, "LOCAL")

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

#################### altready existent kmean algoritm #######################
df = DataFrame(k_data, columns=[0, 1, 2, 3])                                #
                                                                            #
kmeans = KMeans(n_clusters=2).fit(df)                                       #
centroids = kmeans.cluster_centers_                                         #
print(centroids)                                                            #
                                                                            #
plt.scatter(df[0], df[1], c=kmeans.labels_.astype(float), s=50, alpha=0.5)  #
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)                #
plt.show()                                                                  #
#############################################################################


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
