# Civ6EGRM
Civilization 6 End Game Replay Map

![Image 1](Picture/SmallMapEnvOnly.PNG)
![Image 2](Picture/BigMapEnvOnly.PNG)
![Image 3](Picture/BigMapWithRandomColorBorders.PNG)
![Image 4](Picture/BigMapWithRandomColorBordersFewTurnsLater.PNG)

## Main features
- fileCopier.py which copies automatically all autosaves (Single/Multi)
- endGameReplay.py visualizes all separately (autosaved) data
  - Visualized environment similar to the minimap in the game
  - Toggle borders on/off
  - Visualized goody huts and barb camps
  
## TODOs
- Rivers, + improve: goody huts, barbarians, icebergs
- Lock civ colors and city visualization
- Include more natural wonders
- Take actual turn number in use

- Nice to have stuff in future:
  - Optional visualize units
  - List events (e.g. wars, wonders, great people)

## Tested with
- Base game: (Single + Multi)
- Python 3.8.3

## Dependencies
- matplotlib
- numpy
- zlib
- struct
- watchdog
- shutil

These can be installed with pip e.g. 
> - 'pip install matplotlib'

## Quickstart
1) Start civ game
1) Start file copier (set correct paths to code)
    > - Open cmd
    > - 'python runFileWatcher.py'
1) Stop it when game has reached the point and all necessary files are copied
1) Run end game replay code (check correct paths)
    > - 'python endGameReplay.py'


