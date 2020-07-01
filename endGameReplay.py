import matplotlib.pyplot as plt
from utils.hexgrid import HexGrid

from matplotlib.collections import PatchCollection
from saveFileHandler.gameDataHandler import *
from matplotlib.widgets import Button, Slider
import os
# import matplotlib.animation as manimation  # requires ffmpeg installed
from matplotlib.animation import FuncAnimation, PillowWriter

# TODO: Lock civ colors
# TODO: Include natural wonders
# TODO: Take actual turn number in use

# TODO: Nice to have stuff in future:
#       TODO: Optional visualize units
#       TODO: List events (e.g. wars, wonders, great people)

# Read and parse all files to memory
gdh = GameDataHandler(os.getcwd() + "/data/auto/")
gdh.parseData()

outerBordersOnly = True
# Calculate border colors
gdh.calculateBorderColors(outerBordersOnly)
gdh.calculateCityColors()

# Calculate environment colors
gdh.calculateEnvColors()
gdh.calculateRiverColors()

# Other stuff
gdh.calculateOtherStuff()

# MapSize
M, N = gdh.getMapSize()

# TurnCount
TurnCount = gdh.getTurnCount()

# Figure
fig, ax = plt.subplots()

# Button for border toggling
bax = fig.add_axes([0.05, 0.95, 0.15, 0.05])
button_toggleB = Button(bax, "Toggle borders")
bax2 = fig.add_axes([0.20, 0.95, 0.15, 0.05])
button_randomC = Button(bax2, "Random colors")
bax3 = fig.add_axes([0.35, 0.95, 0.15, 0.05])
button_playB = Button(bax3, "Play")
bax4 = fig.add_axes([0.50, 0.95, 0.15, 0.05])
button_pauseB = Button(bax4, "Pause")
bax5 = fig.add_axes([0.65, 0.95, 0.15, 0.05])
button_movieB = Button(bax5, "Create gif")

# Slider for turns
axTurn = plt.axes([0.1, 0.03, 0.8, 0.02])
sTurn = Slider(axTurn, 'Turn', 1, TurnCount, valinit=1, valstep=1)

hg_environment = HexGrid(M, N)
hg_borders = HexGrid(M, N, 0.9, outerBordersOnly)
hg_rivers = HexGrid(M, N, 1.0, outerBordersOnly)
hg_goodyHut = HexGrid(M, N, 0.35)
hg_cities = HexGrid(M, N, 0.5)

hg_borders.set_fill(False)
hg_borders.set_lw(4)
hg_rivers.set_fill(False)
hg_rivers.set_lw(8)

hg_environment.createCollection(ax)
hg_rivers.createCollection(ax)
hg_borders.createCollection(ax)
hg_goodyHut.createCollection(ax)
hg_cities.createCollection(ax)

hg_environment.set_fc_colors(gdh.envColors)
hg_goodyHut.set_fc_colors(gdh.goodyHuts[0])
hg_cities.set_fc_colors(gdh.cityColors[0])

hg_borders.set_ec_colors(gdh.borderColors[0])
hg_rivers.set_ec_colors(gdh.riverColors)

ax.autoscale_view(True, True, True)
ax.set_aspect('equal', adjustable='box')

pause = False
def play(event):
    global pause
    pause = False
    for ii in range(sTurn.val, TurnCount+1):
        if not pause:
            sTurn.set_val(ii)
button_playB.on_clicked(play)

def pausePlay(event):
    global pause
    pause ^= True
button_pauseB.on_clicked(pausePlay)

def update(event):
    hg_borders.collection.set_visible(not hg_borders.collection.get_visible())
    fig.canvas.draw()
    fig.canvas.flush_events()
button_toggleB.on_clicked(update)

def randomColorsCivs(event):
    gdh.randomCivColors(20)
    updateTurnSlider(event)
button_randomC.on_clicked(randomColorsCivs)

def updateTurnSlider(event):
    hg_borders.set_ec_colors(gdh.borderColors[sTurn.val-1])
    hg_goodyHut.set_fc_colors(gdh.goodyHuts[sTurn.val-1])
    hg_cities.set_fc_colors(gdh.cityColors[sTurn.val-1])
    fig.canvas.draw()
    fig.canvas.flush_events()
sTurn.on_changed(updateTurnSlider)

# def createMovie(event):
#     FFMpegWriter = manimation.writers['ffmpeg']
#     writer = FFMpegWriter(fps=10)
#     with writer.saving(fig, "endGameReplayMap.mp4", TurnCount):
#         for ii in range(1, TurnCount + 1):
#             sTurn.set_val(ii)
#         writer.grab_frame()

def setSlider(value):
    sTurn.set_val(int(value))

def createMovie(event):
    ani = FuncAnimation(fig, setSlider, np.linspace(1, TurnCount, TurnCount))
    writer = PillowWriter(fps=10)
    ani.save("endGameReplayMap.gif", writer=writer)
button_movieB.on_clicked(createMovie)

plt.show()