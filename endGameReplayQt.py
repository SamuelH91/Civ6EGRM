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
        self.riversHG.generatePicture()
        self.graphWidget.addItem(self.riversHG)

        self.bordersHG = HexGrid(M, N, 0.9, outerBordersOnly)
        self.bordersHG.set_ec_colors(borderColors)
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

class TurnWidget(QtWidgets.QWidget):
    def __init__(self, parent, turnCount, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent

        layout = QtWidgets.QVBoxLayout(self)

        slider_widget = QtWidgets.QWidget(self)
        layout.addWidget(slider_widget)
        slider_layout = QtWidgets.QHBoxLayout(slider_widget)

        self.turnSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.turnSlider.setMinimum(1)
        self.turnSlider.setMaximum(turnCount)
        self.turnSlider.setValue(1)
        self.turnSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.turnSlider.setTickInterval(1)
        slider_layout.addWidget(self.turnSlider)
        self.turnSlider.valueChanged.connect(self.parent.updateTurn)

        slider_value = QtWidgets.QLabel(self)
        slider_layout.addWidget(slider_value)
        slider_value.setNum(1)
        self.turnSlider.valueChanged.connect(slider_value.setNum)


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
        button_play.clicked.connect(self.parent.play)

        button_pause = QtWidgets.QPushButton('Pause', self)
        button_layout.addWidget(button_pause)
        button_pause.clicked.connect(self.parent.setPause)

        button_gif = QtWidgets.QPushButton('Create gif', self)
        button_layout.addWidget(button_gif)
        # button_gif.clicked.connect(self.parent.plot_widget.button_pressed)

        button_mp4 = QtWidgets.QPushButton('Create mp4', self)
        button_layout.addWidget(button_mp4)
        # button_mp4.clicked.connect(self.parent.plot_widget.button_pressed)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, app, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Civ VI End Game Replay Map")
        self.app = app
        self.pause = False
        self.currentIdx = 0
        self.current_timer = None
        self.timerCount = 0
        self.timerCurrentCount = 0

        # Options
        self.OptimizeGif = True
        self.outerBordersOnly = True
        self.riversOn = True
        self.saveDataLocation = os.getcwd() + "/data/auto/"  # Default location where runFileWatcher copies all auto saves

        # Read and parse all files to memory
        self.gdh = GameDataHandler(self.saveDataLocation)
        self.gdh.parseData()

        # Calculate border colors
        self.gdh.calculateBorderColors(3, self.outerBordersOnly)
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
                                self.outerBordersOnly, self.gdh.borderColors[0],
                                self.gdh.cityColors[0], self.gdh.goodyHuts[0])
        main_layout.addWidget(self.plot_widget)

        self.slider_widget = TurnWidget(self, self.TurnCount)
        main_layout.addWidget(self.slider_widget)

        self.showMaximized()

    def updateTurn(self, turn):
        t0 = time.time()
        self.plot_widget.bordersHG.set_ec_colors(self.gdh.borderColors[turn - 1])
        t1 = time.time()
        print("Border update took {} s".format(t1 - t0))
        t0 = t1
        self.plot_widget.goodyHutHG.set_fc_colors(self.gdh.goodyHuts[turn - 1])
        t1 = time.time()
        print("GoodyHut update took {} s".format(t1 - t0))
        t0 = t1
        self.plot_widget.citiesHG.set_fc_colors(self.gdh.cityColors[turn - 1])
        t1 = time.time()
        print("City update took {} s".format(t1 - t0))

    # def start_timer(self, func, count=1, interval=1000):
    #     counter = 0
    #
    #     def handler():
    #         nonlocal counter
    #         counter += 1
    #         func()
    #         if counter >= count:
    #             timer.stop()
    #             timer.deleteLater()
    #
    #     timer = QtCore.QTimer()
    #     timer.timeout.connect(handler)
    #     timer.start(interval)

    def start_timer(self, count=1, interval=1000):
        if self.current_timer:
            self.current_timer.stop()
            self.current_timer = None
        self.timerCount = count
        self.timerCurrentCount = 0
        self.current_timer = QtCore.QTimer()
        self.current_timer.timeout.connect(self.handler)
        self.current_timer.start(interval)

    def handler(self):
        self.timerCurrentCount += 1
        self.updateSlider(self.currentIdx)
        self.currentIdx += 1
        if self.timerCurrentCount >= self.timerCount or self.pause:
            self.current_timer.stop()
            self.current_timer = None

    def play(self):
        self.pause = False
        self.currentIdx = self.slider_widget.turnSlider.sliderPosition()
        self.start_timer(self.TurnCount-self.currentIdx+1, 100)

    def setPause(self):
        self.pause = True

    def updateSlider(self, idx):
        self.slider_widget.turnSlider.setValue(idx)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow(app)
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()