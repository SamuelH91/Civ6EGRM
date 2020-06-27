import matplotlib.pyplot as plt
from utils.hexgrid import HexGrid

from matplotlib.collections import PatchCollection
from saveFileHandler.gameDataHandler import *
from matplotlib.widgets import Button, Slider
import os

# TODO: Rivers, + improve: goody huts, barbarians, icebergs
# TODO: Lock civ colors and city visualization

# TODO: Nice to have stuff in future:
#       TODO: Optional visualize units
#       TODO: List events (e.g. wars, wonders, great people)

# Read and parse all files to memory
gdh = GameDataHandler(os.getcwd() + "/data/auto/")
gdh.parseData()

# Calculate border colors
gdh.calculateBorderColors()

# Calculate environment colors
gdh.calculateEnvColors()

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
button = Button(bax, "Toggle borders")
# Slider for turns
axTurn = plt.axes([0.1, 0.03, 0.8, 0.02])
sTurn = Slider(axTurn, 'Turn', 1, TurnCount, valinit=1, valstep=1)

hg_environment = HexGrid(M, N)
hg_borders = HexGrid(M, N, 0.85)
hg_goodyHut = HexGrid(M, N, 0.2)

hg_environment.set_fc_colors(gdh.envColors)
hg_goodyHut.set_fc_colors(gdh.goodyHuts[0])
hg_borders.set_ec_colors(gdh.borderColors[0])
hg_borders.set_fill(False)
hg_borders.set_lw(2)

p_env = PatchCollection(hg_environment.patches_list, match_original=True)
ax.add_collection(p_env)

p_borders = PatchCollection(hg_borders.patches_list, match_original=True)
ax.add_collection(p_borders)

p_goodyHuts = PatchCollection(hg_goodyHut.patches_list, match_original=True)
ax.add_collection(p_goodyHuts)

ax.autoscale_view(True, True, True)
ax.set_aspect('equal', adjustable='box')

def update(event):
    p_borders.set_visible(not p_borders.get_visible())
    fig.canvas.draw()
    fig.canvas.flush_events()
button.on_clicked(update)

def updateTurnSlider(event):
    hg_borders.set_ec_colors(gdh.borderColors[sTurn.val-1])
    hg_borders.set_fc_colors(gdh.goodyHuts[sTurn.val-1])
    collection_b = ax.collections[1]
    collection_g = ax.collections[2]
    collection_b.set_edgecolors(gdh.borderColors[sTurn.val-1])
    collection_g.set_facecolors(gdh.goodyHuts[sTurn.val-1])
    fig.canvas.draw()
    fig.canvas.flush_events()
sTurn.on_changed(updateTurnSlider)

plt.show()
