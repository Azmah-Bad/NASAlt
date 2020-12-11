import unittest
import math
from packages.functions import *
from packages import Router
from packages import Network
import numpy as np


class FunctionsTest(unittest.TestCase):
    AdjMatrix = np.array([
        [math.inf,4,math.inf,math.inf,math.inf,math.inf],
        [4,math.inf,3,6,math.inf,2],
        [math.inf,3,math.inf,math.inf,1,math.inf],
        [math.inf,6,math.inf,math.inf,2,math.inf],
        [math.inf,math.inf,1,2,math.inf,5],
        [math.inf,2,math.inf,math.inf,5,math.inf]])

    DemandMatrix = np.random.randint(70, size=(6,6))

    mNetwork = Network(AdjMatrix, DemandMatrix)

    def test_isThereLink(self):
        self.assertEqual(isThereLink(self.mNetwork.Routers[0], (0,1) ), 1)
        self.assertEqual(isThereLink(self.mNetwork.Routers[0], (0,4) ), -1)


if __name__ == '__main__':
    unittest.main()
