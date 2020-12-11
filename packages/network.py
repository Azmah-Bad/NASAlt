from .router import Router


class Network:
    def __init__(self, AdjacencyMatrix, DemandMatrix):
        self.AdjacencyMatrix = AdjacencyMatrix
        self.Routers = []

        for ID in range(len(AdjacencyMatrix)):
            self.Routers.append(Router(ID, AdjacencyMatrix, DemandMatrix))

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
        allRouterIDs = []
        for router in self.Routers:
            allRouterIDs.append(router.ID)
        return allRouterIDs

    def getAllShortestPath(self):
        """
        Print all the shortest path of each router of the network
        """
        for router in self.Routers:
            print("#", router.ID, "\n", router.shortest_paths, "\n")
        return 1
