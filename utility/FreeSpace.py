from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np
from PolyCurve import PolyCurve, plot_curves
POINT_PER_CELL = 100


class FreeSpace:
    def __init__(self, P, Q):
        self.P = P
        self.Q = Q

    @property
    def len_P(self):
        return len(self.P)-1

    @property
    def len_Q(self):
        return len(self.Q)-1

    def compute_freespace(self):
        x_d = self.P.parametric_distances[-1]
        xx = np.linespace(0, x_d, int(x_d * POINT_PER_CELL))
        x = self.P.parametric(xx)
        y_d = self.Q.parametric_distances[-1]
        yy = np.linespace(0, y_d, int(y_d * POINT_PER_CELL))
        y = self.Q.parametric(yy)

        distances = x.T[None, :, :] - y.T[:, None, :]
        return np.linalg.norm(distances, axis=2)