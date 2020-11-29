import unittest
from packages import Network
import math
import numpy as np


class NetworkTest(unittest.TestCase):
    AdjMatrix = np.array([[math.inf, 1, 2, math.inf],
                          [1, math.inf, math.inf, 3],
                          [2, math.inf, math.inf, 1],
                          [math.inf, 3, 1, math.inf]])

    AdjMatrixBi = np.array([[math.inf, 1, 2, 5],
                            [5, math.inf, math.inf, 3],
                            [1, math.inf, math.inf, 1],
                            [math.inf, 3, 1, math.inf]])

    DemandMatrix = np.array([[0, 1, 2, 0],
                             [1, 0, 0, 3],
                             [2, 0, 0, 1],
                             [0, 3, 1, 0]])
    mNetwork = Network(AdjMatrix, DemandMatrix)

    def test_constructor(self):
        ID_list = [router.ID for router in self.mNetwork.Routers]
        self.assertListEqual(ID_list, list(range(4)))
        self.assertListEqual(self.mNetwork.getRouterByID(0).neighbors, [1, 2])

    def test_getRouterByID(self):
        self.assertEqual(self.mNetwork.getRouterByID(0).ID, 0)


if __name__ == '__main__':
    unittest.main()
