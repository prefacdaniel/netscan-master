import os
import sys
import re
import time
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql import Row
# from pyspark.sql.functions import *

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pyspark.sql.functions as func
import matplotlib.patches as mpatches
from operator import add
from pyspark.mllib.clustering import KMeans, KMeansModel
from operator import add
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.mllib.util import MLUtils
from pyspark.mllib.regression import LabeledPoint
import itertools

MAX_ITERATIONS = 100


def euclidean_distance(p1, p2):
    return np.sqrt(np.sum([(c1 - c2) ** 2 for c1, c2 in zip(p1, p2)]))


def find_closest_centroid_index(datapoint, centroids):
    return min(enumerate(centroids), key=lambda x: euclidean_distance(datapoint, x[1]))[0]


def randomize_centroids(data, k):
    indices = np.arange(len(data))  # generate a list from 0 to len(data)-1
    np.random.shuffle(indices)  # shuffle the obtained list
    random_indices = indices[:k]  # extact only first k indices
    centroids = [data[i] for i in range(len(data)) if
                 i in random_indices]  # todo  check if works with for i in random_indices
    return centroids


def check_converge(centroids, old_centroids, num_iterations, threshold=0):
    if num_iterations > MAX_ITERATIONS:
        return True
    distances_between_new_and_old_centroids = np.array(
        [euclidean_distance(n, o) for n, o in zip(centroids, old_centroids)])
    if (distances_between_new_and_old_centroids <= threshold).all():
        return True
    return False


def update_centroids(centroids, clusters):
    assert (len(centroids) == len(clusters))
    clusters = np.array(clusters)
    for i, cluster in enumerate(clusters):
        centroids[i] = sum(cluster) / len(cluster)
    return centroids


def kmeans(data, k=2, centroids=None):
    data = np.array(data)
    if not centroids:
        centroids = randomize_centroids(data, k)

    old_centroids = centroids[:]

    iterations = 0

    while True:
        iterations += 1

        clusters = [[] for i in range(k)]

        for datapoint in data:
            centroid_index = find_closest_centroid_index(datapoint, centroids)
            clusters[centroid_index].append(datapoint)

        old_centroids = centroids[:]

        centroids = update_centroids(centroids, clusters)

        if check_converge(centroids, old_centroids, iterations):
            break

    return centroids

def parseLine(line):
    cols = line.split(",")
    label = cols[-1]
    feature_vector = cols[:-1]
    feature_vector = np.array(feature_vector, dtype=np.float)
    return (label, feature_vector)


def getVars(data):
    n = data.count()
    means = data.reduce(add) / n
    variances = data.map(lambda x: ( x  - means)**2).reduce(add) / n
    return variances

input_path = "/datasets/k-means/kddcup.data" #todo <- put your file
raw_data = sc.textFile(input_path, 12)

labelsAndData = raw_data.map(parseLine).cache()

# load data
iris = datasets.load_iris()
X_iris = iris.data
y_iris = iris.target
# do the clustering
centers = kmeans(X_iris, k=3)
labels = [find_closest_centroid_index(p, centers) for p in X_iris]

#plot the clusters in color
fig = plt.figure(1, figsize=(8, 8))
plt.clf()
ax = Axes3D(fig, rect=[0, 0, 1, 1], elev=8, azim=200)
plt.cla()
ax.scatter(X_iris[:, 3], X_iris[:, 0], X_iris[:, 2], c=labels)

# moon
# np.random.seed(0)
# X, y = datasets.make_moons(2000, noise=0.2)

# blob
# np.random.seed(0)
# X, y = datasets.make_blobs(n_samples=2000, centers=3, n_features=20, random_state=0)

# centers = kmeans(X, k=3)
# labels = [find_closest_centroid(p, centers) for p in X]

# fig = plt.figure(1, figsize=(8, 8))
# plt.clf()
# plt.scatter(X[:,0], X[:,1], s=40, c=labels, cmap=plt.cm.Spectral)

ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('Petal width')
ax.set_ylabel('Sepal length')
ax.set_zlabel('Petal length')

plt.show()

