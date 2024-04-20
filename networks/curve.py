class Curve:
    def __init__(self, points):
        self.points = points  # list of tuples (x1, y1, z1) in order

    def curve(points, resolution=40, debug=False):
        """
        Returns a 3d curve.

        https://stackoverflow.com/questions/18962175/spline-interpolation-coefficients-of-a-line-curve-in-3d-space

        Args:
            points (np.array): Points where the curve should pass in order.
            resolution (int, optional): Number of points to compute. Defaults to 40.
            debug (bool, optional): Visual. Defaults to False.

        Returns:
            tuple: Tuple of list of each coordinate.
        """
        # Remove duplicates.
        points = tuple(map(tuple, points))
        points = sorted(set(points), key=points.index)

        x_sample = []
        y_sample = []
        z_sample = []

        for i in range(len(points)):
            x_sample.append(points[i][0])
            z_sample.append(points[i][1])
            y_sample.append(points[i][2])

        x_sample = np.array(x_sample)
        y_sample = np.array(y_sample)
        z_sample = np.array(z_sample)

        tck, u = interpolate.splprep([x_sample, y_sample, z_sample], s=2, k=2)
        x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
        u_fine = np.linspace(0, 1, number_true_pts)
        x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)

        if debug:
            fig2 = plt.figure(2)
            ax3d = fig2.add_subplot(111, projection="3d")
            ax3d.plot(x_sample, y_sample, z_sample, "r*")
            ax3d.plot(x_knots, y_knots, z_knots, "go")
            ax3d.plot(x_fine, y_fine, z_fine, "r")
            fig2.show()
            plt.show()

        x = x_fine.tolist()
        z = y_fine.tolist()
        y = z_fine.tolist()

        for i in x:
            i = round(i)
        for i in y:
            i = round(i)
        for i in z:
            i = round(i)

        return x, y, z