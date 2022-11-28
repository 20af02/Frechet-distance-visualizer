import numpy as np
import sympy
from sympy.geometry import Circle, Segment, Point

def freespace_distance(segment : Segment, point : Point, epsilon):
  """
  Computes the distance from the first coordinate of the segment to the nearest
  point on the segment that can be reached given the epsilon (leash lenght)

  Returns:
    -1 if no point can be reached given the leash
    0 if the first point on the segment can be reached
    distance > 0 otherwise
  """  

  # Check if the segment can be reached for this epsilon
  distance = segment.distance(point)
  if distance > epsilon:
    return -1, -1

  # Slow method using sympy functions
  # critical_points = Circle(point, epsilon).intersect(segment)
  # critical_distances = [segment.points[0].distance(p) for p in critical_points]

  # Faster custom method
  critical_distances = fast_segment_circle_intersection(segment, Circle(point, epsilon))

  if len(critical_distances) == 0:
    return 0, np.inf

  dist_min = 0 if segment.points[0].distance(point) <= epsilon else max(critical_distances)
  dist_max = np.inf if segment.points[1].distance(point) <= epsilon else min(critical_distances)

  return dist_min, dist_max

def fast_segment_circle_intersection(segment : Segment, circle : Circle):
  # Use ray circle intersection. Code based on https://stackoverflow.com/questions/1073336/circle-line-segment-collision-detection-algorithm
  d = segment.points[1] - segment.points[0]
  f = segment.points[0] - circle.center

  a = _dot(d, d)
  b = 2*_dot(f, d)
  c = _dot(f, f) - circle.radius ** 2

  discriminant = b ** 2 - 4 * a * c

  if discriminant < 0:
    # No intersection
    return []

  if discriminant == 0:
    t1 = -b / (2 * a)
    return [segment.length * t1] if 0 <= t1 <= 1 else []

  discriminant = sympy.sqrt(discriminant)

  intersections = []
  t1 = (-b - discriminant)/(2*a);
  t2 = (-b + discriminant)/(2*a);

  if t1 >= 0 and t1 <= 1:
    intersections += [segment.length * t1]

  if t2 >= 0 and t2 <= 1:
    intersections += [segment.length * t2]

  return intersections

def _dot(p, q):
  return p.x * q.x + p.y * q.y
