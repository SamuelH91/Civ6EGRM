import matplotlib.pyplot as plt
from utils.hexgrid import HexGrid

from matplotlib.collections import PatchCollection
from saveFileHandler.gameDataHandler import *
from matplotlib.widgets import Button, Slider
import os
import matplotlib.animation as animation  # requires ffmpeg installed
from matplotlib.animation import FuncAnimation, PillowWriter
from pygifsicle import gifsicle

# TODO: Lock civ colors
# TODO: Include natural wonders
# TODO: Take actual turn number in use

# TODO: Nice to have stuff in future:
#       TODO: Optional visualize units
#       TODO: List events (e.g. wars, wonders, great people)

# Options
OptimizeGif = True
outerBordersOnly = True
saveDataLocation = os.getcwd() + "/data/auto/"  # Default location where runFileWatcher copies all auto saves

# Read and parse all files to memory
gdh = GameDataHandler(saveDataLocation)
gdh.parseData()

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
button_gifB = Button(bax5, "Create gif")
bax6 = fig.add_axes([0.80, 0.95, 0.15, 0.05])
button_movieB = Button(bax6, "Create mp4")

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

def createMovie(event):
    ani = FuncAnimation(fig, setSlider, np.linspace(1, TurnCount+2, TurnCount+2))  # some problem with ending, cuts out
    writervideo = animation.FFMpegWriter(fps=1)
    ani.save("endGameReplayMap.mp4", writer=writervideo)
    print("Mp4 done!")
button_movieB.on_clicked(createMovie)

def setSlider(value):
    if value <= TurnCount:
        sTurn.set_val(int(value))

def createGif(event):
    ani = FuncAnimation(fig, setSlider, np.linspace(1, TurnCount, TurnCount))
    writer = PillowWriter(fps=10)
    ani.save("endGameReplayMap.gif", writer=writer)
    if OptimizeGif:
        gifsicle(
            sources=["endGameReplayMap.gif"],  # or a single_file.gif
            destination="endGameReplayMap.gif",   # or just omit it and will use the first source provided.
            optimize=False,  # Whetever to add the optimize flag of not, optimized with -O3 option
            colors=256,  # Number of colors t use
            options=["--verbose", "-O3"],  # Options to use. "--lossy"
        )
    print("Gif done!")
button_gifB.on_clicked(createGif)

plt.show()