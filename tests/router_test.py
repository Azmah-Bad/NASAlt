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

    AdjMatrix2 = np.array([
        [math.inf, 4, math.inf, math.inf, math.inf, math.inf],
        [4, math.inf, 3, 6, math.inf, 2],
        [math.inf, 3, math.inf, math.inf, 1, math.inf],
        [math.inf, 6, math.inf, math.inf, 2, math.inf],
        [math.inf, math.inf, 1, 2, math.inf, 5],
        [math.inf, 2, math.inf, math.inf, 5, math.inf]
    ])

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
        # print(mRouter.shortest_paths)
        self.assertDictEqual(mRouter.shortest_paths,
                             {0: ([[]], 0), 1: ([[1]], 1.0), 2: ([[2]], 2.0), 3: ([[2, 3]], 3.0)})

    def test_dijkstra_unequal_bidirectional_weight(self):
        mRouter = Router(self.RouterID, self.AdjMatrixBi, self.DemandMatrix)
        start = time.time()
        mRouter.dijkstra()
        end = time.time()
        print(f"calculated Dijkstra in {end - start}")
        # print(mRouter.shortest_paths)
        self.assertDictEqual(mRouter.shortest_paths,
                             {0: ([[]], 0), 1: ([[1]], 1.0), 2: ([[2]], 2.0), 3: ([[2, 3]], 3.0)})

    def test_dijkstra_from_b(self):
        mRouter = Router(1, self.AdjMatrix, self.DemandMatrix)
        start = time.time()
        mRouter.dijkstra()
        end = time.time()
        print(f"calculated Dijkstra in {end - start}")
        self.assertDictEqual(mRouter.shortest_paths, mRouter.shortest_paths)

    def test_getNeighbors(self):
        mRouter = Router(self.RouterID, self.AdjMatrix, self.DemandMatrix)
        self.assertListEqual(mRouter.neighbors, [1, 2])

    def test_dijkstra2(self):
        CorrectOutput = {0: ([[]], 0), 1: ([[1]], 4.0), 2: ([[1, 2]], 7.0), 3: ([[1, 3], [[1, 2, 4, 3]]], 10.0), 4: ([[1, 2, 4]], 8.0), 5: ([[1, 5]], 6.0)}
        mRouter = Router(0, self.AdjMatrix2, self.DemandMatrix)
        mRouter.dijkstra()
        self.assertDictEqual(mRouter.shortest_paths, CorrectOutput)

    def test_2equal_links(self):
        AdjMatrix = np.array([[math.inf, 1, 1, math.inf],
                              [1, math.inf, math.inf, 1],
                              [1, math.inf, math.inf, 1],
                              [math.inf, 1, 1, math.inf]])
        mRouter = Router(0, AdjMatrix, self.DemandMatrix)
        mRouter.dijkstra()
        self.assertDictEqual(mRouter.shortest_paths, {0: ([[]], 0), 1: ([[1]], 1.0), 2: ([[2]], 1.0), 3: ([[1, 3], [[2, 3]]], 2.0)})

    def test_alternative(self):
        mRouter = Router(2, self.AdjMatrix2, self.DemandMatrix)
        alter = mRouter.restrainedDijkstra([[2,1]])
        self.assertDictEqual(alter, 0: ([4, 5, 1, 0], 12.0), 2: ([], 0), 1: ([4, 5, 1], 8.0), 3: ([4, 3], 3.0), 4: ([4], 1.0), 5: ([4, 5], 6.0)})
        self.assertDictEqual(mRouter.getMinIncrements(alter)), 0: 5.0, 1: 5.0, 2: 0, 3: 0.0, 4: 0.0, 5: 1.0})



if __name__ == '__main__':
    unittest.main()
