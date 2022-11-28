from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np
from utility.PolyCurve import PolyCurve, POINT_PER_CELL
from utility.FreeSpace import FreeSpace


def plot_freespace(P : PolyCurve, Q : PolyCurve, eps, ax=None, markers=None):
    if ax is None:
        fig, ax_ = plt.subplots(1)
    else:
        ax_ = ax

    ax_.set_title("Freespace of curves P and Q")

    ax_.set_xlim([0, P.parametric_distances[-1] * POINT_PER_CELL])
    ax_.set_ylim([0, Q.parametric_distances[-1] * POINT_PER_CELL])

    space_grid = FreeSpace(P, Q).compute_freespace()

    ax_.imshow(space_grid <= eps, cmap=ListedColormap(
        ['grey', 'white']), origin='lower', vmin=0, vmax=1)

    if markers is not None:
        marker_xy = (markers[0] * POINT_PER_CELL, markers[1] * POINT_PER_CELL)
        ax_.scatter(*marker_xy, color='black')

    ax_.grid(color='greay', linestyle='-', linewidth=0.5)

    x_ticks = P.parametric_distances[1:-1] * POINT_PER_CELL
    ax_.set_xticks(x_ticks)
    ax_.set_xticks([round(x, 2) for x in x_ticks], rotation=45)
    ax_.set_xlabel('Distance on curve P')
    ax_.xaxis.label.set_color('blue')
    ax_.spines['bottom'].set_color('blue')
    ax_.spines['bottom'].set_linewidth(2)

    y_ticks = Q.parametric_distances[1:-1] * POINT_PER_CELL
    ax_.set_yticks(y_ticks)
    ax_.set_yticks([round(y, 1) for y in y_ticks])
    ax_.set_ylabel('Distance on curve Q')
    ax_.yaxis.label.set_color('red')
    ax_.spines['left'].set_color('red')
    ax_.spines['left'].set_linewidth(2)

    if ax is None:
        fig.show()
