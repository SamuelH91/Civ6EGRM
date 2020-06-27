from utils.hexagon import Hexagon
import numpy as np

Y0 = np.sqrt(3)/2
Y1 = 1/np.sqrt(3)
Y2 = 1/2/np.sqrt(3)
X1 = 0.0
X2 = 0.5


class HexGrid:
    def __init__(self, x, y, scale=1.0):
        self.X = x
        self.Y = y
        self.patches_list = []
        for yy in range(y):
            xOffset = X2 if yy % 2 == 1 else X1
            yval = yy*Y0
            for xx in range(x):
                self.patches_list.append(Hexagon(np.array([[xx + xOffset], [yval]]), scale))

    def set_fc_colors(self, fcColors):
        for ii, color in enumerate(fcColors):
            self.patches_list[ii].set_fc(color)

    def set_fill(self, fill):
        for patch in self.patches_list:
            patch.set_fill(fill)

    def set_lw(self, lw):
        for patch in self.patches_list:
            patch.set_linewidth(lw)

    def set_ec_colors(self, ecColors):
        for ii, color in enumerate(ecColors):
            self.patches_list[ii].set_ec(color)

