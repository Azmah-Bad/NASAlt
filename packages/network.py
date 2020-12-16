from .router import Router
import numpy as np


class Network:
    def __init__(self, AdjacencyMatrix, DemandMatrix):
        self.AdjacencyMatrix = AdjacencyMatrix
        self.Routers = []

        for ID in range(len(AdjacencyMatrix)):
            self.Routers.append(Router(ID, AdjacencyMatrix, DemandMatrix))
        self.CapacityMatrix = 10*np.ones(shape=np.shape(AdjacencyMatrix))
        self.LoadMatrix = np.zeros(shape=np.shape(AdjacencyMatrix))

    def __init__(self, AdjacencyMatrix, DemandMatrix, capacityMatrix):
        self.AdjacencyMatrix = AdjacencyMatrix
        self.Routers = []

        for ID in range(len(AdjacencyMatrix)):
            self.Routers.append(Router(ID, AdjacencyMatrix, DemandMatrix))
        self.CapacityMatrix = capacityMatrix
        self.LoadMatrix = np.zeros(shape=np.shape(AdjacencyMatrix))

    def getRouterByID(self, ID: int) -> Router or None:
        """
        :param ID: int
        :return: the router with the id ID if it doesnt exists returns  None
        """
        for Router in self.Routers:
            if Router.ID == ID:
                return Router
        return None

    def nDijkstra(self):
        """
        compute the shortest path of all the routers
        :return:
        """
        for router in self.Routers:
            router.dijkstra()
        return 1

    def getAllRouterIDs(self):
        """
        Return all the RouterIDs of the network
        :return: array of int corresponding to the RouterIDs
        """
        return [Router.ID for Router in self.Routers]

    def getAllShortestPath(self):
        """
        Print all the shortest path of each router of the network
        """
        for router in self.Routers:
            print("#", router.ID, "\n", router.shortest_paths, "\n")
        return 1

    def isCongested(self) -> bool:  # TODO :: how are capacity matrix are handled ?
        raise NotImplementedError


