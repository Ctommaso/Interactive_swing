import numpy as np


def shortest_distance(X,Y,x,y):
	
	euclidean_distance = (X-x)**2+(Y-y)**2
	idx = np.nanargmin(euclidean_distance)
	min_dist = euclidean_distance[idx]
	return idx, min_dist
