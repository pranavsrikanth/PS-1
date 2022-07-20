import matplotlib.pyplot as plt
import pandas as pd
from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
from qiskit import Aer, execute
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def QuantumAlgo(x_p,y_p,centroids):
    # Calculating theta and phi values
    phi_list = [((x_p + 1) * np.pi / 2)]
    theta_list = [((y_p + 1) * np.pi / 2)]
    for x in range(len(centroids)):
        phi_list.append(((centroids[x][0] + 1) * np.pi / 2))
    for x in range(len(centroids)):
        theta_list.append(((centroids[x][1] + 1) * np.pi / 2))

    # Create a 2 qubit QuantumRegister - two for the vectors, and 
    # one for the ancillary qubit
    qreg = QuantumRegister(3, 'qreg')

    # Create a one bit ClassicalRegister to hold the result
    # of the measurements
    creg = ClassicalRegister(1, 'creg')

    qc = QuantumCircuit(qreg, creg, name='qc')

    # Get backend using the Aer provider
    backend = Aer.get_backend('qasm_simulator')

    # Create list to hold the results
    results_list = []
    # Estimating distances from the new point to the centroids
    for i in range(1, 20):
        # Apply a Hadamard to the ancillary
        qc.h(qreg[2])

        # Encode new point and centroid
        qc.u3(theta_list[0], phi_list[0], 0, qreg[0])           
        qc.u3(theta_list[i], phi_list[i], 0, qreg[1]) 

        # Perform controlled swap
        qc.cswap(qreg[2], qreg[0], qreg[1])
        # Apply second Hadamard to ancillary
        qc.h(qreg[2])

        # Measure ancillary
        qc.measure(qreg[2], creg[0])

        # Reset qubits
        qc.reset(qreg)

        # Register and execute job
        job = execute(qc, backend=backend, shots=1024)
        result = job.result().get_counts(qc)
        results_list.append(result['1'])
    print("here")
    return(results_list)

    # # Create a list to hold the possible classes
    # class_list = ['Green', 'Blue', 'Black']

    # # Find out which class the new data point belongs to 
    # # according to our distance estimation algorithm
    # quantum_p_class = class_list[results_list.index(min(results_list))]


    

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
datax = []*len(data)
datay = []*len(data)
for i in range(len(data)):
    datax.append(data[i][0])
    datay.append(data[i][1])
max_x = datax[0]; 
for i in range(0, len(datax)):    
    #Compare elements of array with max    
   if(datax[i] > max_x):    
       max_x = datax[i]
max_y = datay[0]
for i in range(0, len(datay)):    
    #Compare elements of array with max    
   if(datay[i] > max_y):    
       max_y = datay[i]       
while prevCk != Ck:
    
    prevCk = Ck
    Ck = list([] for i in range(20))
    
    def run_through_datapoints(data: list):
        curr_ind = 0
        dist = QuantumAlgo(data[0]/max_x,data[1]/max_y,centroids)
        print("here")
        curr_ind = dist.index(min(dist))
        Ck[curr_ind].append(data)
    with ThreadPoolExecutor(max_workers=500) as executor:
       executor.map(run_through_datapoints, data)
    
    # for i in range(n):  # running through all datapoints

    #     curr_ind = 0
    #     dist = QuantumAlgo(data[i][0]/max_x,data[i][1]/max_y,centroids)
    #     curr_ind = dist.index(min(dist))
    #     Ck[curr_ind].append(data[i])

    for j in range(20):

        xlis, ylis = 0, 0
        for k in range(len(Ck[j])):
            xlis += Ck[j][k][0]
            ylis += Ck[j][k][1]

        centroids[j][0] = xlis / len(Ck[j])
        centroids[j][1] = ylis / len(Ck[j])

print(centroids)