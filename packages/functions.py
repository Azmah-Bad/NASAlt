#!/usr/bin/env python3

from random import *
import numpy as np


'''check if a link exists
*   return : -1 if the link does not exist, router_id of the dest we want to reach using this link 
'''
def isThereLink(router,link):
    for dest,path in router.shortest_paths.items():
        for j in range( len(path) ):
            if ( j < len(path)-1 and path[j] == link[0] and  path[j+1] == link[1] ):
                return dest
    return -1



'''check the charge of a link by finding all the routers which use this link
 *  return: int>0 charge of a link
'''
def chargeLink(routers, dem_mat, link):
    charge = 0
    value = 0
    for r in routers: #browse the routers
        dest = isThereLink(r,link)
        if dest != -1:
            value = dem_mat[r.router_id][int(dest)] 
            charge += value 
    return charge

def computeModel(filename):

    with open(filename) as f:
        content = f.read()
    
    [nodes, edges] = content.split("edge", 1)
    lastNodeDescription = nodes.rsplit("node", 1)[1]
    nodeNumber = int(lastNodeDescription.split("id")[1].split('\n')[0].replace(' ','')) + 1

    edges = edges.split("edge")
    adjMat = np.zeros(dtype=np.uint8,shape=(nodeNumber, nodeNumber))
    for _,oneEdge in enumerate(edges):
        src = int(oneEdge.split("source")[1].split('\n')[0].replace(' ',''))
        dest = int(oneEdge.split("target")[1].split('\n')[0].replace(' ',''))
        adjMat[src][dest] = 1