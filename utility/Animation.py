import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PatchCollection
from scipy.interpolate import interp1d
from functools import partial
from solver.FreeSpaceContinuous import FreeSpaceContinuous
from utility.PolyCurve import PolyCurve
from utility.Color import COLOR_BLUE, COLOR_GREEN, GRID_GRANULARITY
from utility.Plotter import plot_freespace, plot_curves
from IPython.display import HTML

EPSILON = 1000
N_FRAMES = 100

def animate_solution(P : PolyCurve, Q : PolyCurve, eps=1000):
    freespace = FreeSpaceContinuous(P, Q)

    #assert freespace.continuous_path_exists(eps), 'Path does not exist'

    plt.rcParams['figure.figsize'] = [18, 5]

    fig, ax = plt.subplots(1, 2)

    path = np.array(freespace.find_continous_path(eps))

    path_distances = np.cumsum(np.array([0] + [np.linalg.norm(x - y) for x, y in zip(path[1:], path[:-1])]))

    point_on_path = interp1d(path_distances, path.T)(np.linspace(0, path_distances[-1], N_FRAMES))
    plot_freespace(P, Q, eps, ax[0])
    plot_curves(P, Q, ax[1])

    line_path, = ax[0].plot([], [], lw=2, color=COLOR_BLUE)
    line_leash, = ax[1].plot([], [], lw=3, color=COLOR_GREEN)
    
    ani = FuncAnimation(fig, partial(update, point_on_path=point_on_path, line_path=line_path, \
                        line_leash=line_leash, P=P, Q=Q), frames=np.arange(N_FRAMES), blit=True)
    
    plt.close(fig)

    return HTML(ani.to_html5_video())

def plot_leash(frame, point_on_path, line_leash, P, Q):
  cur = point_on_path[:, frame]

  px = P.parametric(cur[0])
  py = Q.parametric(cur[1])
  line_leash.set_data([px[0], py[0]], [px[1], py[1]])

  return line_leash

def plot_path(frame, point_on_path, line_path):
  cur = point_on_path[:, :frame] * GRID_GRANULARITY

  line_path.set_data(cur[0, :], cur[1, :]) 

  return line_path


def update(frame, point_on_path, line_path, line_leash, P, Q):
  return [plot_path(frame, point_on_path, line_path), plot_leash(frame, point_on_path, line_leash, P, Q)]


