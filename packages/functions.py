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
    for dest, path in router.shortest_paths.items():
        for j in range(len(path)):
            if j < len(path) - 1 and path[j] == link[0] and path[j + 1] == link[1]:
                return int(dest)
    return -1

def howManySP(router,dest):
    """
    check how many shortest path exists to reach dest. Used for ECMP.
    :param router: an object Router
    :param dest:
    :return: int corresponding to the number of shortest path to reach dest
    """
    if string(dest) not in router.shortest_paths:
        return 0
    else:
        return len( router.shortest_path[string(dest)] ) #discuss of the structure of router.shortest_path, especially when there are several paths

def loadLink(routers, dem_mat, link):
    """
    check the charge of a link by finding all the routers which use this link
    :param router: an object Router
    :param demand_mat: square matrix of int
    :param link: a tuple corresponding to a link ( ex: (1,3) )
    :return: int>0 charge of a link
    """
    charge = 0
    value = 0
    for r in routers:  # browse the routers
        dest = isThereLink(r, link)
        if dest != -1:
            nb_shortest_paths = howManySP(router,dest)
            value = dem_mat[r.router_id][dest] / nb_shortest_paths #ECMP if there is several shortest paths to reach a dest
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
