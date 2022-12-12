from utility.FreeSpace import FreeSpace
from utility.PolyCurve import PolyCurve
class FreeSpaceDiscrete(FreeSpace):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def discrete_frechet(P : PolyCurve, Q : PolyCurve):
        """
        calculate discrete frechet distance of 2 curves
        """

        # init
        n = len(P)
        m = len(Q)
        D = [[0 for i in range(m)] for j in range(n)]

        # calculate distance matrix
        for i in range(n):
            for j in range(m):
                D[i][j] = P[i].distance(Q[j])

        # calculate discrete frechet distance
        for i in range(1, n):
            for j in range(1, m):
                D[i][j] = max(D[i-1][j], D[i][j-1], D[i-1][j-1] + D[i][j])

        return D[n-1][m-1]

