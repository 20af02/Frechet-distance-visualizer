import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from utility.PolyCurve import PolyCurve
from utility.FreeSpace import FreeSpace, POINT_PER_CELL

def plot_custom_curves(P : PolyCurve, Q : PolyCurve, ax=None, markers=None):
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

# Plot the freespace of 2 curves
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
    
# read from file
def read_curves():
    P_points, Q_points = [], []
    with open('P_points.txt') as f:
        for line in f:
            # each line is of form x,y
            P_points.append(tuple(map(float, line.split(','))))
    with open('Q_points.txt') as f:
        for line in f:
            # each line is of form x,y
            Q_points.append(tuple(map(float, line.split(','))))

    # return poly curves
    return PolyCurve(P_points), PolyCurve(Q_points)

# Plot the 2 curves from stored files
def plot_file_curve():
    P, Q = read_curves()
    plot_custom_curves(P, Q)

def plot_file_freespace():
    P, Q = read_curves()
    plot_freespace(P, Q, 0.1)
