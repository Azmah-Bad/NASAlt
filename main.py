#!/usr/bin/env python3

from packages.router import Router
from packages.network import Network
from packages.functions import *
import numpy as np
import math

if __name__ == "__main__":
    # mat_adj = computeModelGML("inputs/france.gml")
    # print("Matrice d'adjacence : ")
    # print(mat_adj)

    """Test with a simple network"""
    mat_adj2 = np.array([
        [0, 4, 0, 0, 0, 0],
        [4, 0, 3, 6, 0, 2],
        [0, 3, 0, 0, 1, 0],
        [0, 6, 0, 0, 2, 0],
        [0, 0, 1, 2, 0, 5],
        [0, 2, 0, 0, 5, 0]
    ])

    mat_adj2_cor = np.array([
        [math.inf, 4, math.inf, math.inf, math.inf, math.inf],
        [4, math.inf, 3, 6, math.inf, 2],
        [math.inf, 3, math.inf, math.inf, 1, math.inf],
        [math.inf, 6, math.inf, math.inf, 2, math.inf],
        [math.inf, math.inf, 1, 2, math.inf, 5],
        [math.inf, 2, math.inf, math.inf, 5, math.inf]
    ])

    # Create a random demand matrix within a link's load can not exceed 70
    mat_dem = 10 * np.ones(shape=np.shape(mat_adj2_cor))

    mySimpleNetwork = Network(mat_adj2_cor, mat_dem)
    mySimpleNetwork.nDijkstra()
    computeLoadMatrix(mySimpleNetwork)
    print("\n\nloadMatrix : \n", mySimpleNetwork.LoadMatrix)
    disturbNetwork(mySimpleNetwork, 9)
    print('\n', mySimpleNetwork.DemandMatrix)
    print("\n\nloadMatrix : \n\n", mySimpleNetwork.LoadMatrix)

    """[a,c,d] = computeModelTXT('./inputs/abilene.txt')
    print("adj =\n",a)
    print('cap =\n',c)
    print('demand =\n',d)"""


