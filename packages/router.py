#!/usr/bin/env python3
import math
import numpy as np


class Router:
    def __init__(self, router_id, adjacency_matrix, demand_matrix):
        self.ID = router_id  # We define the router id as the position of the router in the adjency matrix
        self.adjacency_matrix = adjacency_matrix
        weight = adjacency_matrix[router_id]  # Weights of the different links to the neighbors
        self.charge = demand_matrix[router_id]
        self.shortest_paths = {}  # Shortests paths to the neighbors
        self.neighbors = []  # neighbors' router id

        # define the neighbors
        for j in range(0, len(weight)):
            if weight[j] != 0:
                self.neighbors.append(j)

    def __str__(self):
        return 'router : %.2d' % self.ID

    def dijkstra(self):
        """
        fills in the routing table of the router using dijkstra algorithm
        :return:
        """
        # init shortest paths
        NextHops = []
        for Destination in range(len(self.adjacency_matrix)):
            if self.adjacency_matrix[self.ID][Destination] == math.inf:
                self.shortest_paths[Destination] = ([], math.inf)
            else:
                self.shortest_paths[Destination] = ([Destination], self.adjacency_matrix[self.ID][Destination])
                NextHops.append(Destination)
            self.shortest_paths[self.ID] = ([], 0)

        while NextHops:
            for NextHop in NextHops:
                CostToHop = self.shortest_paths[NextHop][1]
                for Destination, Cost in enumerate(self.adjacency_matrix[NextHop]):
                    if Cost + CostToHop < self.shortest_paths[Destination][1]:  # less costly route
                        if Cost + CostToHop == 1:
                            print('a')
                        self.shortest_paths[Destination] = (self.shortest_paths[NextHop][0] + [Destination], Cost + CostToHop)
                        NextHops.append(Destination)
                NextHops.remove(NextHop)


if __name__ == "__main__":
    mat_adj = [[0, 2, 1], [0, 0, 3], [1, 2, 0]]
    print("Matrice d'adjacence : ")
    print(mat_adj)

    mat_dem = [[0, 40, 100], [0, 0, 30], [10, 32, 0]]
    print("\nMatrice de demande :")
    print(mat_dem)

    r1 = Router(0, mat_adj, mat_dem)
    r = [r1]
    print("Voisins :")
    print(r1.neighbours)
    print("\nR1 ID :")
    print(r1)
    print(r1.getShortestPaths())
