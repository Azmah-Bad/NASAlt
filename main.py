#!/usr/bin/env python3

from packages.router import Router
from packages.network import Network
from packages.functions import *
import numpy as np

if __name__ == "__main__":

    mat_adj = computeModel("inputs/france.gml")
    #print("Matrice d'adjacence : ")
    #print(mat_adj)

    """Test with a simple network"""
    mat_adj2 = np.array([
        [0,4,0,0,0,0],
        [4,0,3,6,0,2],
        [0,3,0,0,1,0],
        [0,6,0,0,2,0],
        [0,0,1,2,0,5],
        [0,2,0,0,5,0]
    ])
        #Create a random demand matrix within a link's load can not exceed 70 
    mat_dem = np.random.randint(70, size=(6,6))
    
    mySimpleNetwork = Network(mat_adj2,mat_dem)
    print(mySimpleNetwork.getAllRouterIDs())
    mySimpleNetwork.nDijkstra()
    mySimpleNetwork.getAllShortestPath()