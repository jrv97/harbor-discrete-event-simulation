import random
import matplotlib.pyplot as plt
from numpy import histogram, digitize, linspace
from math import floor
import numpy


class PdfGrapher:
    """
    Graphs an histogram of a series of points.
    That way we can see the distribution.
    """

    def __init__(self, bins, list_of_names, list_of_lims):
        # make n subplots
        self.graph, self.axes = plt.subplots(
            len(list_of_names), sharex=True, sharey=True)

        # name the subplots
        for i in range(len(self.axes)):
            self.axes[i].set_title(list_of_names[i])

        # set limits for each axis
        self.xranges = []
        self.yranges = []
        for i, (xrange, yrange) in enumerate(list_of_lims):
            self.xranges.append(xrange)
            self.yranges.append(yrange)
            self.axes[i].set_xlim(xrange[0], xrange[1])
            self.axes[i].set_ylim(yrange[0], yrange[1])

        # set histogram for each axis
        self.hists = []
        for i in range(len(self.axes)):
            self.hists.append([0] * bins)

        plt.ion()
        plt.draw()

        # attribute to keep points updated
        self.points = [None] * len(list_of_names)

    def graph_points(self):
        for i, point in enumerate(self.points):
            if point:
                index, x_axis_low, x_axis_high = self._get_point_initial_x_axis(
                    point, i)
                self.axes[i].bar([x_axis_low], self.hists[i]
                                 [index], abs(x_axis_high - x_axis_low))
                #self.graph.plot([index], [self.hist[index]])
        plt.draw()
        plt.pause(0.10)

    def update(self, index, point):
        self.points[index] = point
        i, _, _ = self._get_point_initial_x_axis(point, index)
        self.hists[index][i] += 1
        self.graph_points()

    def _get_point_initial_x_axis(self, point, i):
        """Returns position of given point

        Arguments:
            point {float} -- point to get index for

        Returns:
            (bin_index, xaxis_low,xaxis_high) -- {(int,float,float)}
        """
        bins = linspace(self.xranges[i][0],
                        self.xranges[i][1], len(self.hists[i]) + 1)
        a = digitize([point], bins)
        return (a[0] - 1, bins[a[0] - 1], bins[a[0]])


def uniform(lower, upper):
    while True:
        yield random.uniform(lower, upper)


def normal(mu, sigma):
    while True:
        yield random.normalvariate(0, 1)


def exponential(lamb):
    while True:
        yield random.expovariate(lamb)


list_of_distribution = [
    'Tanker arrivals',
    'Berthing time',
    'Deberthing time',
    'Solo trip time',
    'S-tanker load time',
    'M-tanker load time',
    'L-tanker load time',
]

list_of_lims = [
    ((0, 30), (0, 30)),
    ((0, 30), (0, 30)),
    ((0, 30), (0, 30)),
    ((0, 30), (0, 30)),
    ((0, 30), (0, 30)),
    ((0, 30), (0, 30)),
    ((0, 30), (0, 30))
]


# grapher = PdfGrapher(
#     bins=200, list_of_names=list_of_distribution, list_of_lims=list_of_lims)

# while True:
#     grapher.update(0, exponential(1/8).__next__())
#     grapher.update(1, exponential(2).__next__())
#     grapher.update(2, exponential(1).__next__())
#     grapher.update(3, exponential(1/4).__next__())
#     grapher.update(4, uniform(9, 1).__next__())
#     grapher.update(5, uniform(12, 2).__next__())
#     grapher.update(6, uniform(18, 3).__next__())
