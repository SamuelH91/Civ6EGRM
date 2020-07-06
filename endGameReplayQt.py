from PyQt5 import QtWidgets
from utils.hexgridQt import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from saveFileHandler.gameDataHandler import *

# pg.setConfigOptions(antialias=True)

class MapVisualizerWidget(QtWidgets.QWidget):
    def __init__(self, parent, M, N, envColors, riverColors, outerBordersOnly, borderColors, citiesColors,
                 goodyHutColors, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        layout = QtWidgets.QVBoxLayout(self)

        self.graphWidget = pg.PlotWidget()
        layout.addWidget(self.graphWidget)
        self.graphWidget.setAspectLocked(True)
        self.graphWidget.setAntialiasing(True)
        self.graphWidget.setBackground((0, 0, 0, 0))

        self.environmentHG = HexGrid(M, N)
        self.environmentHG.set_fc_colors(envColors)
        #self.environmentHG.set_edges_visible(False)
        #self.environmentHG.set_lw(0.1)
        self.environmentHG.generatePicture()
        self.graphWidget.addItem(self.environmentHG)

        self.riversHG = HexGrid(M, N, 1.0, True)
        self.riversHG.set_ec_colors(riverColors)
        self.riversHG.set_lw(4)
        self.riversHG.generatePicture()
        self.graphWidget.addItem(self.riversHG)

        self.bordersHG = HexGrid(M, N, 0.9, outerBordersOnly)
        self.bordersHG.set_ec_colors(borderColors)
        self.bordersHG.set_lw(3)
        self.bordersHG.generatePicture()
        self.graphWidget.addItem(self.bordersHG)

        self.citiesHG = HexGrid(M, N, 0.5)
        self.citiesHG.set_fc_colors(citiesColors)
        self.citiesHG.set_edges_visible(False)
        self.citiesHG.generatePicture()
        self.graphWidget.addItem(self.citiesHG)

        self.goodyHutHG = HexGrid(M, N, 0.35)
        self.goodyHutHG.set_fc_colors(goodyHutColors)
        self.goodyHutHG.set_edges_visible(False)
        self.goodyHutHG.generatePicture()
        self.graphWidget.addItem(self.goodyHutHG)

        # dynamic_canvas = FigureCanvas(Figure(figsize=(10, 10)))
        # layout.addWidget(dynamic_canvas)
        #
        # self._dynamic_ax = dynamic_canvas.figure.subplots()
        # dynamic_canvas.figure.canvas.mpl_connect('button_press_event', onclick)
        # self._dynamic_ax.grid()
        # self._timer = dynamic_canvas.new_timer(
        #     100, [(self._update_window, (), {})])
        # self._timer.start()

    # def button_pressed(self):
    #     if self.sender().text() == 'Stop':
    #         self._timer.stop()
    #     if self.sender().text() == 'Start':
    #         self._timer.start()
    #
    # def _update_window(self):
    #     self._dynamic_ax.clear()
    #     global x, y1, y2, y3, N, count_iter, last_number_clicks
    #     x.append(x[count_iter] + 0.01)
    #     y1.append(np.random.random())
    #     idx_inf = max([count_iter-N, 0])
    #     if last_number_clicks < len(clicks):
    #         for new_click in clicks[last_number_clicks:(len(clicks))]:
    #             rowPosition = self.parent.table_widget.table_clicks.rowCount()
    #             self.parent.table_widget.table_clicks.insertRow(rowPosition)
    #             self.parent.table_widget.table_clicks.setItem(rowPosition,0, QtWidgets.QTableWidgetItem(str(new_click)))
    #             self.parent.table_widget.table_clicks.setItem(rowPosition,1, QtWidgets.QTableWidgetItem("Descripcion"))
    #         last_number_clicks = len(clicks)
    #     self._dynamic_ax.plot(x[idx_inf:count_iter], y1[idx_inf:count_iter],'-o', color='b')
    #     count_iter += 1
    #     self._dynamic_ax.figure.canvas.draw()


class TurnWidget(QtWidgets.QWidget):
    def __init__(self, parent, turnCount, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent

        layout = QtWidgets.QVBoxLayout(self)

        slider_widget = QtWidgets.QWidget(self)
        layout.addWidget(slider_widget)
        slider_layout = QtWidgets.QHBoxLayout(slider_widget)

        turnSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        turnSlider.setMinimum(1)
        turnSlider.setMaximum(turnCount)
        turnSlider.setValue(1)
        turnSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        turnSlider.setTickInterval(1)
        slider_layout.addWidget(turnSlider)
        turnSlider.valueChanged.connect(self.parent.updateTurn)

        slider_value = QtWidgets.QLabel(self)
        slider_layout.addWidget(slider_value)
        slider_value.setNum(1)
        turnSlider.valueChanged.connect(slider_value.setNum)


class ButtonsWidget(QtWidgets.QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        layout = QtWidgets.QHBoxLayout(self)

        button_widget = QtWidgets.QWidget(self)
        layout.addWidget(button_widget)
        button_layout = QtWidgets.QHBoxLayout(button_widget)

        button_toggle = QtWidgets.QPushButton('Toggle borders', self)
        button_layout.addWidget(button_toggle)
        # button_toggle.clicked.connect(self.parent.plot_widget.button_pressed)

        button_play = QtWidgets.QPushButton('Play', self)
        button_layout.addWidget(button_play)
        # button_play.clicked.connect(self.parent.plot_widget.button_pressed)

        button_pause = QtWidgets.QPushButton('Pause', self)
        button_layout.addWidget(button_pause)
        # button_pause.clicked.connect(self.parent.plot_widget.button_pressed)

        button_gif = QtWidgets.QPushButton('Create gif', self)
        button_layout.addWidget(button_gif)
        # button_gif.clicked.connect(self.parent.plot_widget.button_pressed)

        button_mp4 = QtWidgets.QPushButton('Create mp4', self)
        button_layout.addWidget(button_mp4)
        # button_mp4.clicked.connect(self.parent.plot_widget.button_pressed)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Civ VI End Game Replay Map")

        # Options
        self.OptimizeGif = True
        self.outerBordersOnly = True
        self.riversOn = True
        self.saveDataLocation = os.getcwd() + "/data/auto/"  # Default location where runFileWatcher copies all auto saves

        # Read and parse all files to memory
        self.gdh = GameDataHandler(self.saveDataLocation)
        self.gdh.parseData()

        # Calculate border colors
        self.gdh.calculateBorderColors(self.outerBordersOnly)
        self.gdh.calculateCityColors()

        # Calculate environment colors
        self.gdh.calculateEnvColors()
        self.gdh.calculateRiverColors()

        # Other stuff
        self.gdh.calculateOtherStuff()

        # MapSize
        self.M, self.N = self.gdh.getMapSize()

        # TurnCount
        self.TurnCount = self.gdh.getTurnCount()

        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        main_layout = QtWidgets.QVBoxLayout(self._main)

        self.buttons_widget = ButtonsWidget(self)
        main_layout.addWidget(self.buttons_widget)

        self.plot_widget = \
            MapVisualizerWidget(self, self.M, self.N, self.gdh.envColors, self.gdh.riverColors,
                                self.outerBordersOnly, self.gdh.borderColors[1],
                                self.gdh.cityColors[1], self.gdh.goodyHuts[1])
        main_layout.addWidget(self.plot_widget)

        self.slider_widget = TurnWidget(self, self.TurnCount)
        main_layout.addWidget(self.slider_widget)

        self.showMaximized()

    def updateTurn(self, turn):
        t0 = time.time()
        self.plot_widget.bordersHG.set_ec_colors(self.gdh.borderColors[turn - 1])
        self.plot_widget.bordersHG.generatePicture()
        self.plot_widget.update()
        t1 = time.time()
        print("Border update took {} s".format(t1 - t0))
        # t0 = t1
        # hg_goodyHut.set_fc_colors(gdh.goodyHuts[sTurn.val - 1])
        # t1 = time.time()
        # print("GoodyHut update took {} s".format(t1 - t0))
        # t0 = t1
        # hg_cities.set_fc_colors(gdh.cityColors[sTurn.val - 1])
        # t1 = time.time()
        # print("City update took {} s".format(t1 - t0))
        # t0 = t1
        # # fig.canvas.draw()
        # fig.canvas.flush_events()
        # t1 = time.time()
        # print("Draw update took {} s".format(t1 - t0))



def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()