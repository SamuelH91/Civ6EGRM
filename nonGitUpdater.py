import wget
import os
import sys

updater_file = "nonGitUpdater.py"
base_url = "https://raw.githubusercontent.com/SamuelH91/Civ6EGRM/master/"
files = [
    "endGameReplay.bat",
    "endGameReplay.py",
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

if len(sys.argv) < 2:
    print(f"This file should be run from the root of the Civ6EGRM folder!!!")
    print(f"Updating common files without git: Use git for to be sure that all necessary files are up-to-date!")
    print(f"Updating this file first")
    if os.path.exists(updater_file):  # remove old first
        os.remove(updater_file)
    wget.download(base_url + updater_file, updater_file)
    new_args = sys.argv[1:]
    new_args.append("UpdateOtherFiles")
    os.execl(sys.executable, 'python', __file__, *new_args)  # Restart this script with additional arg
else:
    print(f"\nUpdating other files next:")

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