#!/usr/bin/env python3

from packages.router import Router
from packages.functions import *

if __name__ == "__main__":

    mat_adj = computeModel("inputs/france.gml")
    print("Matrice d'adjacence : ")
    print(mat_adj)

    mat_dem = [[0,40,100],[0,0,30],[10,32,0]] 
    
