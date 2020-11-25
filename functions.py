#!/usr/bin/env python3

from random import *

'''check if a link exists
*   return : -1 if the link does not exist, int>0 equals to the weight if it does 
'''
def isThereLink(router,link):
    for dest,path in router.shortest_paths.items():
        for j in range( len(path) ):
            if ( j < len(path)-1 and path[j] == link[0] and  path[j+1] == link[1] ):
                return dest
    return -1



#check the charge of a link by finding all the routers which use this link
def chargeLink(routers, dem_mat, link):
    charge = 0
    value = 0
    for r in routers: #browse the routers
        dest = isThereLink(r,link)
        if dest != -1:
            value = dem_mat[r.router_id][int(dest)] 
            charge += value 
    return charge

if __name__ == "__main__":

    mat_adj = [[0,2,1],[0,0,3],[1,2,0]] 
    print("Matrice d'adjacence : ")
    print(mat_adj)

    mat_dem = [[0,40,100],[0,0,30],[10,32,0]] 
    print("\nMatrice de demande :")
    print(mat_dem)

    r1 = Router(0,mat_adj,mat_dem,0)
    r = [r1]
    print(r1)
    print(r1.getShortestPaths())

    print("\nLink (1,2) does exist : ")
    print( isThereLink( r1,(1,2) ) )

    print("\nCharge du lien (1,2)")
    print(chargeLink(r,mat_dem,(1,2)))

