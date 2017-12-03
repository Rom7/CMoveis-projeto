import numpy
import pandas
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import mean_squared_error
from geopy.distance import vincenty
from math import ceil, sqrt
import SwarmPackagePy

dataframe = pandas.read_csv("total.csv", delim_whitespace=False)
trainingmatrix = dataframe.values
numpy.random.shuffle(trainingmatrix)
dataframe = pandas.read_csv("testLoc2.csv", delim_whitespace=False)
testmatrix = dataframe.values
dataframe = pandas.read_csv("erbs2.csv", delim_whitespace=False, header=None)
erbs = dataframe.values 

dim = 6
big_alfa = 3
small_alfa = 0.5
k = 7

min_lat = -8.080
max_lat = -8.065
min_long = -34.91
max_long = -34.887

def regENN(k, test_set, alfa):
	m = test_set.shape[0]
	contador = 0
	for i in range(0,m):
		mask = numpy.ones(test_set.shape[0], dtype=bool)
		mask[i-contador] = False
		temp = test_set[mask,...]
		nbrs = NearestNeighbors(n_neighbors=k, algorithm='kd_tree', leaf_size=60).fit(temp[:,2:8])
		distances, indices = nbrs.kneighbors(test_set[i-contador,2:8].reshape(1,6))
		y, neighbors = kNN_estimator2(indices, distances, temp[:,0:2])
		stds = numpy.std(neighbors, axis=0)
		y = abs(test_set[i-contador,0:2] - y)
		if y[0] > alfa*stds[0] or y[1] > alfa*stds[1]:
			test_set = temp
			contador = contador + 1
	return test_set

def regCNN(k, test_set, alfa):
	m = test_set.shape[0]
	P = test_set[0:k,:]
	for i in range(k,m):
		temp = test_set[i,:]
		nbrs = NearestNeighbors(n_neighbors=k, algorithm='kd_tree', leaf_size=60).fit(P[:,2:8])
		distances, indices = nbrs.kneighbors(temp[2:8].reshape(1,6))
		y, neighbors = kNN_estimator2(indices, distances, P[:,0:2])
		stds = numpy.std(neighbors, axis=0)
		y = abs(temp[0:2] - y)
		if y[0] > alfa*stds[0] or y[1] > alfa*stds[1]:
			P = numpy.append(P, temp.reshape(1,8), axis=0)
	return P

def get_neighbors(indices, pos_set):
	neighbors = numpy.zeros((indices.shape[1], 2))
	for i in range(0, neighbors.shape[0]):
		neighbors[i,:] = pos_set[indices[0,i],:]
	return neighbors

def kNN_estimator2(indices, dist_neighbors, pos_set):	
	s = numpy.sum(dist_neighbors[0,:])
	est = numpy.zeros(2)
	neighbors = get_neighbors(indices, pos_set)
	for i in range(0, neighbors.shape[0]):
		est = est + dist_neighbors[0,i]*neighbors[i,:]
	return est/s, neighbors

def kNN_estimator(indices, dist_neighbors, pos_set, erbs):
	s = numpy.sum(dist_neighbors[0,:])
	est = numpy.zeros(dim)
	neighbors = get_neighbors(indices, pos_set)
	d = distance_to_erbs(neighbors, erbs)
	for i in range(0, dim):
		for j in range(0, neighbors.shape[0]):
			est[i] = est[i] + dist_neighbors[0,j]*d[j,i]
		est[i] /= s
	return est

def distance_to_erbs(points, erbs):
	tup = erbs.shape
	limitj = tup[0]
	tup2 = points.shape
	limiti = tup2[0]
	d = numpy.zeros((tup2[0], tup[0]))
	for i in range(0,limiti):
		for j in range(0,limitj):
			d[i, j] = vincenty((points[i,0], points[i,1]), (erbs[j,0], erbs[j,1])).meters
	return d
	
def distance_to_reference(training_result, reference):
	tup = reference.shape
	d = numpy.zeros(tup[0])
	for i in range(0, tup[0]):
		d[i] = vincenty((training_result[i, 0], training_result[i, 1]), (reference[i, 0], reference[i, 1])).meters
	return d

def fitness(point):
	new_dists = distance_to_erbs(point.reshape(1,2), erbs)
	vector = numpy.zeros(6)
	for i in range(0,dim):
		vector[i] = inter_step[i] - new_dists[0,i]
	return numpy.dot(vector,vector)

k_measures = numpy.zeros(4)
trainingmatrix = regENN(k, trainingmatrix, big_alfa)
trainingmatrix = regCNN(k, trainingmatrix, small_alfa)

X_train = trainingmatrix[:,2:8]
Y_train = trainingmatrix[:,0:2]
Yd_train = distance_to_erbs(Y_train, erbs)
X_test = testmatrix[:,2:8]
Y_test = testmatrix[:,0:2]
Yd_test = distance_to_erbs(Y_test, erbs)

tup = X_test.shape
inter_step = numpy.zeros(X_test.shape[1])
results = numpy.zeros(Y_test.shape)
nbrs = NearestNeighbors(n_neighbors=k, algorithm='kd_tree', leaf_size=60).fit(X_train)

for i in range(0, tup[0]):
    distances, indices = nbrs.kneighbors(X_test[i,:].reshape(1,6))
    inter_step = kNN_estimator(indices, distances, Y_train, erbs)
    # print(inter_step)
    # results[i,:] = SwarmPackagePy.aba(200, fitness, [min_lat, min_long], [max_lat, max_long], 2, 50).get_Gbest()
    results[i,:] = SwarmPackagePy.pso(100, fitness, [min_lat, min_long], [max_lat, max_long], 2, 50, 0.1, 1, 1).get_Gbest()

err = distance_to_reference(Y_test, results)
# for i in range(0, err.size):
    # err[i] = vincenty((Y_test[i,0], Y_test[i,1]), (results[i,0], results[i,1])).meters

k_measures = [sqrt((err**2).mean()), err.std(), err.max(), err.min()]

print(err)
print(k_measures)
f = open('fichier-test.csv', 'w+')
f.write("lat,lon\n")
for i in range(0,results.shape[0]):
	f.write("%.6f, %.6f\n" % (results[i,0], results[i,1]))
# print(results)
# d = distance_to_reference(results, Y_test)
# print(sqrt((d**2).mean()), d.std(), d.max(), d.min())
# print(d)
