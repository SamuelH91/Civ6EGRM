# Civ6EGRM
Civilization 6 End Game Replay Map

![](endGameReplayMap.gif)

## Main features
- fileCopier.py which copies automatically all autosaves (Single/Multi) (not necessary if you have some other method to collect your save files)
- endGameReplay.py visualizes all separately (autosaved) data
  - Visualized environment similar to the minimap in the game
  - Toggle borders on/off
  - Visualized goody huts and barb camps
  
## TODOs
- Lock civ colors
- Include natural wonders
- Take actual turn number in use

- Nice to have stuff in future:
  - Optional visualize units
  - List events (e.g. wars, wonders, great people)

## Tested with
- Base game: (Single + Multi)
- Expansions: (RF + GS)
- Python 3.8.3

## Dependencies
- matplotlib
- numpy
- zlib
- struct
- watchdog
- shutil
- Pillow
- pygifsicle (to compress gifs, gifsicle.exe (64bit) included also)
- ffmpeg (included exe)

These can be installed with pip e.g. 
> - 'pip install matplotlib'

## Quickstart
1) Start civ game
1) Start file copier (set correct paths to code) (or use your own method to collect saves)
    > - Open cmd
    > - 'python runFileWatcher.py'
1) Stop it when game has reached the point and all necessary files are copied
1) Run end game replay code (check correct paths)
    > - 'python endGameReplay.py'

## Special thanks for https://github.com/lucienmaloney/civ6save-editing

