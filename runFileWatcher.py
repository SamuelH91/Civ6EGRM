from folderWatcher.fileCopier import Watcher
import os

watchDir = os.path.expanduser("~/Documents/My Games/Sid Meier's Civilization VI/Saves/Single/auto/")
# watchDir = os.path.expanduser("~/Documents/My Games/Sid Meier's Civilization VI (Epic)/Saves/Multi/auto/")
targetDir = os.getcwd() + "/data/auto/"

if __name__ == '__main__':
    print("Starting file watcher: copying auto save files from '{}' to '{}'".format(watchDir, targetDir))
    w = Watcher(watchDir, targetDir)
    w.run()

