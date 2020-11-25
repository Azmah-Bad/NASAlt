#!/usr/bin/env python3

from random import *

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