#!/usr/bin/env python3

from random import *
import numpy as np
import os


def isThereLink(router, link):
    """
    check if a link exists
    :param router: an object Router
    :param link: a tuple corresponding to a link ( ex: (1,3) )
    :return: -1 if the link does not exist, (int) router_id of the dest we want to reach using this link
    """
    if router.ID == link[0]:
        if link[1] in router.neighbors :
            return link[1]
    for dest, path in router.shortest_paths.items():
        #print("path : ", path[0])
        for j in range(len(path[0])):
            if j < len(path[0]) - 1 and path[0][j] == link[0] and path[0][j + 1] == link[1]:
                return dest
    return -1

def howManySP(router,dest):
    """
    check how many shortest path exists to reach dest. Used for ECMP.
    :param router: an object Router
    :param dest:
    :return: int corresponding to the number of shortest path to reach dest
    """
    if dest not in router.shortest_paths:
        return 0
    else:
        return len( router.shortest_paths[dest][0] ) # /!\ change to fit with the new version of Dijkstra with several SP!

def disturbNetwork(network):
    """
    Increase randomly links load on the network
    :param network: an object Network
    :return: void
    """
    demand_matrix = network.DemandMatrix
    capacity_matrix = network.CapacityMatrix

    i = randint( 1,len(demand_matrix)-1 )
    j = randint( 1,len(demand_matrix)-1 )
    demand_matrix[i][j] += randint( 1,capacity_matrix[i][j]/2 )

    while demand_matrix[i][j] >= capacity_matrix[i][j]:
        i = randint( 1,len(demand_matrix)-1 )
        j = randint( 1,len(demand_matrix)-1 )
        demand_matrix[i][j] += randint( 1,capacity_matrix[i][j]/2 ) #maybe start at a lower value than 1 to have a real impact

    #computeLoadMatrix(..)

def computeLoadMatrix(network): 
    demand_matrix = network.DemandMatrix
    capacity_matrix = network.CapacityMatrix
    print("\n demand_matrix \n",demand_matrix,"\n")

    for i in range( len(network.LoadMatrix) ):
        for j in range( len(network.LoadMatrix) ):
            network.LoadMatrix[i][j] = loadLink(network.Routers,demand_matrix, (i,j) ) 

def loadLink(routers, dem_mat, link):
    """
    check the charge of a link by finding all the routers which use this link
    :param routers: an array of object Router
    :param demand_mat: square matrix of int
    :param link: a tuple corresponding to a link ( ex: (1,3) )
    :return: int>0 charge of a link
    """
    charge = 0
    value = 0
    for r in routers:  # browse the routers
        dest = isThereLink(r, link)
        if dest != -1:
            nb_shortest_paths = howManySP(r,dest)
            value = dem_mat[r.ID][dest] / nb_shortest_paths #ECMP if there is several shortest paths to reach a dest
            charge += value
    return charge


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
