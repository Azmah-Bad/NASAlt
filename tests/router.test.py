import unittest
from packages import Router
import numpy as np
import math


class RouterTest(unittest.TestCase):
    RouterID = 0
    AdjMatrix = np.array([[math.inf, 1, 2, math.inf],
                          [1, math.inf, math.inf, 3],
                          [2, math.inf, math.inf, 1],
                          [math.inf, 3, 1, math.inf]])

    AdjMatrixBi = np.array([[math.inf, 1, 2,        5],
                            [5, math.inf, math.inf, 3],
                            [1, math.inf, math.inf, 1],
                            [math.inf, 3, 1, math.inf]])

    DemandMatrix = np.array([[0, 1, 2, 0],
                             [1, 0, 0, 3],
                             [2, 0, 0, 1],
                             [0, 3, 1, 0]])

    def test_dijkstra(self):
        mRouter = Router(self.RouterID, self.AdjMatrix, self.DemandMatrix)
        mRouter.dijkstra()
        self.assertEqual(mRouter.shortest_paths[1], ([1], 1))
        self.assertEqual(mRouter.shortest_paths[2], ([2], 2))
        self.assertEqual(mRouter.shortest_paths[3], ([2, 3], 3))

    def test_dijkstra_unequal_bidirectional_weight(self):
        mRouter = Router(self.RouterID, self.AdjMatrixBi, self.DemandMatrix)
        mRouter.dijkstra()
        self.assertEqual(mRouter.shortest_paths[1], ([1], 1))
        self.assertEqual(mRouter.shortest_paths[2], ([2], 2))
        self.assertEqual(mRouter.shortest_paths[3], ([2, 3], 3))


if __name__ == '__main__':
    unittest.main()
