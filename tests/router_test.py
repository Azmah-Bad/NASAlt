import unittest
from packages import Router
import numpy as np
import math
import time


class RouterTest(unittest.TestCase):
    RouterID = 0
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

    def test_dijkstra(self):
        mRouter = Router(self.RouterID, self.AdjMatrix, self.DemandMatrix)
        start = time.time()
        mRouter.dijkstra()
        end = time.time()
        print(f"calculated Dijkstra in {end - start}")
        self.assertEqual(mRouter.shortest_paths[1], ([1], 1))
        self.assertEqual(mRouter.shortest_paths[2], ([2], 2))
        self.assertEqual(mRouter.shortest_paths[3], ([2, 3], 3))

    def test_dijkstra_unequal_bidirectional_weight(self):
        mRouter = Router(self.RouterID, self.AdjMatrixBi, self.DemandMatrix)
        start = time.time()
        mRouter.dijkstra()
        end = time.time()
        print(f"calculated Dijkstra in {end-start}")
        self.assertEqual(mRouter.shortest_paths[1], ([1], 1))
        self.assertEqual(mRouter.shortest_paths[2], ([2], 2))
        self.assertEqual(mRouter.shortest_paths[3], ([2, 3], 3))

    def test_dijkstra_from_b(self):
        mRouter = Router(1, self.AdjMatrix, self.DemandMatrix)
        start = time.time()
        mRouter.dijkstra()
        end = time.time()
        print(f"calculated Dijkstra in {end - start}")
        self.assertEqual(mRouter.shortest_paths[0], ([0], 1))
        self.assertEqual(mRouter.shortest_paths[2], ([0, 2], 3))
        self.assertEqual(mRouter.shortest_paths[3], ([3], 3))

    def test_getNeighbors(self):
        mRouter = Router(self.RouterID, self.AdjMatrix, self.DemandMatrix)
        self.assertListEqual(mRouter.neighbors, [1, 2])


if __name__ == '__main__':
    unittest.main()
