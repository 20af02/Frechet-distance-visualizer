import itertools as it
import numpy as np
from solver.FreeSpaceDistance import freespace_distance
from utility.FreeSpace import FreeSpace


class FreeSpaceWeak(FreeSpace):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    # For visualisation purposes, 
    self.callbacks_weak_explore = []

  def check_weak_transition(self, epsilon, x, y, dx, dy):
    """
    Checks if a transition can be made between two cells of the freespace for
    the weak variant of the Fréchet distance
    """
    assert -1 <= dx <= 1 and -1 <= dy <= 1 and abs(dx) + abs(dy) == 1, \
      'Only transitions to the horizontal or vertical neighbor can be made'

    if 0 <= x + dx < self.len_P and 0 <= y + dy < self.len_Q:
      if dx != 0:
        return self.Q.segments[y].distance(self.P[x + dx]) <= epsilon
      if dy != 0:
        return self.P.segments[x].distance(self.Q[y + dy]) <= epsilon

    return False

  def explore_weak_freespace(self, epsilon, x=0, y=0, visited=None):
    """
    Explores the freespace, recursively checking if each cell can be reached in
    the weak Fréchet distance.
    
    :args
      visited: Array of cells that have already been explored
      x, y: The coordinates of the cell from which to explore further

    :returns
      True if the top rightmost cell in the freespace can be reached, else False
    """

    # Creates the 'closed list' of cells already visited if none are provided
    if visited is None:
      visited = np.zeros((self.len_P, self.len_Q))

    if visited[x, y]:
      return False
    else:
      visited[x, y] = True

    # Provide callback for visualisation
    self._callback_weak(x, y, visited)

    # Return if the final cell is reached
    if x == self.len_P - 1 and y == self.len_Q - 1:
      return True

    # Check if the neighboring cells can be reached, in the order:
    # right, top, left, bottom
    if self.check_weak_transition(epsilon, x, y, 1, 0) and self.explore_weak_freespace(epsilon, x + 1, y, visited):
        return True
    if self.check_weak_transition(epsilon, x, y, 0, 1) and self.explore_weak_freespace(epsilon, x, y + 1, visited):
        return True
    if self.check_weak_transition(epsilon, x, y, -1, 0) and self.explore_weak_freespace(epsilon, x - 1, y, visited):
        return True
    if self.check_weak_transition(epsilon, x, y, 0, -1) and self.explore_weak_freespace(epsilon, x, y - 1, visited):
        return True

    return False

  def _callback_weak(self, x, y, visited):
    for f in self.callbacks_weak_explore:
      f(x, y, visited.copy())

  def weak_path_exists(self, epsilon):
    """
    Checks if a path exists between the start and the end of the freespace given
    'weak' constraints
    """
    # Check if the start and end points can be reached
    if self.P[0].distance(self.Q[0]) > epsilon or \
       self.P[-1].distance(self.Q[-1]) > epsilon:
      return False

    return self.explore_weak_freespace(epsilon)

  def compute_minimum_distance(self, debug=False):
    critical_values = list()

    for x, y in it.product(range(self.len_P), range(self.len_Q)):
      critical_values += [self.Q.segments[y].distance(self.P.segments[x].points[0])]
      critical_values += [self.Q.segments[y].distance(self.P.segments[x].points[1])]
      critical_values += [self.P.segments[x].distance(self.Q.segments[y].points[0])]
      critical_values += [self.P.segments[x].distance(self.Q.segments[y].points[1])]

    critical_values = sorted(list(set(critical_values)))

    i = 0
    while True:
      if debug:
        print(f'exp {i} of {len(critical_values)}')
      if self.weak_path_exists(critical_values[i]):
        break
      i = i**2 if i > 1 else i + 1
      if i > len(critical_values):
        i = len(critical_values)
        break

    if i == 0:
      return critical_values[i]
  
    min_range = int(np.log2(i))
    while i - min_range > 1:
      center = int((min_range + i) / 2)
      if debug:
        print(f'{i}, min range {min_range}, {critical_values[center]}, {self.weak_path_exists(critical_values[center])}')
      if self.weak_path_exists(critical_values[center]):
        i = center
      else:
        min_range = center

    return critical_values[i]
