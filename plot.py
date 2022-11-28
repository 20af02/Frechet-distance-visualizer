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

# takes two PolyCurves P and Q


# plot freespace


def plot_freespace(p, q, eps, ax=None, markers=None):
    if ax is None:
        fix, _ax = plt.subplots(1)
    else:
        _ax = ax
      # @TODO finish this function
