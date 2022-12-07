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
        Remove consecutive repeated points
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
        
    """
    Return a compressed curve by dividing points by compression_ratio
    """
    def compressed_curve(self, compression_ratio):
        new_points = []
        for point in self._points:
            new_points.append(point / compression_ratio)
            print(point / compression_ratio)
        return PolyCurve(new_points)

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


    """ Cumulative segments' length """
    @property
    def parametric_distances(self):
        return np.cumsum(np.array([0] + [float(segment.length) for segment in self.segments]))
