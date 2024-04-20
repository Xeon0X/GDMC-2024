import numpy as np
from scipy import interpolate


class Curve:
    def __init__(self, target_points):
        # list of points to [(x1, y1, z1), (...), ...]
        self.target_points = target_points
        self.computed_points = []

    def compute_curve(self, resolution=40):
        """
        Fill self.computed_points with a list of points that approximate a smooth curve following self.target_points.

        https://stackoverflow.com/questions/18962175/spline-interpolation-coefficients-of-a-line-curve-in-3d-space

        Args:
            points (np.array): Points where the curve should pass in order.
            resolution (int, optional): Total number of points to compute. Defaults to 40.
        """
        # Remove duplicates. Curve can't intersect itself
        points = tuple(map(tuple, np.array(self.target_points)))
        points = sorted(set(points), key=points.index)

        # Change coordinates structure to (x1, x2, x3, ...), (y1, y2, y3, ...) (z1, z2, z3, ...)
        coords = np.array(points, dtype=np.float32)
        x = coords[:, 0]
        y = coords[:, 1]
        z = coords[:, 2]

        # Compute
        tck, u = interpolate.splprep([x, y, z], s=2, k=2)
        x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
        u_fine = np.linspace(0, 1, resolution)
        x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)

        x_rounded = np.round(x_fine).astype(int)
        y_rounded = np.round(y_fine).astype(int)
        z_rounded = np.round(z_fine).astype(int)

        self.computed_points = [(x, y, z) for x, y, z in zip(
            x_rounded, y_rounded, z_rounded)]
