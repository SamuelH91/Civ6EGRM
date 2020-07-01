from utils.hexagon import Hexagon
from matplotlib.collections import PatchCollection
from matplotlib.collections import LineCollection
import numpy as np

Y0 = np.sqrt(3)/2
Y1 = 1/np.sqrt(3)
Y2 = 1/2/np.sqrt(3)
X1 = 0.0
X2 = 0.5


class HexGrid:
    def __init__(self, x, y, scale=1.0, outsideBordersOnly=False):
        self.X = x
        self.Y = y
        self.collection = None
        self.patches_list = []
        self.lines_list = []
        self.neigbours_list = []
        self.outsideBordersOnly = outsideBordersOnly
        for yy in range(y):
            xOffset = X2 if yy % 2 == 1 else X1
            yval = yy*Y0
            for xx in range(x):
                self.patches_list.append(Hexagon(np.array([[xx + xOffset], [yval]]), scale))
        if self.outsideBordersOnly:
            self.lines_list = np.zeros((6*self.X*self.Y, 2, 2))
            for ii, patch in enumerate(self.patches_list):
                xy = patch.get_xy()
                for jj in range(6):
                    self.lines_list[ii*6+jj, :, :] = np.array([xy[jj, :], xy[(jj + 1) % 6, :]])

    def createCollection(self, ax):
        if self.outsideBordersOnly:
            self.collection = LineCollection(self.lines_list)
        else:
            self.collection = PatchCollection(self.patches_list)  #, match_original=True
        ax.add_collection(self.collection)

    def set_fc_colors(self, fcColors):
        if self.collection:
            self.collection.set_facecolors(fcColors)
        else:
            for ii, color in enumerate(fcColors):
                self.patches_list[ii].set_fc(color)

    def set_fill(self, fill):
        # self.collection.set_fill(fill)
        for patch in self.patches_list:
            patch.set_fill(fill)

    def set_hatch(self, hatch='x'):
        for patch in self.patches_list:
            patch.set_hatch(hatch)

    def set_lw(self, lw):
        for patch in self.patches_list:
            patch.set_linewidth(lw)
        if self.collection:
            self.collection.set_lw(lw)

    def set_ec_colors(self, ecColors):
        if self.collection:
            self.collection.set_edgecolors(ecColors)
        else:
            for ii, color in enumerate(ecColors):
                if ii < len(self.patches_list):
                    self.patches_list[ii].set_ec(color)
                else:
                    break

