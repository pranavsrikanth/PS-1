import time
import random

dim = 1024

datafile = open(f"C:\\Users\\advi\\Downloads\\{dim} dimention dataset for k means.txt", "r")

rawdata = datafile.read()

temp_data = list(rawdata.split("\n"))

data = [[] for i in range(len(temp_data))]
for i in range(len(temp_data)):
    data[i] = list(map(int, list(temp_data[i].split())))

start = time.time()

for rounds in range(50):

    n = len(data)

    centroids = [data[i] for i in random.sample(range(0, 1024), 16)]  # randomly assigning centroids

    Ck = list([] for i in range(16))
    prevCk = list()

    while prevCk != Ck:

        prevCk = Ck
        Ck = list([] for i in range(16))
        for i in range(n):  # running through all datapoints

            curr_dis = 10e10
            curr_ind = 0
            for j in range(16):  # running through each centroid to check which is closest to a given datapoint

                distance = sum(list(abs((data[i][k] - centroids[j][k])) for k in range(dim)))
                if distance < curr_dis:

                    curr_dis = distance
                    curr_ind = j
            Ck[curr_ind].append(data[i])

        for j in range(16):

            total = [0 for m in range(dim)]
            for m in range(dim):
                for k in range(len(Ck[j])):
                    total[m] += Ck[j][k][m]

            for k in range(dim):
                if len(Ck[j]) != 0:
                    centroids[j][k] = total[k] / len(Ck[j])

end = time.time()

print(f"total time = {(end - start) / 50}")