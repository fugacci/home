import math
import phat
from itertools import chain
from itertools import combinations
import time
import sys
import numpy as np
import matplotlib.pyplot as plt

class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init

def distance(p, q):
    return math.sqrt((p.x-q.x)**2+(p.y-q.y)**2)

def F(s):
    return max( distance(p,q) for p in s for q in s  )

def Comb(iterable,m,n):
    return list(chain.from_iterable(combinations(iterable, r) for r in range(m,n+1)))

def Bound(i,S):
    Indexes=[]
    for s in Comb(S[i],len(S[i])-1,len(S[i])-1):
        if s:
            Indexes.append( S.index(s) )
    return sorted(Indexes)


#### STARTING POINTS:

V=[Point(0,0),Point(0,1),Point(1,0),Point(2,3),Point(3,2),Point(3,3),Point(3,0),Point(0,3)]


#### CONSTRUCTION OF THE SIMPLICES UP TO DIMENSION 2:

S=Comb(V,1,3)

S.sort(  key=lambda x: (  F(x), len(x)  )  )

# print("Number of simplices: %d" % len(S))

# TO=[]
# for i in range(len(S)):
#     TO.append(F(S[i]))
# print(TO)


#### CONSTRUCTION OF THE BOUNDARY MATRIX:

C=[ () for x in range(len(S))]
m=0
for i in range(0,len(S)):
    C[i]=(  len(S[i])-1, Bound(i,S)  )

# print(C)

boundary_matrix = phat.boundary_matrix(representation = phat.representations.vector_vector)

boundary_matrix.columns = C


#### PAIRS COMPUTATION:

pairs = boundary_matrix.compute_persistence_pairs()
# pairs = boundary_matrix.compute_persistence_pairs(reduction=phat.reductions.chunk_reduction)
# pairs = boundary_matrix.compute_persistence_pairs(reduction=phat.reductions.standard_reduction)
# pairs = boundary_matrix.compute_persistence_pairs(reduction=phat.reductions.row_reduction)
# pairs = boundary_matrix.compute_persistence_pairs(reduction=phat.reductions.spectral_sequence_reduction)


#### REMOVAL OF THE "NULL" PERSISTENCE PAIRS & RETRIEVAL OF THE INFINITE PAIRS:

Indices=list(range(len(S)))
realPairs=[]
for pair in pairs:
    Indices.remove(pair[0])
    Indices.remove(pair[1])
    birth=F(S[pair[0]])
    death=F(S[pair[1]])
    if birth!=death:
        life=death-birth
        degree=len(S[pair[1]])-2
        realPairs.append([life,birth,death,degree])

Inf=max(F(x) for x in S)+1

for i in Indices:
        realPairs.append(   [  Inf, F(S[i]), Inf, len(S[i])-1]  )

realPairs.sort(  key=lambda x: (  x[3], x[1]  )  )

# Here, I am considering only the pairs of homological degree at most 1. Since I am considering the 2-simplices at most, the homological information of degree 2 is not complete.
RealPairs=list(filter( lambda x: x[3]<2, realPairs))


#### PRINT OF THE PAIRS

print("\nThere are %d non-null persistence pairs: " % len(RealPairs))
for pair in RealPairs:
    print("Lifespan: %s, Birth: %s, Death: %s; Homological Degree: %d" %(pair[0],pair[1],pair[2],pair[3]) )


#### VISUALIZATION OF PERSISTENCE DIAGRAM:

x = np.array(list(pair[1] for pair in RealPairs ))
y = np.array(list(pair[2] for pair in RealPairs ))
colors = np.array(list(pair[3] for pair in RealPairs ))

plt.scatter(x, y, c=colors, alpha=0.5)

plt.axis([-0.1, Inf+0.1, -0.1, Inf+0.1])

plt.plot([-0.1, Inf+0.1], [-0.1, Inf+0.1], '-', linewidth=0.2)

plt.show()
