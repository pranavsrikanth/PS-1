import numpy as np
dataset = "a1"
data    = np.loadtxt(dataset+".data.gz", ndmin=2)
data = data.tolist()

n = len(data)

centroids = [data[100*i] for i in range(20)]  # randomly assigning centroids
# print(centroids)

var = 0
curr_var = 10e10
Ck = list([] for i in range(20))
prevCk = list()

# print(Ck)

while prevCk != Ck:

    prevCk = Ck
    Ck = list([] for i in range(20))
    for i in range(n):  # running through all datapoints

        curr_dis = 10e10
        curr_ind = 0
        for j in range(20):  # running through each centroid to check which is closest to a given datapoint

            distance = abs(data[i][0] - centroids[j][0]) + abs(data[i][1] - centroids[j][1])
            if distance < curr_dis:
                curr_dis = distance
                curr_ind = j
        Ck[curr_ind].append(data[i])

    for j in range(20):

        xlis, ylis = 0, 0
        for k in range(len(Ck[j])):
            xlis += Ck[j][k][0]
            ylis += Ck[j][k][1]

        centroids[j][0] = xlis / len(Ck[j])
        centroids[j][1] = ylis / len(Ck[j])

print(centroids)