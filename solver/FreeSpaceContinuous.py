import itertools as it
import numpy as np
from solver.FreeSpaceDistance import freespace_distance
from utility.FreeSpace import FreeSpace

class FreeSpaceContinuous(FreeSpace):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    # For visualisation purposes, 
    self.callback_continuous_explore = []

  def explore_continuous_freespace(self, epsilon):
    """
    Explores the freespace, checking if each cell can be reached in
    the strong Fréchet distance.
    """

    cell_entrance_coordinates = -np.ones((self.len_P, self.len_Q, 2)) 
    cell_entrance_coordinates[0, 0, :] = np.zeros(2) 

    for x, y in it.product(range(self.len_P), range(self.len_Q)):
      start_coords = cell_entrance_coordinates[x, y]

      # Optimization, only compute distances if we can reach this cell
      if all(start_coords < 0):
        continue

      dy, dy_max = freespace_distance(self.Q.segments[y],
                                      self.P[x + 1],
                                      epsilon)
      dx, dx_max = freespace_distance(self.P.segments[x],
                                      self.Q[y + 1],
                                      epsilon)
      # Check starting from left going up
      if start_coords[1] != -1 and dx >= 0 and y < self.len_Q - 1:
        cell_entrance_coordinates[x, y + 1, 0] = dx
      # If this is not possible, go down to up
      elif start_coords[0] != -1 and dx >= 0 and y < self.len_Q - 1 and start_coords[0] < dx_max:
        cell_entrance_coordinates[x, y + 1, 0] = max(start_coords[0], dx)
      
      # Check starting from down going right
      if start_coords[0] != -1 and dy >= 0 and x < self.len_P - 1:
        cell_entrance_coordinates[x + 1, y, 1] = dy
      # If this is not possible, go left to right
      elif start_coords[1] != -1 and dy >= 0 and x < self.len_P - 1 and start_coords[1] < dy_max:
        cell_entrance_coordinates[x + 1, y, 1] = max(start_coords[1], dy)

      self._callback_continuous(x, y, cell_entrance_coordinates)

    return cell_entrance_coordinates
              
  def _callback_continuous(self, x, y, cell_entrance_coordinates):
    for f in self.callback_continuous_explore:
      f(x, y, cell_entrance_coordinates.copy())

  def continuous_path_exists(self, epsilon):
    """
    Checks if a path exists between the start and the end of the freespace given
    'continuous' constraints
    """
    # Check if the start and end points can be reached
    if self.P[0].distance(self.Q[0]) > epsilon or \
       self.P[-1].distance(self.Q[-1]) > epsilon:
      return False

    return any(self.explore_continuous_freespace(epsilon)[-1, -1] >= 0)

  def find_continous_path(self, epsilon):
    if not self.continuous_path_exists(epsilon):
      return False

    cell_entrance_coordinates = self.explore_continuous_freespace(epsilon)

    p_distances = self.P.parametric_distances
    q_distances = self.Q.parametric_distances

    # Define a polycurve in the continous space to find the path
    inversed_path = [(p_distances[-1], q_distances[-1])]
    x = self.len_P - 1
    y = self.len_Q - 1
    
    while x != 0 or y != 0:
      if y > 0 and cell_entrance_coordinates[x, y, 0] >= 0:
        p = (p_distances[x] + cell_entrance_coordinates[x, y, 0], q_distances[y])
        inversed_path.append(p)
        y -=1
      elif x > 0 and cell_entrance_coordinates[x, y, 1] >= 0:
        p = (p_distances[x], q_distances[y] + cell_entrance_coordinates[x, y, 1])
        inversed_path.append(p)
        x -=1
      else:
        assert False, 'Something went wrong'
    path = inversed_path[::-1]
    path = [(0, 0)] + path
    return path

  def calculate_distance(self, tolerance=0.001, debug=False):

    # Exponential search step
    epsilon_max = 2
    epsilon_min = 0
    while not self.continuous_path_exists(epsilon_max):
      epsilon_min = epsilon_max
      epsilon_max *= epsilon_max
      if debug:
        print(f'exponential searching, range between {epsilon_min}, {epsilon_max}')

    while epsilon_max - epsilon_min > tolerance:
      if debug:
        print(f'binary searching, range between {epsilon_min}, {epsilon_max}')
      center = (epsilon_max + epsilon_min) / 2
      if self.continuous_path_exists(center):
        epsilon_max = center
      else:
        epsilon_min = center

    return epsilon_max
