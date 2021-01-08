import unittest
from packages import engine, Network
import numpy as np
import math


class NormalNetwork(unittest.TestCase):
    """
    hope it doesnt fuck it up
    """
    AdjMatrix = np.array([[math.inf, 1, 2, math.inf],
                          [1, math.inf, math.inf, 3],
                          [2, math.inf, math.inf, 1],
                          [math.inf, 3, 1, math.inf]])
    DemandMatrix = np.array([[0, 6, 2, 0],
                             [1, 0, 0, 4],
                             [2, 0, 0, 4],
                             [0, 6, 4, 0]])
    mNetwork = Network(AdjMatrix, DemandMatrix)

    def test_engine(self):
        # CorrectedNetwork = engine(self.mNetwork)
        # self.assertFalse(CorrectedNetwork.isCongested())
        pass  # TODO :: decomment tests once implemented


class OverloadedNetwork(unittest.TestCase):
    """
    hope it fucks it up
    """
    AdjMatrix = np.array([[math.inf, 1, 2, math.inf],
                          [1, math.inf, math.inf, 3],
                          [2, math.inf, math.inf, 1],
                          [math.inf, 3, 1, math.inf]])
    DemandMatrix = np.array([[0, 6, 2, 0],
                             [1, 0, 0, 4],
                             [2, 0, 0, 4],
                             [0, 6, 4, 0]])  # TODO :: put am Overloaded Network here
    mNetwork = Network(AdjMatrix, DemandMatrix)

    def test_engine(self):
        # CorrectedNetwork = engine(self.mNetwork)
        # self.assertFalse(CorrectedNetwork.isCongested())
        pass


if __name__ == '__main__':
    unittest.main()
