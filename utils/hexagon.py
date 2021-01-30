from PyQt5 import QtGui, QtCore
import numpy as np

Y1 = 1/np.sqrt(3)
Y2 = 1/2/np.sqrt(3)
X1 = 0.0
X2 = 0.5
HXY = np.array([[X1, X2, X2, X1, -X2, -X2], [Y1, Y2, -Y2, -Y1, -Y2, Y2]])


class Hexagon(QtGui.QPolygonF):
    def __init__(self, xy, scale=1):
        super().__init__()
        self.xy = xy
        for row in np.transpose(HXY * scale + xy):
            self.append(QtCore.QPointF(row[0], row[1]))

    def get_xy(self):
        N = self.size()
        xy = np.zeros((N, 2))
        for ii in range(N):
            point = self.at(ii)
            xy[ii, :] = np.array([point.x(), point.y()])
        return xy

    def get_mid_coord(self):
        return self.xy[0], self.xy[1]

# if __name__ == '__main__':
# #     hex1 = Hexagon(np.array([[0], [0]]))
# #     test = hex1.get_xy()
# #     print("Test")
