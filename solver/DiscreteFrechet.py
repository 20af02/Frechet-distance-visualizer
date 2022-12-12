from utility.FreeSpace import FreeSpace
from utility.PolyCurve import PolyCurve
import numpy as np

def calculate_discrete_frechet(P : PolyCurve, Q : PolyCurve):
    """
    calculate discrete frechet distance of 2 curves
    """
    ca = (np.ones((len(P), len(Q)), dtype=np.float64) * -1)

    def dist(i, j):
        return P[i].distance(Q[j])

    def c(i, j):
        if ca[i, j] > - 1:
            return ca[i, j]
        elif i == 0 and j == 0:
            ca[i, j] = dist(i, j)
        elif i > 0 and j == 0:
            ca[i, j] = max(c(i - 1, 0), dist(i, j))
        elif i == 0 and j > 0:
            ca[i, j] = max(c(0, j - 1), dist(i, j))
        elif i > 0 and j > 0:
            ca[i, j] = max(min(c(i - 1, j), c(i - 1, j - 1), c(i, j - 1)), dist(i, j))
        else:
            ca[i, j] = np.Infinity
        return ca[i, j]

    return c(len(P) - 1, len(Q) - 1)

