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

import arcade

sys.coinit_flags = 2


class MainWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Drawing Example")

        self.x = 150
        self.y = 150
        self.P_points = []
        self.Q_points = []
        self.is_drawing_line_one = True
        self.is_running = True

    def on_draw(self):
        arcade.start_render()
        if self.is_drawing_line_one:
            arcade.draw_line_strip(
                self.P_points, arcade.color.ALABAMA_CRIMSON, 2)
        else:
            arcade.draw_circle_filled(self.x, self.y, 15, arcade.color.BLUE)
        # draw points in pointlist points
        for point in self.P_points:
            arcade.draw_circle_filled(
                point[0], point[1], 15, arcade.color.BLUE)
        # draw lines between points
        for i in range(len(self.P_points)-1):
            arcade.draw_line(self.P_points[i][0], self.P_points[i][1],
                             self.P_points[i+1][0], self.P_points[i+1][1], arcade.color.BLUE, 2)
        for point in self.Q_points:
            arcade.draw_circle_filled(
                point[0], point[1], 15, arcade.color.ALABAMA_CRIMSON)
        # draw lines between points
        for i in range(len(self.Q_points)-1):
            arcade.draw_line(self.Q_points[i][0], self.Q_points[i][1],
                             self.Q_points[i+1][0], self.Q_points[i+1][1], arcade.color.AMBER, 2)

    def on_mouse_motion(self, x, y, dx, dy):
        self.x = x
        self.y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.P_points.append((x, y))
        if button == arcade.MOUSE_BUTTON_RIGHT:
            # switch
            if self.is_drawing_line_one:
                self.is_drawing_line_one = False
            self.Q_points.append((x, y))
        # end
        if button == arcade.MOUSE_BUTTON_MIDDLE:
            self.is_running = False
            # Save points to file
            with open('P_points.txt', 'w') as f:
                for item in self.P_points:
                    # write as x, y\n ...
                    f.write("%s,%s\n" % (item[0], item[1]))

            with open('Q_points.txt', 'w') as f:
                for item in self.Q_points:
                    f.write("%s,%s\n" % (item[0], item[1]))
            self.close()


MainWindow()

arcade.run()
