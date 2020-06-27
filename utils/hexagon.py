import matplotlib.patches as poly
import numpy as np

Y1 = 1/np.sqrt(3)
Y2 = 1/2/np.sqrt(3)
X1 = 0.0
X2 = 0.5
HXY = np.array([[X1, X2, X2, X1, -X2, -X2], [Y1, Y2, -Y2, -Y1, -Y2, Y2]])


class Hexagon(poly.Polygon):
    def __init__(self, xy, scale=1):
        super().__init__(np.transpose(HXY * scale + xy))
