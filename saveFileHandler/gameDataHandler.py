from watchdog.utils.dirsnapshot import DirectorySnapshot
import os
from saveFileHandler.filehandler import *

class GameDataHandler():
    def __init__(self, dataFolder, fileExt=".Civ6Save"):
        self.dataFolder = dataFolder
        self.recursive = False
        self.gameData = []
        self.fileExt = fileExt

    def parseData(self):
        snapshot = DirectorySnapshot(self.dataFolder, self.recursive)
        for filePath in sorted(snapshot.paths):
            if self.fileExt == os.path.splitext(filePath)[1]:
                f = open(filePath, "rb")
                data = f.read()
                f.close()
                self.gameData.append(save_to_map_json(data))

    def getMapSize(self):
        if len(self.gameData) != 0:
            return self.gameData[0]["mapSize"]
        else:
            return None