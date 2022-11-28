import numpy as np
from sympy import N, Point, Segment, Circle
from scipy.interpolate import interp1d


class PolyCurve:
    """
    Curve consisting of line segments.

    The sympy library is used for symbolic calculation, and therefore exact precision
    """

    def __init__(self, points):
        self._points = [Point(point) for point in points]
        self._remove_double_points()

        self._segments = [Segment(self[i], self[i + 1])
                          for i in range(len(self) - 1)]
        self._np_array = np.array(self._points)

    def _remove_double_points(self):
        """
        Remove directly following repeated points to prevent sympy from interpreting 
        them as points.
        """
        index = 1
        while index < len(self._points):
            if self._points[index - 1] == self._points[index]:
                del self._points[index]
            index += 1

    def __len__(self):
        return len(self._points)

    def __getitem__(self, index):
        return self._points[index]

    @property
    def segments(self):
        return self._segments

    @property
    def np_array(self):
        """
        Returns a numpy array of the points in the curve

        This can be used for easy broadcasting and matplotlib calculation
        """
        return self._np_array

    @property
    def coords(self):
        return self.np_array[:, 0], self.np_array[:, 1]

    def parametric(self, xs):
        """ Curve parametrization to [0, total_curve_length] """
        return interp1d(self.parametric_distances, self.coords)(xs)

    @property
    def parametric_distances(self):
        return np.cumsum(np.array([0] + [float(segment.length) for segment in self.segments]))


def plot_curves(P, Q, ax=None, markers=None):
    if ax is None:
        fig, ax_ = plt.subplots(1)
    else:
        ax_ = ax

    ax_.set_title("Curves P and Q")

    # plot P and Q
    P_line = ax_.plot(*P.coords, 'o-', color='blue', linewidth=2)
    Q_line = ax_.plot(*Q.coords, 'o-', color='red', linewidth=2)

    if markers is not None:
        marker_loc = np.array(
            [P.parametric(markers[0])] + [Q.parametric(markers[1])])

        # leash connection
        leash = ax_.plot(marker_loc[:, 0], marker_loc[:, 1], 'o-',
                         markerfacecolor='black', markersize=8, color='orange', linewidth=2)

        marker_dst = np.linalg.norm(marker_loc[0, :]-marker_loc[1, :])

        ax_.legend(('P', 'Q', f'Leash, length={round(marker_dst,2)}'))
    else:
        ax_.legend((P_line, Q_line), ('P', 'Q'))

    if ax is None:
        fig.show()


def plot_pq(Marker_P, Marker_Q):
    plot_curves(P, Q, markers=(Marker_P, Marker_Q))
