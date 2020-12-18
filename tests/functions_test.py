import unittest
import math
from packages.functions import *
from packages import Router
from packages import Network
import numpy as np


class FunctionsTest(unittest.TestCase):
    AdjMatrix = np.array([
        [math.inf, 4, math.inf, math.inf, math.inf, math.inf],
        [4, math.inf, 3, 6, math.inf, 2],
        [math.inf, 3, math.inf, math.inf, 1, math.inf],
        [math.inf, 6, math.inf, math.inf, 2, math.inf],
        [math.inf, math.inf, 1, 2, math.inf, 5],
        [math.inf, 2, math.inf, math.inf, 5, math.inf]])

    DemandMatrix = 10 * np.ones(shape=np.shape(AdjMatrix))

    mNetwork = Network(AdjMatrix, DemandMatrix)
    mNetwork.nDijkstra()

    def test_isThereLink(self):
        self.assertEqual(isThereLink(self.mNetwork.Routers[0], (0, 1)), {1: [[1]]})
        self.assertEqual(isThereLink(self.mNetwork.Routers[0], (1, 4)), {})
        self.assertEqual(isThereLink(self.mNetwork.Routers[0], (2, 4)), {3: [[1, 2, 4, 3]], 4: [[1, 2, 4]]})

    def test_howManySP(self):
        self.assertEqual(howManySP(self.mNetwork.Routers[0], 1), 1)
        self.assertEqual(howManySP(self.mNetwork.Routers[0], 3), 2)

    """def test_loadLink(self):
        self.assertEqual( loadLink(self.mNetwork.Routers, self.DemandMatrix, (0,1)),10 )
       """


if __name__ == '__main__':
    unittest.main()
