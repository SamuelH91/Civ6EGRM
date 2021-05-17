import wget
import os

base_url = "https://raw.githubusercontent.com/SamuelH91/Civ6EGRM/master/"
files = [
    "endGameReplay.bat",
    "endGameReplay.py",
    "nonGitUpdater.py",
    "folderWatcher/__init__.py",
    "folderWatcher/autoRunEndGameReplayHere.bat",
    "folderWatcher/fileCopier.py",
    "saveFileHandler/__init__.py",
    "saveFileHandler/civColors.py",
    "saveFileHandler/civLocalization.py",
    "saveFileHandler/features.py",
    "saveFileHandler/filehandler.py",
    "saveFileHandler/gameDataHandler.py",
    "utils/__init__.py",
    "utils/binaryconvert.py",
    "utils/hexagon.py",
    "utils/hexgrid.py",
]

print(f"This file should be run from the root of the Civ6EGRM folder!!!")
print(f"Updating common files without git: Use git for to be sure that all necessary files are up-to-date!")

for file in files:
    print(f"\nDownloading file '{file}'")
    path = os.path.dirname(file)
    if path:
        os.makedirs(path, exist_ok=True)
    if os.path.exists(file):  # remove old first
        os.remove(file)
    wget.download(base_url + file, file)

print(f"\nUpdate 'runFileWatcher.py' (contains your path) manually if needed!")
input("Press any key to close...")