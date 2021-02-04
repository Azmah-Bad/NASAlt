#!/usr/bin/env python3

from .network import Network
from random import *
import numpy as np
import os
import math


def isThereLink(router, link, sp={}):
    """
    check if a link exists
    :param router: an object Router
    :param link: a tuple corresponding to a link ( ex: (1,3) )
    :return dictionary: keys = (int) router_id of the dest we want to reach using this link | value = array of paths
        (= array of int) which contain the link
    """
    if sp == {}:
        shortest_paths = router.shortest_paths
    else:
        shortest_paths = sp

    res = {}
    if router.ID == link[0]:
        if link[1] in router.neighbors:
            return {link[1]: [[1]]}
    for dest, paths in shortest_paths.items():
        paths_to_add = []
        for path in paths[0]:
            if len(path) == 1 and router.ID == link[0] and link[1] in router.neighbors:
                paths_to_add.append([[link[1]]])
            for j in range(len(path)):
                if (j < len(path) - 1 and path[j] == link[0] and path[j + 1] == link[1]) or (
                        j < len(path) - 1 and path[j + 1] == link[0] and path[j] == link[1]):
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


def disturbNetwork(network):
    """
    Increase randomly links load on the network
    :param network: an object Network
    :param nb: number of perturbations
    :return: void
    """
    capacity_matrix = network.CapacityMatrix

    while (isSaturated(network.LoadMatrix) == -1):
        i = randint(1, len(network.DemandMatrix) - 1)
        j = randint(1, len(network.DemandMatrix) - 1)
        additional_load = randint(int(capacity_matrix[i][j] / 3), int(
            3 * capacity_matrix[i][j] / 4))  # maybe start at a lower value than 1 to have a real impact
        network.DemandMatrix[i][j] += additional_load / network.CapacityMatrix[i][j]
        network.DemandMatrix[j][i] += additional_load / network.CapacityMatrix[i][j]
        network.nDijkstra()


def computeLoadMatrix(network):
    demand_matrix = network.DemandMatrix
    capacity_matrix = network.CapacityMatrix

    network.LoadMatrix = np.zeros(shape=np.shape(demand_matrix))

    for router in network.Routers:
        for i in range(len(network.LoadMatrix)):
            for j in range(len(network.LoadMatrix)):
                links = isThereLink(router, (i, j))
                if links != {}:
                    for dest, paths in links.items():
                        cost = demand_matrix[router.ID][dest]
                        for path in paths:
                            network.LoadMatrix[i][j] += cost / capacity_matrix[i][j] * 100

    network.LoadMatrix = np.around(network.LoadMatrix, decimals=1)


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
    adjMat = math.inf*np.ones(dtype=np.uint8, shape=(nodeNumber, nodeNumber))
    for _, oneEdge in enumerate(edges):
        src = int(oneEdge.split("source")[1].split('\n')[0].replace(' ', ''))
        dest = int(oneEdge.split("target")[1].split('\n')[0].replace(' ', ''))
        adjMat[src][dest] = 1

    return adjMat


def computeModelTXT(filename, nameToID = None, adjMat = np.array(None), capMat = np.array(None), demandMatrix = np.array(None)):
    """construct the adjecency matrix of a graph descripted in the format used by http://sndlib.zib.de/home.action in native files
        input : filename = relative or absolute path to the description of the graph
                nameToID = if None, function computes it according to file (only for network description in source file because only demands can change from one not source file to another)
                adjMat = if None, function computes it according to file (only for network description in source file because only demands can change from one not source file to another)
                capMat = if None, function computes it according to file (only for network description in source file because only demands can change from one not source file to another)
                demandMatrix = if None, function computes it according to file, not supposed to be None for now
        output : inputs updated according to file
    """

    if os.path.exists(filename):
        try:
            with open(filename) as f:
                content = f.read()
        except IOError:
            print("[computeModelTXT] : erreur de lecture du fichier source\n")
    else:
        print('[computeModelTXT] : Le fichier source n\'existe pas')
        return -1

    if nameToID == None:
        nameToID = {}
        i = 0
        [nodes, edges] = content.split("# LINK SECTION", 1)
        nodes = nodes.split('#')[-1].split("NODES (")[1].split('\n')
        for oneNode in nodes:
            name = oneNode.split('(', 1)[0]
            if len(name) > 0 and name != ')':
                name = name.replace(' ', '')
                nameToID[name] = i
                i+=1

    if np.any(capMat) == None and np.any(adjMat) == None :
        adjMat = math.inf*np.ones(dtype=np.uint8, shape=(i, i))
        capMat = np.zeros(dtype=np.uint64, shape=(i,i))
        edges = edges.split("LINKS (")[1].split("# DEMAND SECTION")[0].split('\n')
        for oneEdge in edges:
            name = oneEdge.split('(')[0].replace(' ', '')
            if len(name) > 0 and name != ')':
                cap = np.int(oneEdge.split(')',1)[1].split('(',1)[1].split('.',1)[0].replace(' ',''))
                names = name.split('_')
                adjMat[nameToID[names[0]]][nameToID[names[1]]] = 1
                adjMat[nameToID[names[1]]][nameToID[names[0]]] = 1
                capMat[nameToID[names[0]]][nameToID[names[1]]] = cap
                capMat[nameToID[names[1]]][nameToID[names[0]]] = cap

    if np.any(demandMatrix) == None:
        demandMatrix = np.zeros(dtype=np.uint64, shape=adjMat.shape)
        demandDesc = content.split("DEMANDS (\n",1)[1].split('\n')
        for oneDemand in demandDesc:
            if len(oneDemand) < 5:
                break
            names = oneDemand.split('_')
            names[0] = names[0].replace(' ', '')
            dValue = np.int(names[1].split(') ')[1].split(' ')[1].split('.')[0])
            names[1] = names[1].split(' ')[0]
            demandMatrix[nameToID[names[0]], nameToID[names[1]]] = int(dValue)

    return nameToID, adjMat, capMat, demandMatrix

def getDataset(filename):
    """ compute a dataset from a file descripting a network and many mor files descripting different demand matrixes for this network
            input : network description file (/!\ if filename = xxx then the directory containing demand descriptions has to be names demands-xxx)
            output : [(adjacencyMatrix,demandMatrix,capacityMatrix)]
    """
    if not os.path.exists(filename):
        print('[getDataSet] : Le fichier source n\'existe pas')
        return -1
    try:
        demandRepo = "{}/demands-{}".format("".join(filename.split('/')[:-1]), filename.split('/')[-1].split('.',1)[0]) if '/' in filename else "demands-{}".format(filename)
        demandFiles = os.listdir(demandRepo)
    except FileNotFoundError:
        print("[getDataset] : cannot list demand files with repo_name=", "{}/demands-{}".format("".join(filename.split('/')[:-1]), filename.split('/')[-1].split('.',1)[0]))
        return -1
    [namesToIDs, adjacency, capacity, demand] = computeModelTXT(filename)
    demands = []
    for oneDFile in demandFiles:
        [_, _, _, oneDemand] = computeModelTXT("{}/{}".format(demandRepo,oneDFile), namesToIDs, adjacency, capacity)  # get only demand from file
        if not (oneDemand.any() == None):
            demands.append(oneDemand)
        else:
            print('[getDataset] : oneDemand is None')
            return -1
    ds = []
    #adjust demand matrix given capacity
    tempNetwork = Network(adjacency,oneD,capacity)
    for oneD in demands:
        tempNetwork.DemandMatrix = oneD
        computeLoadMatrix(tempNetwork)
        maxLoadWithLinks = getMaxLoad(tempNetwork.LoadMatrix)
        maxLoad = list(maxLoadWithLinks)[0]
        toSaturation = 100/maxLoad
        if toSaturation > 0:
            oneD = oneD*toSaturation
            ds.append((adjacency,oneD,capacity))
    return ds


def isSaturated(lMatrix):
    """
    check if network is saturated
    :return: [positions of saturated links] or -1
    """
    saturated = np.where(lMatrix >= 100)
    if saturated[0].size > 0:
        return list(zip(saturated[0], saturated[1]))
    return -1


def getMaxLoad(lMatrix):
    """
    Return the charge and position of the most charged link(s) (percentage) in the network
    :return: {maxLoad : positions with load==maxLoad}
    """
    value = np.amax(lMatrix)
    indexes = np.where(lMatrix == value)
    indexes = list(zip(indexes[0], indexes[1]))
    return {value: indexes}


def networkFromList(a_list):
    """
    Compute a network from a 1D list that contains an adjacency matrix, a demand matrix and a load matrix
    :return: Network
    """

    # get the different matrix in a 1D vector
    adjacency_matrix = np.array(a_list[0:int(len(a_list) / 3)])
    demand_matrix = np.array(a_list[int(len(a_list) / 3):int(2 * len(a_list) / 3)])

    # reshape
    adjacency_matrix = adjacency_matrix.reshape(int(math.sqrt(len(adjacency_matrix))),
                                                int(math.sqrt(len(adjacency_matrix))))
    demand_matrix = demand_matrix.reshape(int(math.sqrt(len(demand_matrix))), int(math.sqrt(len(demand_matrix))))

    network = Network(adjacency_matrix, demand_matrix)


def printDifference(mat1, mat2):
    """
    print a matrix in a different way where a value has been changed, help for debug
    """
    print("[")
    for i in range(len(mat1)):
        add = []
        for j in range(len(mat1)):
            if mat1[i][j] != mat2[i][j]:
                add.append("+" + str(mat2[i][j])) if mat1[i][j] < mat2[i][j] else add.append("_" + str(mat2[i][j]))
            else:
                add.append(str(mat2[i][j]))
        print(add)
    print("]")


def train(network, max_iter, loop):
    """
    Compute new weights for the Adjacency matrix of a saturated network
    :param network: Network object
    :param max_iter: (int) the maximum number of times the model has to readjust the weights
    :param loop: (boolean) readjust the weight in a loop or not
    """
    iter = 0
    network.nDijkstra()
    condition = isSaturated(network.LoadMatrix) != - 1 and iter < max_iter if loop else iter < max_iter
    load_before = np.around(network.LoadMatrix, decimals=1)
    adj_before = np.around(network.AdjacencyMatrix, decimals=1)
    # print("\n\n----- Adjacency Matrix before -----\n", adj_before)
    # print("\n\n----- Load Matrix before -----\n", load_before)

    if isSaturated(network.LoadMatrix) == -1:
        disturbNetwork(network)
        print("\n\n----- Load Matrix after disturb -----\n", network.LoadMatrix)

    print("\n#Start\n")
    while isSaturated(network.LoadMatrix) != - 1 and iter < max_iter:

        """Find the saturated link and the minimum increment """
        saturated_link = getMaxLoad()
        routersLoad = {}  # ex : {1: {dest1: [sp], dest2: [sp] ..} 2: …}

        for router in Network.Routers:
            alternative_sp = router.restrainedDijskstra(saturated_link)
        where = isThereLink(router, router.saturated_link, alternative_sp)
        if where != {}:
            routersLoad[router.ID] = router.minIncr(alternative_sp)

        rand_router = randint(0, len(routersLoad))
        rand_dest = randint(0, len(routersLoad[rand_router]))
        minIncr = routersLoad[rand_router][rand_dest]

        """
        70% > increment only the saturated link
        30% > increment the nearby links
        """
        incrOneLink = randint(1, 10) <= 7
        if incrOneLink:
            network.AdjacencyMatrix[saturated_link[0]][saturated_link[1]] += minIncr

        # increment the nearby links
        else:
            situation = randint(1,100);
            nearbyLink = nearbyLinks(network.AdjacencyMatrix,saturated_link)
            # Increment all the nearby links with an equal cost
            if situation <= 33 :
                i = 0
                while minIncr > 0 and i < len(nearbyLink) - 1 :
                    network.AdjacencyMatrix[(nearbyLink[i])[0]][(nearbyLink[i])[1]] += 1
                    i += 1
                    minIncr -= 1

            # Increment the saturated link with 50% of minIncr and all the nearby links with an equal cost
            elif situation <= 66:
                bigIncr = minIncr // 2
                minIncr -= bigIncr
                network.AdjacencyMatrix[saturated_link[0]][saturated_link[1]] += bigIncr
                i = 0

                while minIncr > 0 and i < len(nearbyLink) - 1 :
                    network.AdjacencyMatrix[(nearbyLink[i])[0]][(nearbyLink[i])[1]] += 1
                    i += 1
                    minIncr -= 1

            # Increment progressively the saturated link and the nearby links
            else:
                i = 0
                progressive_incr = [30, 20, 10]
                network.AdjacencyMatrix[saturated_link[0]][saturated_link[1]] += round(0.4*minIncr)
                while i < min(len(nearbyLink) - 1, len(progressive_incr)):
                    network.AdjacencyMatrix[(nearbyLink[i])[0]][(nearbyLink[i])[1]] += round(minIncr*progressive_incr[i])
                    i += 1

    # prints
    color_red = '\033[31m'
    color_green = '\033[32m'
    print(color_red + "\n\n----- Adjacency Matrix after -----") if isSaturated(network.LoadMatrix) != -1 else print(
        color_green + "\n\n----- Adjacency Matrix after -----")
    print('\033[0m')
    printDifference(adj_before, network.AdjacencyMatrix)
    print(color_red + "\n\n----- Load Matrix after -----") if isSaturated(network.LoadMatrix) != -1 else print(
        color_green + "\n\n----- Load Matrix after -----")
    print('\033[0m')
    printDifference(load_before, network.LoadMatrix)


def fromSPGetLinks(sp):
    """
    Compute the links associated to a shortest path
    :param sp: array of router ID -> shortest path
    :return: array of tuple corresponding to the links
    """
    links = []
    for i in range(sp):
        if i != len(sp) - 1:
            links.append((sp[i], sp[i + 1]))

    return links


def nearbyLinks(adjacency_matrix, link):
    res = []
    for idx, w in enumerate(adjacency_matrix[link[1]]):
        if w > 0:
            res.append((link[1], idx))

    return res
