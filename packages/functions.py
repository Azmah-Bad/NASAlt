#!/usr/bin/env python3

from random import *
import numpy as np
import os


def isThereLink(router, link):
    """
    check if a link exists
    :param router: an object Router
    :param link: a tuple corresponding to a link ( ex: (1,3) )
    :return dictionary: keys = (int) router_id of the dest we want to reach using this link | value = array of paths
        (= array of int) which contain the link
    """
    res = {}
    if router.ID == link[0]:
        if link[1] in router.neighbors:
            return {link[1]: [[1]]}
    for dest, paths in router.shortest_paths.items():
        paths_to_add = []
        for path in paths[0]:
            for j in range(len(path)):
                if j < len(path) - 1 and path[j] == link[0] and path[j + 1] == link[1]:
                    paths_to_add.append(path)
        if paths_to_add != []:
            res[dest] = paths_to_add
            paths_to_add = []
    return res


def howManySP(router, dest):
    """
    check how many shortest path exists to reach dest. Used for ECMP.
    :param router: an object Router
    :param dest:
    :return: int corresponding to the number of shortest path to reach dest
    """
    if dest not in router.shortest_paths.keys():
        return 0
    else:
        return len(router.shortest_paths[dest][
                       0])  # discuss of the structure of router.shortest_path, especially when there are several paths


def disturbNetwork(network, nb):
    """
    Increase randomly links load on the network
    :param network: an object Network
    :param nb: number of perturbations
    :return: void
    """
    demand_matrix = network.DemandMatrix
    capacity_matrix = network.CapacityMatrix

    for k in range(nb):
        i = randint(1, len(demand_matrix) - 1)
        j = randint(1, len(demand_matrix) - 1)
        demand_matrix[i][j] += randint(1, capacity_matrix[i][j] / 2) # maybe start at a lower value than 1 to have a real impact
    # computeLoadMatrix(..)


def computeLoadMatrix(network):
    demand_matrix = network.DemandMatrix
    capacity_matrix = network.CapacityMatrix

    for router in network.Routers:
        for i in range(len(network.LoadMatrix)):
            for j in range(len(network.LoadMatrix)):
                links = isThereLink( router, (i, j) )
                if links != {}:
                    for dest,paths in links.items():
                        cost = demand_matrix[router.ID][dest]
                        for path in paths:
                            if len(path) == 1:
                                network.LoadMatrix[router.ID][dest] += cost
                            for k in range(len(path)):
                                if k < len(path) - 1:
                                    network.LoadMatrix[path[k]][path[k+1]] += cost
                                    network.LoadMatrix[path[k+1]][path[k]] += cost
    #Compute the proportions
    for i in range(len(network.LoadMatrix)):
        for j in range(len(network.LoadMatrix)):
            network.LoadMatrix[i][j] /= capacity_matrix[i][j]



def loadLink(link, loadMatrix):
    """
    check the charge of a link by finding all the routers which use this link
    :param loadMatrix: an square array corresponding to the loadMatrix of the network
    :param link: a tuple corresponding to a link ( ex: (1,3) )
    :return: int>0 charge of a link
    """
    return loadMatrix[link[0]][link[1]]


def computeModel(filename):
    """construct the adjecency matrix of a graph descripted in the format used by http://sndlib.zib.de/home.action
            input : filename = relative or absolute path to the description of the graph
            output : adjMat = adjacency marix of the graph
    """

    if os.path.exists(filename):
        try:
            with open(filename) as f:
                content = f.read()
        except IOError:
            print("[computeModel] : erreur de lecture du fichier source\n")
    else:
        return -1

    [nodes, edges] = content.split("edge", 1)
    lastNodeDescription = nodes.rsplit("node", 1)[1]
    nodeNumber = int(lastNodeDescription.split("id")[1].split('\n')[0].replace(' ', '')) + 1

    edges = edges.split("edge")
    adjMat = np.zeros(dtype=np.uint8, shape=(nodeNumber, nodeNumber))
    for _, oneEdge in enumerate(edges):
        src = int(oneEdge.split("source")[1].split('\n')[0].replace(' ', ''))
        dest = int(oneEdge.split("target")[1].split('\n')[0].replace(' ', ''))
        adjMat[src][dest] = 1

    return adjMat

    def getMaxLoad(lMatrix):
        """
        Return the charge and position of the most charged link(s) (percentage) in the network
        :return: {maxLoad : positions with load==maxLoad}
        """
        value = np.amax(lMatrix)
        indexes = np.where(lMatrix == value)
        indexes = list(zip(indexes[0], indexes[1]))
        return {value: indexes}

    def isSaturated(lMatrix):
        """
        check if network is saturated
        :return: [positions of saturated links] or -1
        """
        saturated = np.where(lMatrix >= 100)
        if saturated[0].size > 0:
            return list(zip(saturated[0], saturated[1]))
        return -1
