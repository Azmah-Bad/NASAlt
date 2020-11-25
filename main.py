#!/usr/bin/env python3

from packages.router import Router
from packages.functions import *

if __name__ == "__main__":

    mat_adj = [[0,2,1],[0,0,3],[1,2,0]] 
    print("Matrice d'adjacence : ")
    print(mat_adj)

    mat_dem = [[0,40,100],[0,0,30],[10,32,0]] 
    print("\nMatrice de demande :")
    print(mat_dem)

    r1 = Router(0,mat_adj,mat_dem,)
    r = [r1]
    print(r1)
    print(r1.getShortestPaths())

    print("\nLink (1,2) does exist : ")
    print( isThereLink( r1,(1,2) ) )
