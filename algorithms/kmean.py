import numpy as np

MAX_ITERATIONS = 100


class Kmean:
    def __init__(self):
        pass

    def euclidean_distance(self, p1, p2):
        return np.sqrt(np.sum([(c1 - c2) ** 2 for c1, c2 in zip(p1, p2)]))

    def update_centroids(self, centroids, clusters):
        assert (len(centroids) == len(clusters))
        clusters = np.array(clusters)
        for i, cluster in enumerate(clusters):
            centroids[i] = sum(cluster) / len(cluster)
        return centroids

    def check_converge(self, centroids, old_centroids, num_iterations, threshold=0):
        if num_iterations > MAX_ITERATIONS:
            return True
        distances_between_new_and_old_centroids = np.array(
            [self.euclidean_distance(n, o) for n, o in zip(centroids, old_centroids)])
        if (distances_between_new_and_old_centroids <= threshold).all():
            return True
        return False

    def randomize_centroids(self, data, k):
        indices = np.arange(len(data))  # generate a list from 0 to len(data)-1
        np.random.shuffle(indices)  # shuffle the obtained list
        random_indices = indices[:k]  # extact only first k indices
        centroids = [data[i] for i in range(len(data)) if
                     i in random_indices]  # todo  check if works with for i in random_indices
        return centroids

    def kmeans(self, data, k=2, centroids=None):
        data = np.array(data)
        if not centroids:
            centroids = self.randomize_centroids(data, k)

        old_centroids = centroids[:]

        iterations = 0

        while True:
            iterations += 1

            clusters = [[] for i in range(k)]

            for datapoint in data:
                centroid_index = self.find_closest_centroid_index(datapoint, centroids)
                clusters[centroid_index].append(datapoint)

            old_centroids = centroids[:]

            centroids = self.update_centroids(centroids, clusters)

            if self.check_converge(centroids, old_centroids, iterations):
                break

        return centroids

    def find_closest_centroid_index(self, datapoint, centroids):
        return min(enumerate(centroids), key=lambda x: self.euclidean_distance(datapoint, x[1]))[0]

    def get_labels(self, k_data, centers):
        return [self.find_closest_centroid_index(p, centers) for p in k_data]
