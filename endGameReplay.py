import matplotlib.pyplot as plt
import numpy as np
from utils.hexgrid import HexGrid

from matplotlib.colors import ListedColormap
from matplotlib.collections import PatchCollection
from saveFileHandler.filehandler import *
from matplotlib.widgets import Button, Slider

# TODO: Read and parse all files to memory
# TODO: From 1st save take environment
# TODO: Visualize colors with current slider situation
# TODO: Rivers, goody huts, barbarians

# TODO: Nice to have stuff in future:
#       TODO: Optional visualize units
#       TODO: List events (e.g. wars, wonders, great people)

M = 44
N = 26
hg = HexGrid(M, N, 10)
hg2 = HexGrid(M, N, 10)

f = open("data/GANDHI 20 3240 BC.Civ6Save", "rb")
data = f.read()
f.close()

map = save_to_map_json(data)
hg2.set_environment_colors(map)
hg.update_border_colors(map)
hg.set_fill(False)
hg.set_lw(2)

# our_cmap = ListedColormap(hg2.color_list)
# patches_collection = PatchCollection(hg2.patches_list, cmap=our_cmap)

fig, ax = plt.subplots()
bax = fig.add_axes([0.45, 0.91, 0.1, 0.05])
button = Button(bax, "toggle")
axTurn = plt.axes([0.1, 0.05, 0.8, 0.01]) #, facecolor=axcolor)
sTurn = Slider(axTurn, 'Turn', 1, 30, valinit=1, valstep=1)

our_cmap = ListedColormap(hg2.color_list)
p_env = PatchCollection(hg2.patches_list, cmap=our_cmap)
p_env.set_array(np.arange(len(hg2.patches_list)))
ax.add_collection(p_env)

our_cmap = ListedColormap(hg.color_list)
p_borders = PatchCollection(hg.patches_list, match_original=True)
#p_borders.set_array(np.arange(len(hg.patches_list)))



ax.add_collection(p_borders)
ax.autoscale_view(True,True,True)
ax.set_aspect('equal', adjustable='box')


def update(event):
    p_borders.set_visible(not p_borders.get_visible())
    fig.canvas.draw_idle()

button.on_clicked(update)

def updateTurnSlider(val):
    amp = sTurn.val
    # l.set_ydata(amp*np.sin(2*np.pi*freq*t))
    # fig.canvas.draw_idle()

sTurn.on_changed(updateTurnSlider)

plt.show()
