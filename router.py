#!/usr/bin/env python3

from random import *

class Router:
    def __init__ (self,router_id,adj_mat,dem_mat):
        self.router_id = router_id #We define the router id as the position of the router in the adjency matrix
        wheight = adjency_matrix[router_id] #Weights of the different links to the neighbors
        self.charge = demand_matrix[router_id]
        shortest_paths = {} #Shortests paths to the neighbors
        
       # for i in range( len(distance) ):
        #    if distance[i] != 0:
         #       shortest_paths[str(i)] = [randint(2,3),randint(2,3)] #replace the random int by the result of dijkstra on the router i

        shortest_paths[str(1)] = [1] #replace the random int by the result of dijkstra on the router i
        shortest_paths[str(2)] = [1,2] #replace the random int by the result of dijkstra on the router i
        self.shortest_paths = shortest_paths
        self.neighbors = [] #neighbors' router id

        #define the neighbors
        for j in range(0,len(distance) ):
            if ( distance[j] != 0 ):
                self.neighbors.append(j)


    def __str__ (self):
        return 'router : %.2d' % (self.router_id) 

    def getShortestPaths (self):
        return self.shortest_paths


if __name__ == "__main__":

    mat_adj = [[0,2,1],[0,0,3],[1,2,0]] 
    print("Matrice d'adjacence : ")
    print(mat_adj)

    mat_dem = [[0,40,100],[0,0,30],[10,32,0]] 
    print("\nMatrice de demande :")
    print(mat_dem)

    r1 = Router(0,mat_adj,mat_dem)
    r = [r1]
    print("Voisins :")
    print(r1.neighbours)
    print("\nR1 ID :")
    print(r1)
    print(r1.getShortestPaths())

