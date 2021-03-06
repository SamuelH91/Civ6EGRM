from PyQt5 import QtWidgets
from utils.hexgrid import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from saveFileHandler.gameDataHandler import *
import io
from PIL import Image
from pygifsicle import gifsicle
import subprocess as sp
import argparse
import platform

platformWin7 = platform.release() == "7" and platform.system() == "Windows"
LANGUAGES = ["en_EN", "ru_RU", "de_DE", "es_ES", "fr_FR", "it_IT", "ja_JP", "ko_KR", "pl_PL", "pt_BR"]


def run_arg_parser():
    # Create the parser
    arg_parser = argparse.ArgumentParser(description='endGameReplay.py reads all civ6 autosave files from -d "<location>"\n'
                                                     'and displays end game replay map turn by turn. You can also create\n'
                                                     'mp4 and gif files from your game.')
    # Add the arguments
    arg_parser.add_argument('-d', metavar='civ6 autosave directory', action='store', type=str,
                            required=False, help='the path to the autosave folder')
    # Execute the parse_args() method
    args = arg_parser.parse_args()
    target_path = args.d

    if target_path:
        if not os.path.isdir(target_path):
            target_path = None
        else:
            target_path = os.path.expanduser(target_path + "/")

    if not target_path:
        print('The path specified does not exist using default target folder ./auto/data, use -d <dir_path> to change')
        target_path = os.getcwd() + "/data/auto/"  # Default location where runFileWatcher copies all auto saves

    return target_path

# pg.setConfigOptions(antialias=True)


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
        button_toggle.clicked.connect(self.parent.toggleBorders)

        button_toggle_water_borders = QtWidgets.QPushButton('Water Borders', self)
        button_layout.addWidget(button_toggle_water_borders)
        button_toggle_water_borders.clicked.connect(self.parent.toggleWaterBorders)

        button_toggle_civs = QtWidgets.QPushButton('Civ names', self)
        button_layout.addWidget(button_toggle_civs)
        button_toggle_civs.clicked.connect(self.parent.toggleCivilizationNames)
        set_civ_width_button = QtWidgets.QPushButton("Set civ width")
        button_layout.addWidget(set_civ_width_button)
        set_civ_width_button.clicked.connect(self.parent.set_civ_width)

        button_play = QtWidgets.QPushButton('Play', self)
        button_layout.addWidget(button_play)
        button_play.clicked.connect(self.parent.play)

        button_pause = QtWidgets.QPushButton('Pause', self)
        button_layout.addWidget(button_pause)
        button_pause.clicked.connect(self.parent.setPause)

        button_gif = QtWidgets.QPushButton('Create gif', self)
        button_layout.addWidget(button_gif)
        button_gif.clicked.connect(self.parent.createGif)

        button_mp4 = QtWidgets.QPushButton('Create mp4', self)
        button_layout.addWidget(button_mp4)
        button_mp4.clicked.connect(self.parent.createMp4)

        coordinate_widget = QtWidgets.QWidget(self)
        button_layout.addWidget(coordinate_widget)
        coordinate_layout = QtWidgets.QHBoxLayout(coordinate_widget)

        self.x_value = QtWidgets.QLabel(self)
        coordinate_layout.addWidget(self.x_value)
        self.x_value.setNum(0)

        self.y_value = QtWidgets.QLabel(self)
        coordinate_layout.addWidget(self.y_value)
        self.y_value.setNum(0)

        self.civ = QtWidgets.QLabel(self)
        button_layout.addWidget(self.civ)
        self.civ.setWordWrap(True)
        self.civ.setText("")

        # creating a QGraphicsDropShadowEffect object
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        # setting blur radius
        shadow.setBlurRadius(1)
        shadow.setOffset(1)
        # adding shadow to the label
        self.civ.setGraphicsEffect(shadow)

        updateFps_button = QtWidgets.QPushButton("Set output fps")
        button_layout.addWidget(updateFps_button)
        updateFps_button.clicked.connect(self.parent.updateFps)
        self.fps = QtWidgets.QLabel(self)  # QtWidgets.QLineEdit()
        button_layout.addWidget(self.fps)
        self.fps.setNum(10)

        update_symbol_button = QtWidgets.QPushButton("Set symbol size")
        button_layout.addWidget(update_symbol_button)
        update_symbol_button.clicked.connect(self.parent.updateSymbolSize)

        toggle_events_button = QtWidgets.QPushButton("Toggle events")
        button_layout.addWidget(toggle_events_button)
        toggle_events_button.clicked.connect(self.parent.toggle_events)
        set_event_width_button = QtWidgets.QPushButton("Set event width")
        button_layout.addWidget(set_event_width_button)
        set_event_width_button.clicked.connect(self.parent.set_event_width)

        self.comboBox = QtWidgets.QComboBox(self)
        button_layout.addWidget(self.comboBox)
        for lan in LANGUAGES:
            self.comboBox.addItem(lan)
        self.comboBox.activated[str].connect(self.parent.setLanguage)

        self.status = QtWidgets.QLabel(self)
        button_layout.addWidget(self.status)
        self.status.setText("Status: Ready")


# class for scrollable label
class ScrollLabel(QtWidgets.QScrollArea):

    # contructor
    def __init__(self, *args, **kwargs):
        QtWidgets.QScrollArea.__init__(self, *args, **kwargs)

        # making widget resizable
        self.setWidgetResizable(True)

        # making qwidget object
        content = QtWidgets.QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QtWidgets.QVBoxLayout(content)

        # creating label
        self.label = QtWidgets.QLabel(content)

        # setting alignment to the text
        self.label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # making label multi-line
        self.label.setWordWrap(True)

        # adding label to the layout
        lay.addWidget(self.label)

    def set_text(self, text):
        # setting text to the label
        self.label.setText(text)


class MapVisualizerWidget(QtWidgets.QWidget):
    def __init__(self, parent, M, N, envColors, riverColors, outerBordersOnly, borderColors, borderColorsInner,
                 borderColorsSC, citiesColors, goodyHutColors, turnCount, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        layout = QtWidgets.QVBoxLayout(self)
        layoutH = QtWidgets.QHBoxLayout(self)

        # Civilization names
        self.civNames = QtWidgets.QLabel(self)
        self.civNames.setWordWrap(True)
        self.civNames.setText("Finland\nis a great country!")
        #self.civNames.setStyleSheet("outline: 2px black;")
        layoutH.addWidget(self.civNames)

        # creating a QGraphicsDropShadowEffect object
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        # setting blur radius
        shadow.setBlurRadius(1)
        shadow.setOffset(1)
        # adding shadow to the label
        self.civNames.setGraphicsEffect(shadow)

        self.graphWidget = pg.PlotWidget()
        layoutH.addWidget(self.graphWidget)
        self.graphWidget.setAspectLocked(True)
        self.graphWidget.setAntialiasing(True)
        self.graphWidget.setBackground((0, 0, 0, 0))
        self.graphWidget.getPlotItem().hideAxis('bottom')
        self.graphWidget.getPlotItem().hideAxis('left')
        self.graphWidget.scene().sigMouseClicked.connect(self.parent.mouse_clicked)
        self.graphWidget.setMouseTracking(True)

        self.eventList = ScrollLabel()
        layoutH.addWidget(self.eventList)
        self.eventList.set_text("Test\nNothing\nTo\nSee\nHere\nYet\nSorry\n\U0001F3BC&nbsp;\n\u2699&nbsp;\n\U0001F6E1&nbsp;&nbsp;\nWar, peace, capture, raze, etc...\n\n\n\n\n^\n|\n|\n|\nv\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\U0001F64F&nbsp;\n\u2697&nbsp;\n\U0001F4B0&nbsp;&nbsp;\n\u2693&nbsp;")
        self.eventList.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.eventList.setAlignment(QtCore.Qt.AlignRight)
        self.eventList.setMaximumWidth(200)
        # self.eventList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.eventList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.eventList.setVisible(False)

        shadow2 = QtWidgets.QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(1)
        shadow2.setOffset(1)
        self.eventList.label.setGraphicsEffect(shadow2)

        layout.addLayout(layoutH)

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

        # Inner borders secondary color
        self.bordersHG_inner = HexGrid(M, N, 0.55, outerBordersOnly)
        self.bordersHG_inner.set_ec_colors(borderColorsInner)
        self.bordersHG_inner.generatePicture()
        self.graphWidget.addItem(self.bordersHG_inner)

        # Outer borders primary color
        self.bordersHG = HexGrid(M, N, 0.7, outerBordersOnly)
        self.bordersHG.set_ec_colors(borderColors)
        self.bordersHG.generatePicture()
        self.graphWidget.addItem(self.bordersHG)

        # City state borders color
        self.bordersHG_cs = HexGrid(M, N, 0.85, outerBordersOnly)
        self.bordersHG_cs.set_ec_colors(borderColorsSC)
        self.bordersHG_cs.generatePicture()
        self.graphWidget.addItem(self.bordersHG_cs)

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

        self.symbols = {}  # pg.TextItem('', **{'color': '#FFF'})
        # self.graphWidget.addItem(self.label_value)
        # self.label_value.setPos(QtCore.QPointF(2, 10))
        # self.label_value.setText("\U0001F6E1")

    def add_symbol(self, key, x, y, text):
        self.symbols[key] = pg.TextItem('', anchor=(0.5, 0.5))  # pg.TextItem('', **{'color': '#FFF'})
        self.graphWidget.addItem(self.symbols[key])
        self.symbols[key].setPos(QtCore.QPointF(x, y))
        self.symbols[key].setHtml(text)

    def set_symbol_size(self, size):
        font = QtGui.QFont()
        font.setPixelSize(size)
        for symbol in self.symbols:
            self.symbols[symbol].setFont(font)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, app, target_path=None, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Civ VI End Game Replay Map")
        self.app = app
        self.pause = False
        self.currentIdx = 0
        self.current_timer = None
        self.timerCount = 0
        self.timerCurrentCount = 0
        self.imageList = []
        self.hidden = False
        self.enableTiming = False
        self.outputFps = 10
        self.symbolSize = 20
        self.eventListWidth = 200
        self.civWidth = None

        # Options
        self.OptimizeGif = True
        self.outerBordersOnly = True
        self.useCivColors = True
        self.riversOn = True
        self.drawWaterBorders = True
        self.useInnerColorAsCity = True
        if target_path:
            self.saveDataLocation = target_path
        else:
            self.saveDataLocation = os.getcwd() + "/data/auto/"  # Default location where runFileWatcher copies all auto saves

        # Read and parse all files to memory
        self.gdh = GameDataHandler(self.saveDataLocation)
        self.gdh.parseData()

        # Calculate border colors
        self.gdh.calculateBorderColors(3, self.outerBordersOnly, self.useCivColors, self.drawWaterBorders)
        self.gdh.calculateCityColors(self.useInnerColorAsCity)
        # self.gdh.calculateMinorCityColors()

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
                                self.outerBordersOnly, self.gdh.borderColors[0], self.gdh.borderColorsInner[0],
                                self.gdh.borderColorsSC[0], self.gdh.cityColors[0], self.gdh.goodyHuts[0],
                                self.TurnCount)
        main_layout.addWidget(self.plot_widget)

        # Set civ names
        self.gdh.parseCivNames()
        self.setCivilizationNames(self.gdh.getCivNames(0))

        # City state symbol locations
        for i, minor in enumerate(self.gdh.minorOrigos):
            x, y = self.plot_widget.environmentHG.get_hexa_xy(self.gdh.minorOrigos[minor])
            # symbol = CS_UNICODE_MAP[self.gdh.minorCivTypes[minor]].replace("&nbsp;", "").replace(" ", "")
            self.plot_widget.add_symbol(minor, x, y, "")

        self.plot_widget.set_symbol_size(self.symbolSize)

        self.showMaximized()

    def setLanguage(self, language):
        if language == LANGUAGES[0]:
            self.gdh.parseCivNames()
        else:
            self.gdh.parseCivNames(language)
        self.currentIdx = self.plot_widget.turnSlider.sliderPosition()
        self.updateCivs(self.currentIdx - 1)

    def updateCivs(self, turn):
        self.setCivilizationNames(self.gdh.getCivNames(turn))

    def updateFps(self):
        num, ok = QtWidgets.QInputDialog.getInt(self, "Set output fps value", "Enter a number", self.outputFps)
        if ok:
            self.outputFps = num
            self.buttons_widget.fps.setNum(num)

    def updateSymbolSize(self):
        num, ok = QtWidgets.QInputDialog.getInt(self, "Set on map symbol size", "Enter a number", self.symbolSize)
        if ok:
            self.symbolSize = num
            self.buttons_widget.symbol_size.setNum(num)
            self.plot_widget.set_symbol_size(num)

    def set_civ_width(self):
        num, ok = QtWidgets.QInputDialog.getInt(self, "Set on civ width", "Enter a number",
                                                self.plot_widget.civNames.sizeHint().width())
        if ok:
            self.civWidth = num
            self.plot_widget.civNames.setMaximumWidth(num)
        # else:
            # self.plot_widget.civNames.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
            # self.plot_widget.civNames.setMaximumSize(self.plot_widget.civNames.sizeHint())

    def set_event_width(self):
        num, ok = QtWidgets.QInputDialog.getInt(self, "Set on event list width", "Enter a number",
                                                self.plot_widget.eventList.sizeHint().width())
        if ok:
            self.eventListWidth = num
            self.plot_widget.eventList.setMaximumWidth(num)

    def toggle_events(self):
        self.plot_widget.eventList.setHidden(not self.plot_widget.eventList.isHidden())

    def toggleCivilizationNames(self):
        self.plot_widget.civNames.setHidden(not self.plot_widget.civNames.isHidden())

    def setCivilizationNames(self, text):
        self.plot_widget.civNames.setText(text)

    def setCityStateSymbolAtTurn(self, idx):
        for i in range(self.gdh.majorCivs, self.gdh.minorCivs + self.gdh.majorCivs):
            if i in self.plot_widget.symbols:
                symbol = ""  # \u2b22
                colorhexMinor = "181818"
                if self.gdh.playersAlive[idx][i] and idx != 0:
                    symbol = CS_UNICODE_MAP[self.gdh.minorCivTypes[i]].replace("&nbsp;", "").replace(" ", "")
                    colorhexMinor = ''.join([format(int(c), '02x') for c in civColorsMinor[i]])
                self.plot_widget.symbols[i].setHtml("<font color=#" + colorhexMinor + ">" + symbol + "</font>")

    def updateTurn(self, turn):
        t0 = time.time()
        self.plot_widget.bordersHG_cs.set_ec_colors(self.gdh.borderColorsSC[turn - 1])
        t1 = time.time()
        tBorderSC = t1 - t0
        t0 = time.time()
        self.plot_widget.bordersHG_inner.set_ec_colors(self.gdh.borderColorsInner[turn - 1])
        t1 = time.time()
        tBorderInner = t1 - t0
        t0 = time.time()
        self.plot_widget.bordersHG.set_ec_colors(self.gdh.borderColors[turn - 1])
        t1 = time.time()
        tBorder = t1 - t0
        t0 = t1
        self.plot_widget.goodyHutHG.set_fc_colors(self.gdh.goodyHuts[turn - 1])
        t1 = time.time()
        tGoody = t1 - t0
        t0 = t1
        self.plot_widget.citiesHG.set_fc_colors(self.gdh.cityColors[turn - 1])
        t1 = time.time()
        tCity = t1 - t0

        self.setCityStateSymbolAtTurn(turn - 1)

        self.updateCivs(turn - 1)

        if self.enableTiming:
            print("Border update took {} s".format(tBorderSC))
            print("Border update took {} s".format(tBorderInner))
            print("Border update took {} s".format(tBorder))
            print("GoodyHut update took {} s".format(tGoody))
            print("City update took {} s".format(tCity))

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

    def toggleBorders(self):
        self.currentIdx = self.plot_widget.turnSlider.sliderPosition()
        if self.hidden:
            self.plot_widget.bordersHG_cs.set_ec_colors(self.gdh.borderColorsSC[self.currentIdx - 1])
            self.plot_widget.bordersHG_inner.set_ec_colors(self.gdh.borderColorsInner[self.currentIdx - 1])
            self.plot_widget.bordersHG.set_ec_colors(self.gdh.borderColors[self.currentIdx - 1])
            self.hidden = False
        else:
            self.plot_widget.bordersHG_cs.set_ec_colors([emptyPen] * len(self.gdh.borderColors[self.currentIdx - 1]))
            self.plot_widget.bordersHG_inner.set_ec_colors([emptyPen] * len(self.gdh.borderColors[self.currentIdx - 1]))
            self.plot_widget.bordersHG.set_ec_colors([emptyPen] * len(self.gdh.borderColors[self.currentIdx - 1]))
            self.hidden = True

    def toggleWaterBorders(self):
        self.drawWaterBorders = not self.drawWaterBorders
        print("Recalculating borders")
        self.updateStatus("Status: Recalculating borders")
        self.gdh.calculateBorderColors(3, self.outerBordersOnly, self.useCivColors, self.drawWaterBorders)
        print("Borders calculated")
        self.updateStatus("Status: Ready")
        self.currentIdx = self.plot_widget.turnSlider.sliderPosition()
        self.updateTurn(self.currentIdx)

    def play(self):
        self.pause = False
        self.currentIdx = self.plot_widget.turnSlider.sliderPosition()
        self.start_timer(self.TurnCount-self.currentIdx+1, 100)

    def updateStatus(self, status):
        self.buttons_widget.status.setText(status)
        self.buttons_widget.update()
        self._main.update()
        QtWidgets.QApplication.processEvents()

    def createGif(self):
        M = len(self.imageList)
        if M == 0:
            self.createImages()
        M = len(self.imageList)
        print("Please wait patiently: saving and optimizing gif!")
        self.updateStatus("Status: Creating gif, please wait")
        fps = self.outputFps
        self.imageList[0].save('endGameReplayMap.gif', save_all=True, append_images=self.imageList[1:], optimize=False, duration=1000/fps, loop=0)
        self.updateStatus("Status: Optimizing gif, please wait")
        gifsicle(
            sources=["endGameReplayMap.gif"],  # or a single_file.gif
            destination="endGameReplayMap.gif",   # or just omit it and will use the first source provided.
            optimize=False,  # Whetever to add the optimize flag of not, optimized with -O3 option
            colors=256,  # Number of colors t use
            options=["--verbose", "-O3"],  # Options to use. "--lossy"
        )
        self.updateStatus("Status: Gif done!")
        print("Gif done!")

    def createMp4(self):
        remove_row = False
        remove_column = False
        M = len(self.imageList)
        if M == 0:
            self.createImages()
        M = len(self.imageList)
        width, height = self.imageList[0].size

        # To fix error when odd width/height size (in windows 7 version)
        if height % 2 == 1:
            remove_row = True
            height -= 1
        if width % 2 == 1:
            remove_column = True
            width -= 1
        fps = self.outputFps
        print("Creating mp4, please wait")
        self.updateStatus("Status: Creating mp4, please wait")
        command = ["ffmpeg.exe",
                   "-f", "rawvideo",
                   "-vcodec", "rawvideo",
                   "-s", str(width) + "x" + str(height),
                   "-pix_fmt", "rgba",
                   "-r", str(fps),
                   "-loglevel", "error",
                   "-i", "pipe:",
                   "-vcodec", "h264",
                   "-pix_fmt", "yuv420p",
                   "-y", "endGameReplayMap.mp4"]

        pipe = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)
        for image in self.imageList:
            imtemp = np.array(image.copy())
            if remove_row:
                imtemp = np.delete(imtemp, 0, 0)
            if remove_column:
                imtemp = np.delete(imtemp, 0, 1)
            pipe.stdin.write(imtemp.tobytes())

        for ii in range(M % fps + 1):
            imtemp = np.array(self.imageList[M - 1].copy())
            if remove_row:
                imtemp = np.delete(imtemp, 0, 0)
            if remove_column:
                imtemp = np.delete(imtemp, 0, 1)
            pipe.stdin.write(imtemp.tobytes())

        self.updateStatus("Status: Mp4 done!")
        print("Mp4 done!")

    def createImages(self):
        self.updateStatus("Status: Gathering data")
        for ii in range(1, self.TurnCount + 1):
            self.plot_widget.turnSlider.setValue(ii)
            self._main.update()
            QtWidgets.QApplication.processEvents()
            screenshot = self.plot_widget.grab()
            buffer = QtCore.QBuffer()
            buffer.open(QtCore.QBuffer.ReadWrite)
            screenshot.save(buffer, "png")
            self.imageList.append(Image.open(io.BytesIO(buffer.data())))

    def setPause(self):
        self.pause = True

    def updateSlider(self, idx):
        self.plot_widget.turnSlider.setValue(idx)

    def mouse_clicked(self, mouseClickEvent):
        # mouseClickEvent is a pyqtgraph.GraphicsScene.mouseEvents.MouseClickEvent
        pos = mouseClickEvent.pos()
        if self.plot_widget.graphWidget.sceneBoundingRect().contains(pos):
            mousePoint = self.plot_widget.graphWidget.plotItem.vb.mapSceneToView(pos)
            # print("x: {}, y {}".format(mousePoint.x(), mousePoint.y()))
            yidx = np.floor((mousePoint.y() + 1/np.sqrt(3)) / (np.sqrt(3) / 2))
            xidx = np.floor(mousePoint.x() + 0.5 - (yidx % 2) * 0.5)
            # print("x: {}, y {}".format(xidx, yidx))
            self.buttons_widget.x_value.setNum(xidx)
            self.buttons_widget.y_value.setNum(yidx)
            self.currentIdx = self.plot_widget.turnSlider.sliderPosition()
            language = self.buttons_widget.comboBox.currentText()
            owner = self.gdh.getOwner(self.currentIdx - 1, int(xidx), int(yidx), language)
            self.buttons_widget.civ.setText(owner)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow(app, run_arg_parser())
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
