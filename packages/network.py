from .router import Router


class Network:
    def __init__(self, AdjacencyMatrix, DemandeMatrix):
        self.AdjacencyMatrix = AdjacencyMatrix
        self.Routers = []

        for id in range(len(AdjacencyMatrix)):
            self.Routers.append(Router(id, AdjacencyMatrix, DemandeMatrix))

    def dijkstra(self):
        """
        compute the shortest path of all the routers
        :return:
        """
