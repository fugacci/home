import math
import sys
import numpy as np

nummod=80

numfun=2

L=[]

for i in range(numfun):
    L.append(np.zeros(1))


for model in range(nummod):

    for j in range(numfun):

        pgeomfile = open("functions/{}-{}.usr".format(model+1,j+1), 'r')

        pgeom=np.loadtxt(pgeomfile)

        L[j]=np.concatenate((L[j],pgeom), axis=None)

        pgeomfile.close()

    print(model)

minimi=np.zeros(numfun)
massimi=np.zeros(numfun)

for i in range(numfun):
    minimi[i]=np.amin(np.delete(L[i], 0))
    massimi[i]=np.amax(np.delete(L[i], 0))

#### STAMPA #####

minimi=np.round(minimi,3)
massimi=np.round(massimi,3)


wfile = open("MinimiMassimiFunzioni.txt", "w")
for i in range(numfun):
    wfile.write("{} ".format(minimi[i]))
wfile.write("\n")
for i in range(numfun):
    wfile.write("{} ".format(massimi[i]))
wfile.write("\n")
wfile.close()
