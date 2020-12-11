#!/usr/bin/env python3
import math
import numpy as np
from copy import copy


class Router:
    def __init__(self, router_id, adjacency_matrix, demand_matrix):
        """
        Router class
        :param router_id:  int representing the Router's ID
        :param adjacency_matrix:  numpy array of the adjacency matrix, unreachable immediate links have a value of math.inf
        :param demand_matrix:  numpy array  of the demand matrix
        """
        self.ID = router_id  # We define the router id as the position of the router in the adjency matrix
        self.adjacency_matrix = adjacency_matrix
        weight = adjacency_matrix[router_id]  # Weights of the different links to the neighbors
        self.charge = demand_matrix[router_id]
        self.shortest_paths = {}  # Shortest paths to the neighbors
        self.neighbors = []  # neighbors' router id

        # define the neighbors
        for j in range(0, len(weight)):
            if weight[j] != math.inf:
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
                self.shortest_paths[Destination] = ([[]], math.inf)
            else:
                self.shortest_paths[Destination] = ([[Destination]], self.adjacency_matrix[self.ID][Destination])
                NextHops.append(Destination)
            self.shortest_paths[self.ID] = ([[]], 0)

        # for each hop we look at it's adjacent router and compare them to the path in the routing table
        while NextHops:
            for NextHop in NextHops:
                CostToHop = self.shortest_paths[NextHop][1]  # the cost of the current hop
                for Destination, Cost in enumerate(self.adjacency_matrix[NextHop]):
                    if Cost + CostToHop < self.shortest_paths[Destination][1]:  # less costly route
                        self.shortest_paths[Destination] = (
                            [PathToHop + [Destination] for PathToHop in self.shortest_paths[NextHop][0]],
                            Cost + CostToHop)
                        NextHops.append(Destination)
                    elif Cost + CostToHop == self.shortest_paths[Destination][1] and not \
                            self.shortest_paths[Destination][1] == math.inf:  # same costly route
                        for OldRoute in self.shortest_paths[NextHop][0]:
                            NewRoute = OldRoute + [Destination]
                            self.shortest_paths[Destination][0].append(NewRoute)
                        NextHops.append(Destination)
                NextHops.remove(NextHop)

        return self.shortest_paths

    def restrainedDijkstra(self, ids):
        """
        compute the most beneficial alternative paths which do not use the identified link
        :param ids: router ids of two router at each end of the charged link
        """

        adj_mat = copy(self.adjacency_matrix)
        for link in ids:
            adj_mat[link[0]][link[1]] = math.inf
            adj_mat[link[1]][link[0]] = math.inf
        sp = {}
        NextHops = []
        # init shortest paths
        NextHops = []
        for Destination in range(len(adj_mat)):
            if adj_mat[self.ID][Destination] == math.inf:
                sp[Destination] = ([[]], math.inf)
            else:
                sp[Destination] = ([[Destination]], adj_mat[self.ID][Destination])
                NextHops.append(Destination)
            sp[self.ID] = ([[]], 0)

        # for each hop we look at it's adjacent router and compare them to the path in the routing table
        while NextHops:
            for NextHop in NextHops:
                CostToHop = sp[NextHop][1]  # the cost of the current hop
                for Destination, Cost in enumerate(adj_mat[NextHop]):
                    if Cost + CostToHop < sp[Destination][1]:  # less costly route
                        sp[Destination] = (
                            [PathToHop + [Destination] for PathToHop in sp[NextHop][0]], Cost + CostToHop)
                        NextHops.append(Destination)
                    elif Cost + CostToHop == sp[Destination][1] and not \
                            sp[Destination][1] == math.inf:  # same costly route
                        for OldRoute in sp[NextHop][0]:
                            NewRoute = OldRoute + [Destination]
                            sp[Destination][0].append(NewRoute)
                        NextHops.append(Destination)
                NextHops.remove(NextHop)

        return sp

    def getMinIncrements(self, alternativeSP):
        """
        compute the minimal increment needed to add to best alternative path for all destinations
        :param alternativeSP: alternative shortest paths (computed by restrainedDijsktra)
        """
        minIncrements = {}
        for dest in range(len(self.adjacency_matrix)):
            minIncrements[dest] = alternativeSP[dest][1] - self.shortest_paths[dest][1]

        return minIncrements
