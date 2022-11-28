import sys
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import functools
from sympy import N, Segment, Point, Circle
import sympy
from ipywidgets import interactive, RadioButtons
import itertools as it
from typing import Tuple
from matplotlib.colors import ListedColormap
from PolyCurve import PolyCurve
from plot import plot_curves

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import functools
from sympy import N, Segment, Point, Circle
import sympy
from ipywidgets import interactive, RadioButtons
import itertools as it
from typing import Tuple
from matplotlib.colors import ListedColormap


# read from file

class read_poly_curve:
    def __init__(self):
        self.P_points = []
        self.Q_points = []

    def read_curves(self):
        with open('P_points.txt') as f:
            for line in f:
                # each line is of form x,y
                self.P_points.append(tuple(map(float, line.split(','))))
        with open('Q_points.txt') as f:
            for line in f:
                # each line is of form x,y
                self.Q_points.append(tuple(map(float, line.split(','))))

        # return poly curves
        return PolyCurve(self.P_points), PolyCurve(self.Q_points)
