import math
import phat
import itertools
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import persim
from persim import images_weights


def F(s, vF):
    return vF[s].astype(np.float64).max()


def Comb(L):
    LL = []
    for i in range(len(L)):
        LLL = []
        for j in range(len(L)):
            if i != j:
                LLL.append(L[j])
        LLL.sort()
        LL.append(LLL)
        # print L
        # print LL
    return LL


def Bound(el, S):
    Indexes = []
    for s in Comb(el):
        if s:
            Indexes.append(S[tuple(s)])
    return sorted(Indexes)


def LoadSurface(modname):

    INfile = open("data/{}.off".format(modname), "r")

    for line in itertools.islice(INfile, 0, 2):  # start=17, stop=None
        # print(line)
        pass


    line = INfile.readline()
    nv, nt = int(line.split()[0]), int(line.split()[1])

    vertices = []
    edges = []
    triangles = []

    # CARICO I VERTICI
    for i in range(nv):
        vertices.append([i])

    # CARICO I TRIANGOLI E GLI EDGE
    E = set()
    for line in itertools.islice(INfile, nv, None):
        # print(line)
        a = int(line.split()[1])
        b = int(line.split()[2])
        c = int(line.split()[3])

        triangles.append([a, b, c])

        edges = [[a, b], [a, c], [b, c]]
        for edge in edges:
            edge.sort()
            E.add(tuple(edge))

    # Eliminato gli edge doppi al giro sopra. Qui possiamo limitarci a creare la lista
    edges = list(list(s) for s in E)

    print("\nLoaded Model {}".format(modname))
    print("# Vertices:{}".format(len(vertices)))
    print("# Edges:{}".format(len(edges)))
    print("# Triangles:{}".format(len(triangles)))

    INfile.close()

    return vertices, edges, triangles


def ComputePD(D, vF, max_vF):

    D.sort(key=lambda x: (F(x, vF), len(x)))

    # AVREBBE PIU' SENSO USARE CechMate????

    # Qui uso in supporto una map per cercare velocemente l'indice di ogni simplesso
    # cosi facendo non devo spendere n per guardarli tutti
    t_map = {}
    count = 0
    for i in D:
        i.sort()
        t_map[tuple(i)] = count
        count += 1

    #### CONSTRUCTION OF THE BOUNDARY MATRIX:

    C = [() for x in range(len(D))]
    for i in range(0, len(D)):
        C[i] = (len(D[i])-1, Bound(D[i], t_map))

    boundary_matrix = phat.boundary_matrix(
        representation=phat.representations.vector_vector)

    boundary_matrix.columns = C

    # print("Created Boundary Matrix")

    #### PAIRS COMPUTATION:

    pairs = boundary_matrix.compute_persistence_pairs()

    #### REMOVAL OF THE "NULL" PERSISTENCE PAIRS & RETRIEVAL OF THE INFINITE PAIRS:

    # print("Removing Null-Persistence Pairs")

    sF = np.zeros(len(D))
    leng = np.zeros(len(D))
    for i in range(len(D)):
        sF[i] = F(D[i], vF)
        leng[i] = len(D[i])

    # Convert pairs to np.array
    pairs = np.array(pairs)
    # print(pairs.shape)
    pairs_flatten = pairs.flatten()

    # Initialize the Indices corresponding to all the simplexes
    indices = np.arange(len(D))

    # Assign a negative value the pairs found
    indices[pairs_flatten] = -1

    # Filter out the indices corresponding to a pair
    indices_filt = indices[indices > -1]

    birth_minus_death = sF[pairs[:, 0]] - sF[pairs[:, 1]]

    nontrivial_bd = birth_minus_death[birth_minus_death < 0]
    # print('nontrivial_bd = {}'.format(nontrivial_bd))
    # vanno a finito:
    num_finite_pairs = nontrivial_bd.shape[0]
    # print('num_finite_pairs = {}'.format(num_finite_pairs))
    # vanno a infinito
    num_infinite_pairs = indices_filt.shape[0]

    # real_pairs track the pairs with non-trivial life (death - birth > 0)

    rescaledPairs = np.zeros(shape=(num_finite_pairs + num_infinite_pairs, 2))
    degree = np.zeros(num_finite_pairs + num_infinite_pairs)

    rescaledPairs[:num_finite_pairs, 0] = sF[pairs[birth_minus_death < 0, 0]]
    rescaledPairs[:num_finite_pairs, 1] = sF[pairs[birth_minus_death < 0, 1]]
    degree[:num_finite_pairs] = leng[pairs[birth_minus_death < 0, 0]]-1

    rescaledPairs[num_finite_pairs:, 0] = sF[indices_filt]
    rescaledPairs[num_finite_pairs:, 1] = np.inf
    # rescaledPairs[num_finite_pairs:, 1] = max_vF + 1
    degree[num_finite_pairs:] = leng[indices_filt] - 1

    dZero = rescaledPairs[degree < 0.5, :]
    dOne = rescaledPairs[degree == 1, :]
    dTwo = rescaledPairs[degree == 2, :]

    justFinitePairs = rescaledPairs[:num_finite_pairs, :]
    justDegreeFinitePairs = degree[:num_finite_pairs]

    dZeroNoInf = justFinitePairs[justDegreeFinitePairs < 0.5, :]
    dOneNoInf = justFinitePairs[justDegreeFinitePairs == 1, :]
    dTwoNoInf = justFinitePairs[justDegreeFinitePairs == 2, :]
    #
    # # print(dZero.shape[0])
    # # print(dOne.shape[0])
    # # print(dZeroNoInf.shape[0])
    # # print(dOne.shape[0])
    # # print(dTwo)

    return [dZeroNoInf, dOneNoInf, dTwoNoInf]


def savePD(diagram, filename, fun):

    wfile = open(
        "PDs/PD_{}_{}_H0_NoInf.txt".format(filename, fun), "w")
    np.savetxt(wfile, diagram[0], fmt='%f')
    if len(diagram[0])<1:
        wfile.write("{} {}".format(filename, filename))
    wfile.close()
    # np.save("PDs_{}/PD_{}_{}_F{}_H0".format(t,t,filename, i), diagrams[i][0])
    wfile = open(
        "PDs/PD_{}_{}_H1_NoInf.txt".format(filename, fun), "w")
    np.savetxt(wfile, diagram[1], fmt='%f')
    if len(diagram[1])<1:
        wfile.write("{} {}".format(filename, filename))
    wfile.close()
    # np.save("PDs_{}/PD_{}_{}_F{}_H1".format(t,t,filename, i), diagrams[i][1])
    wfile = open(
        "PDs/PD_{}_{}_H2_NoInf.txt".format(filename, fun), "w")
    np.savetxt(wfile, diagram[2], fmt='%f')
    if len(diagram[2])<1:
        wfile.write("{} {}".format(filename, filename))
    wfile.close()
    # np.save("PDs_{}/PD_{}_{}_F{}_H2".format(t,t,filename, i), diagrams[i][2])

    # print("Saved PDs of Molecule {} w.r.t. Function {}".format(filename,fun))

    return 0


def visualizePD(diagram, filename, fun):

    persim.plot_diagrams(diagram, title="PD of Model {} w.r.t. Function {}".format(filename, fun))
    plt.savefig("images/Diagram_{}_{}_NoInf.png".format(filename, fun))
    plt.clf()

    return 0


################### MAIN ##############

extremal_values=np.loadtxt("MinimiMassimiFunzioni.txt")

for modname in range(1,81):

    vertices, edges, triangles = LoadSurface(modname)

    D = vertices+edges+triangles

    for funname in [1,2]:

        print(funname)

        FUNfile = open("functions/{}-{}.usr".format(modname,funname), 'r')
        function = np.loadtxt(FUNfile)
        FUNfile.close()

        pd = ComputePD(D, function, extremal_values[1][funname-1])

        visualizePD(pd, modname, funname)

        savePD(pd, modname, funname)
