import matplotlib.pyplot as plt
from utils.hexgrid import HexGrid

from matplotlib.collections import PatchCollection
from saveFileHandler.gameDataHandler import *
from matplotlib.widgets import Button, Slider
import os

# TODO: Rivers, + improve: goody huts, barbarians, icebergs
# TODO: Lock civ colors and city visualization
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
bax = fig.add_axes([0.1, 0.95, 0.2, 0.05])
button_toggleB = Button(bax, "Toggle borders")
bax2 = fig.add_axes([0.3, 0.95, 0.2, 0.05])
button_randomC = Button(bax2, "Random colors")
bax3 = fig.add_axes([0.5, 0.95, 0.2, 0.05])
button_playB = Button(bax3, "Play")
bax4 = fig.add_axes([0.7, 0.95, 0.2, 0.05])
button_pauseB = Button(bax4, "Pause")

# Slider for turns
axTurn = plt.axes([0.1, 0.03, 0.8, 0.02])
sTurn = Slider(axTurn, 'Turn', 1, TurnCount, valinit=1, valstep=1)

hg_environment = HexGrid(M, N)
hg_borders = HexGrid(M, N, 0.9, outerBordersOnly)
hg_rivers = HexGrid(M, N, 1.0, outerBordersOnly)
hg_goodyHut = HexGrid(M, N, 0.35)

hg_environment.set_fc_colors(gdh.envColors)
hg_goodyHut.set_fc_colors(gdh.goodyHuts[0])
hg_borders.set_fill(False)
hg_borders.set_lw(4)
hg_rivers.set_fill(False)
hg_rivers.set_lw(4)

hg_environment.createCollection(ax)
hg_rivers.createCollection(ax)
hg_borders.createCollection(ax)
hg_goodyHut.createCollection(ax)

hg_borders.set_ec_colors(gdh.borderColors[0])
hg_rivers.set_ec_colors(gdh.riverColors)

# p_env = PatchCollection(hg_environment.patches_list, match_original=True)
# ax.add_collection(p_env)

# p_borders = PatchCollection(hg_borders.patches_list, match_original=True)
# ax.add_collection(p_borders)

# p_goodyHuts = PatchCollection(hg_goodyHut.patches_list, match_original=True)
# ax.add_collection(p_goodyHuts)

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
    hg_borders.set_ec_colors(gdh.borderColors[sTurn.val-1])
    hg_goodyHut.set_fc_colors(gdh.goodyHuts[sTurn.val-1])
    fig.canvas.draw()
    fig.canvas.flush_events()
button_randomC.on_clicked(randomColorsCivs)

def updateTurnSlider(event):
    hg_borders.set_ec_colors(gdh.borderColors[sTurn.val-1])
    hg_goodyHut.set_fc_colors(gdh.goodyHuts[sTurn.val-1])
    fig.canvas.draw()
    fig.canvas.flush_events()
sTurn.on_changed(updateTurnSlider)

plt.show()
