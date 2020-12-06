#!/usr/bin/env python3
import math
import numpy as np


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
                self.shortest_paths[Destination] = ([], math.inf)
            else:
                self.shortest_paths[Destination] = ([Destination], self.adjacency_matrix[self.ID][Destination])
                NextHops.append(Destination)
            self.shortest_paths[self.ID] = ([], 0)

        # for each hop we look at it's adjacent router and compare them to the path in the routing table
        while NextHops:
            for NextHop in NextHops:
                CostToHop = self.shortest_paths[NextHop][1]  # the cost of the current hop
                for Destination, Cost in enumerate(self.adjacency_matrix[NextHop]):
                    if Cost + CostToHop < self.shortest_paths[Destination][1]:  # less costly route
                        self.shortest_paths[Destination] = (
                            self.shortest_paths[NextHop][0] + [Destination], Cost + CostToHop)
                        NextHops.append(Destination)
                NextHops.remove(NextHop)

        return self.shortest_paths
