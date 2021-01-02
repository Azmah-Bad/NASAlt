#!/usr/bin/env python3

from packages.router import Router
from packages.network import Network
from packages.functions import *
import numpy as np
import math

def main(network, max_iter):
    iter = 0
    network.nDijkstra()
    print("\n\n----- Adjacency Matrix before -----\n", network.AdjacencyMatrix)
    print("\n\n----- Load Matrix before -----\n", network.LoadMatrix)

    if isSaturated(network.LoadMatrix) == -1:
        disturbNetwork(network)
        print("\n\n----- Load Matrix after disturb -----\n",network.LoadMatrix)

    print("\n#Start\n")
    while isSaturated(network.LoadMatrix) != - 1 and iter < max_iter:
        maxLink = getMaxLoad(network.LoadMatrix)

        for _,links in maxLink.items() :
            for link in links :
                network.AdjacencyMatrix[link[0]][link[1]] += 1/network.CapacityMatrix[link[0]][link[1]] #minIncr
        network.nDijkstra()
        iter += 1
    network.AdjacencyMatrix = np.around(network.AdjacencyMatrix, decimals=1)

    color_red = '\033[31m'
    color_green = '\033[32m'
    print(color_red + "\n\n----- Adjacency Matrix after -----") if isSaturated(network.LoadMatrix) != -1 else print(color_green + "\n\n----- Adjacency Matrix after -----")
    print('\033[0m')
    print(network.AdjacencyMatrix)
    print(color_red + "\n\n----- Load Matrix after -----") if isSaturated(network.LoadMatrix) != -1 else print(color_green + "\n\n----- Load Matrix after -----")
    print('\033[0m')
    print(network.LoadMatrix)


if __name__ == "__main__":
    mat_adj = computeModel("inputs/france.gml")
    MAX_ITER = 50

    """Test with a simple network"""
    mat_adj2_cor = np.array([
        [math.inf, 4, math.inf, math.inf, math.inf, math.inf],
        [4, math.inf, 3, 6, math.inf, 2],
        [math.inf, 3, math.inf, math.inf, 1, math.inf],
        [math.inf, 6, math.inf, math.inf, 2, math.inf],
        [math.inf, math.inf, 1, 2, math.inf, 5],
        [math.inf, 2, math.inf, math.inf, 5, math.inf]
    ])

    mat_cap = np.array([
        [0, 40, 70, 80, 60, 0],
        [40, 0, 56, 87, 12, 2],
        [70, 56, 0, 87, 11, 3],
        [80, 87, 87, 0, 21,10],
        [60, 12, 11, 21, 0, 50],
        [0, 2, 3, 10, 50, 0]
    ])
        #Create a random demand matrix within a link's load can not exceed 70
    mat_dem = 10*np.ones(shape=np.shape(mat_adj2_cor))

    mySimpleNetwork = Network(mat_adj2_cor,mat_dem)

    main(mySimpleNetwork, MAX_ITER)




