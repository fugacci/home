import sys
import itertools
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm


def createColoredOFF(model, fun, min_val, max_val):

    FUNfile = open("functions/{}-{}.usr".format(model,fun), 'r')

    Fv = np.loadtxt(FUNfile)
    cmap = mpl.cm.coolwarm
    norm = mpl.colors.SymLogNorm(linthresh=1, vmin=min_val, vmax=max_val)
    Cv = cmap(norm(Fv))

    FUNfile.close()

    OFFfile = open("data/{}.off".format(model), 'r')

    COFFfile = open("data_with_functions/{}-{}.off".format(model,fun), "w")


    for line in itertools.islice(OFFfile, 0, 2):  # start=17, stop=None
            pass

    COFFfile.write("COFF\n")
    COFFfile.write("\n")

    line = OFFfile.readline()

    COFFfile.write(line)

    nv, nt = (int(line.split()[0]), int(line.split()[1]))

    # print(nv)

    i=0

    for line in itertools.islice(OFFfile, 0, nv):
        color=Cv[i]
        newline=line.rstrip("\n") + \
            " {} {} {} {}\n".format(color[0], color[1], color[2], color[3])
        COFFfile.write(newline)
        i=i+1

    for line in itertools.islice(OFFfile, 0, nt):
        COFFfile.write(line)

    OFFfile.close()
    COFFfile.close()

    return 0


################### MAIN ##############

nummod=80

numfun=2

extremal_values=np.loadtxt("MinimiMassimiFunzioni.txt")

for m in range(nummod):

    for f in range(numfun):

        print(m)
        print(f)

        createColoredOFF(m+1, f+1, extremal_values[0][f],extremal_values[1][f])
