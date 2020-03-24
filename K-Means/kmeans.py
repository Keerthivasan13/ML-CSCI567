import collections

import numpy as np


def getEuclideanDistance(point1, point2):
    return np.sum(np.float_power((point1 - point2), 2))


def get_k_means_plus_plus_center_indices(n, n_cluster, x, generator=np.random):
    '''

    :param n: number of samples in the data
    :param n_cluster: the number of cluster centers required
    :param x: data-  numpy array of points
    :param generator: random number generator from 0 to n for choosing the first cluster at random
            The default is np.random here but in grading, to calculate deterministic results,
            We will be using our own random number generator.


    :return: the center points array of length n_clusters with each entry being index to a sample
             which is chosen as centroid.
    '''
    # TODO:
    # implement the Kmeans++ algorithm of how to choose the centers according to the lecture and notebook
    # Choose 1st center randomly and use Euclidean distance to calculate other centers.
    centers = [generator.randint(n)]
    for index in range(1, n_cluster):
        # Computer Square Distance of each data point to nearest cluster center
        near_distance = np.zeros(n)
        for sample in range(n):  # 1 x D Data sample
            near_distance[sample] = min(getEuclideanDistance(x[sample], x[center]) for center in centers)
        # centers.append(np.argmax(np.divide(near_distance, np.sum(near_distance))))
        centers.append(np.argmax(near_distance))
    # DO NOT CHANGE CODE BELOW THIS LINE

    print("[+] returning center for [{}, {}] points: {}".format(n, len(x), centers))
    print(centers)
    return centers


def get_lloyd_k_means(n, n_cluster, x, generator):
    return generator.choice(n, size=n_cluster)


class KMeans():
    '''
        Class KMeans:
        Attr:
            n_cluster - Number of cluster for kmeans clustering (Int)
            max_iter - maximum updates for kmeans clustering (Int)
            e - error tolerance (Float)
            generator - random number generator from 0 to n for choosing the first cluster at random
            The default is np.random here but in grading, to calculate deterministic results,
            We will be using our own random number generator.
    '''

    def __init__(self, n_cluster, max_iter=100, e=0.0001, generator=np.random):
        self.n_cluster = n_cluster
        self.max_iter = max_iter
        self.e = e
        self.generator = generator

    def fit(self, x, centroid_func=get_lloyd_k_means):

        '''
            Finds n_cluster in the data x
            params:
                x - N X D numpy array
                centroid_func - To specify which algorithm we are using to compute the centers(Lloyd(regular) or Kmeans++)
            returns:
                A tuple
                (centroids a n_cluster X D numpy array, y a length (N,) numpy array where cell i is the ith sample's assigned cluster, number_of_updates a Int)
            Note: Number of iterations is the number of time you update the assignment
        '''
        assert len(x.shape) == 2, "fit function takes 2-D numpy arrays as input"

        N, D = x.shape

        self.centers = centroid_func(len(x), self.n_cluster, x, self.generator)

        # TODO:
        # - comment/remove the exception.
        # - Initialize means by picking self.n_cluster from N data points
        # - Update means and membership until convergence or until you have made self.max_iter updates.
        # - return (means, membership, number_of_updates)

        # DO NOT CHANGE CODE ABOVE THIS LINE
        # centroids = self.generator.choice(x, self.n_cluster, replace=True)
        # R = np.zeros((N, D))
        centroids = x[self.centers]
        prev_centroids = np.zeros(N)
        y = np.zeros(N, )
        # J = float('Inf')
        for t in range(self.max_iter):
            # Find Assignment y
            for sample in range(N):
                y[sample] = np.argmin(
                    [getEuclideanDistance(x[sample], centroids[cluster_idx]) for cluster_idx in range(self.n_cluster)])

            # Update Centers
            # R = np.eye(self.n_cluster)[y]
            # np.matmul(np.transpose(R), x)

            for cluster_idx in range(self.n_cluster):
                group = np.flatnonzero(y == cluster_idx)
                if len(group):
                    centroids[cluster_idx] = np.divide(np.sum(x[group], axis=0), len(group))

                print(centroids[cluster_idx])
                print("****")
                print(t)
            if np.array_equal(centroids, prev_centroids):
                break
            prev_centroids = centroids

        self.max_iter = t + 1
        # DO NOT CHANGE CODE BELOW THIS LINE
        return centroids, y, self.max_iter


class KMeansClassifier():
    '''
        Class KMeansClassifier:
        Attr:
            n_cluster - Number of cluster for kmeans clustering (Int)
            max_iter - maximum updates for kmeans clustering (Int)
            e - error tolerance (Float)
            generator - random number generator from 0 to n for choosing the first cluster at random
            The default is np.random here but in grading, to calculate deterministic results,
            We will be using our own random number generator.
    '''

    def __init__(self, n_cluster, max_iter=100, e=1e-6, generator=np.random):
        self.n_cluster = n_cluster
        self.max_iter = max_iter
        self.e = e
        self.generator = generator

    def fit(self, x, y, centroid_func=get_lloyd_k_means):
        '''
            Train the classifier
            params:
                x - N X D size  numpy array
                y - (N,) size numpy array of labels
                centroid_func - To specify which algorithm we are using to compute the centers(Lloyd(regular) or Kmeans++)

            returns:
                None
            Stores following attributes:
                self.centroids : centroids obtained by kmeans clustering (n_cluster X D numpy array)
                self.centroid_labels : labels of each centroid obtained by
                    majority voting (N,) numpy array)
        '''

        assert len(x.shape) == 2, "x should be a 2-D numpy array"
        assert len(y.shape) == 1, "y should be a 1-D numpy array"
        assert y.shape[0] == x.shape[0], "y and x should have same rows"

        self.generator.seed(42)
        N, D = x.shape
        # TODO:
        # - comment/remove the exception.
        # - Implement the classifier
        # - assign means to centroids
        # - assign labels to centroid_labels

        # DONOT CHANGE CODE ABOVE THIS LINE
        self.centers = centroid_func(len(x), self.n_cluster, x, self.generator)
        centroids = x[self.centers]
        prev_centroids = np.zeros(N)
        member = np.zeros(N, )
        for t in range(self.max_iter):
            for sample in range(N):
                member[sample] = np.argmin(
                    [getEuclideanDistance(x[sample], centroids[cluster_idx]) for cluster_idx in range(self.n_cluster)])

            # Update Centers
            for cluster_idx in range(self.n_cluster):
                group = np.flatnonzero(member == cluster_idx)
                if len(group):
                    centroids[cluster_idx] = np.divide(np.sum(x[group], axis=0), len(group))

            if np.array_equal(centroids, prev_centroids):
                break
            prev_centroids = centroids

        centroid_labels = np.zeros(self.n_cluster)
        for cluster_idx in range(self.n_cluster):
            centroid_labels[cluster_idx] = \
            collections.Counter(y[np.flatnonzero(member == cluster_idx)]).most_common()[0][0]

        # DONOT CHANGE CODE BELOW THIS LINE

        self.centroid_labels = centroid_labels
        self.centroids = centroids

        assert self.centroid_labels.shape == (
            self.n_cluster,), 'centroid_labels should be a numpy array of shape ({},)'.format(self.n_cluster)

        assert self.centroids.shape == (
            self.n_cluster, D), 'centroid should be a numpy array of shape {} X {}'.format(self.n_cluster, D)

    def predict(self, x):
        '''
            Predict function
            params:
                x - N X D size  numpy array
            returns:
                predicted labels - numpy array of size (N,)
        '''

        assert len(x.shape) == 2, "x should be a 2-D numpy array"

        self.generator.seed(42)
        N, D = x.shape
        # TODO:
        # - comment/remove the exception.
        # - Implement the prediction algorithm
        # - return labels

        # DONOT CHANGE CODE ABOVE THIS LINE
        labels = []
        for sample in range(N):
            labels[sample] = self.centroid_labels[np.argmin(
                [getEuclideanDistance(x[sample], self.centroids[cluster_idx]) for cluster_idx in
                 range(self.n_cluster)])]

        # DO NOT CHANGE CODE BELOW THIS LINE
        return np.array(labels)


def transform_image(image, code_vectors):
    '''
        Quantize image using the code_vectors

        Return new image from the image by replacing each RGB value in image with nearest code vectors (nearest in euclidean distance sense)

        returns:
            numpy array of shape image.shape
    '''

    assert image.shape[2] == 3 and len(image.shape) == 3, \
        'Image should be a 3-D array with size (?,?,3)'

    assert code_vectors.shape[1] == 3 and len(code_vectors.shape) == 2, \
        'code_vectors should be a 2-D array with size (?,3)'

    # TODO
    # - comment/remove the exception
    # - implement the function

    # DONOT CHANGE CODE ABOVE THIS LINE
    new_im = 1

    # DONOT CHANGE CODE BELOW THIS LINE
    return new_im

