import math
import phat
import itertools
# from itertools import chain
# from itertools import combinations
# import time
import sys
import numpy as np
import matplotlib.pyplot as plt
import persim
from persim import images_weights
# import os
from multiprocessing import Pool
import os


def computeBottleneckMatrix(fun, d, nummod):

    print("Function {}, Hom. Degree {}: Start".format(fun, d))

    diagrams = []

    for i in range(1, nummod+1):
        diagram = np.loadtxt(
            "PDs/PD_{}_{}_H{}.txt".format(i, fun, d))

        if len(np.shape(diagram))==1:
            # np.reshape(diagram, (-1,2))
            diagram = np.expand_dims(diagram, axis=0)

        diagrams.append(diagram)

    distances=np.zeros((nummod,nummod))

    for i in range(nummod):
        for j in range(i):
            distances[i,j]=persim.bottleneck(diagrams[i], diagrams[j])

    print("Function {}, Hom. Degree {}: OK".format(fun, d))

    distances=distances+np.transpose(distances)

    ###### VISUALIZING BOTTLENECK DISTANCES ########

    matfig = plt.figure(figsize=(10,10))
    plt.matshow(distances, fignum=matfig.number)
    # plt.matshow(distances)
    # plt.show()

    plt.colorbar()
    plt.title("Bottleneck_Matrix_{}_H{}".format(fun,d))
    plt.savefig("distances/bottleneck_matrix_{}_H{}.png".format(fun,d))
    plt.clf()


    # ##### SAVING BOTTLENECK DISTANCES ########
    #
    # wfile = open("distances/bottleneck_Matrix_{}_H{}.txt".format(fun,d), "w")
    # np.savetxt(wfile, distances,fmt='%f')
    # wfile.close()

    return 0


def computeCombinedBottleneckMatrix(fun, nummod):

    print("Function {}: Start".format(fun))

    distances=np.zeros((nummod,nummod))

    for d in range(3):

        diagrams = []

        for i in range(1, nummod+1):
            diagram = np.loadtxt(
                "PDs/PD_{}_{}_H{}.txt".format(i, fun, d))

            if len(np.shape(diagram))==1:
                # np.reshape(diagram, (-1,2))
                diagram = np.expand_dims(diagram, axis=0)

            diagrams.append(diagram)

        for i in range(nummod):
            for j in range(i):
                distances[i,j]=distances[i,j]+persim.bottleneck(diagrams[i], diagrams[j])

    print("Function {}: OK".format(fun))

    distances=distances+np.transpose(distances)

    ###### VISUALIZING BOTTLENECK DISTANCES ########

    matfig = plt.figure(figsize=(10,10))
    plt.matshow(distances, fignum=matfig.number)
    # plt.matshow(distances)
    # plt.show()

    plt.colorbar()
    plt.title("Bottleneck_Matrix_{}".format(fun))
    plt.savefig("Distances/bottleneck_matrix_{}.png".format(fun))
    plt.clf()


    # ##### SAVING BOTTLENECK DISTANCES ########
    #
    # wfile = open("Distances/bottleneck_Matrix_{}.txt".format(fun), "w")
    # np.savetxt(wfile, distances,fmt='%f')
    # wfile.close()

    return 0


nummod = 80

for function in [1,2]:

    computeBottleneckMatrix(function, 0, nummod)
    computeBottleneckMatrix(function, 1, nummod)
    computeBottleneckMatrix(function, 2, nummod)
    computeCombinedBottleneckMatrix(function, nummod)
