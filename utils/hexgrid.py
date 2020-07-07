from utils.hexagon import Hexagon
from PyQt5 import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

Y0 = np.sqrt(3)/2
Y1 = 1/np.sqrt(3)
Y2 = 1/2/np.sqrt(3)
X1 = 0.0
X2 = 0.5


class HexGrid(pg.GraphicsObject):  # pg.GraphicsItem
    def __init__(self, x, y, scale=1.0, outsideBordersOnly=False, parent=None):
        super().__init__(parent)
        self.picture = QtGui.QPicture()
        self.X = x
        self.Y = y
        self.hexagons = []
        self.lines = []
        self.lines_list = []
        self.ec_colors = None
        self.fc_colors = None
        self.edgesVisible = True
        self.lw = 0.2
        self.neigbours_list = []
        self.outsideBordersOnly = outsideBordersOnly
        for yy in range(y):
            xOffset = X2 if yy % 2 == 1 else X1
            yval = yy*Y0
            for xx in range(x):
                self.hexagons.append(Hexagon(np.array([[xx + xOffset], [yval]]), scale))
        if self.outsideBordersOnly:
            self.lines_list = np.zeros((6*self.X*self.Y, 2, 2))
            for ii, hexagon in enumerate(self.hexagons):
                xy = hexagon.get_xy()
                for jj in range(6):
                    self.lines.append(QtCore.QLineF(xy[jj, 0], xy[jj, 1], xy[(jj + 1) % 6, 0], xy[(jj + 1) % 6, 1]))

    def generatePicture(self):
        # pre-computing a QPicture object allows paint() to run much more quickly,
        # rather than re-drawing the shapes every time.
        p = QtGui.QPainter(self.picture)
        if self.outsideBordersOnly:
            for ii, line in enumerate(self.lines):
                p.setPen(self.ec_colors[ii])
                p.drawLine(line)
        else:
            if self.edgesVisible:
                p.setPen(pg.mkPen('w', width=self.lw))  # None pg.mkPen('w', width=self.lw)
            else:
                p.setPen(pg.mkPen(None))
            for ii, hexagon in enumerate(self.hexagons):
                p.setBrush(self.fc_colors[ii])  # None
                p.drawPolygon(hexagon)
        p.end()
        self.update()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())

    def set_fc_colors(self, fcColors):
        self.fc_colors = fcColors
        self.generatePicture()

    def set_edges_visible(self, visible):
        self.edgesVisible = visible

    def set_lw(self, lw):
        self.lw = lw

    def set_ec_colors(self, ecColors):
        self.ec_colors = ecColors
        self.generatePicture()
