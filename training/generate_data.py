# generate data
import random

import numpy as np
from packages import Network

LINKS_COUNT = 12
THRESHOLD = 80


def generateLoadMatrix():
    """
    :return: a random congestion matrix that is congested
    """
    LoadMatrix = np.random.rand(LINKS_COUNT, LINKS_COUNT) * 100
    if not np.where(LoadMatrix > THRESHOLD):
        LoadMatrix[random.choice(range(LINKS_COUNT)), random.choice(range(LINKS_COUNT))] = random.choice(range(
            THRESHOLD, 100))
    return LoadMatrix


def generateCongestedNetwork():
    AdjacencyMatrix = None  # TODO get this from france.gml
    raise NotImplementedError
