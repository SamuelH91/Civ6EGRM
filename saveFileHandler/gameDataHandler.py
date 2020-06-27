from watchdog.utils.dirsnapshot import DirectorySnapshot
import os
from saveFileHandler.filehandler import *

# Terrain types:
# grassland: 				48 198 231 131:		2213004848     30 C6 E7 83    b'\x30\xC6\xE7\x83'
# grassland (hills):		112 12 157 110: 	1855786096     70 0C 9D 6E    b'\x70\x0C\x9D\x6E'
# grassland (mountains):	51 180 131 95:		1602466867     33 B4 83 5F    b'\x33\xB4\x83\x5F'
# plains: 				    94 134 230 251: 	4226188894     5E 86 E6 FB    b'\x94\x86\xE6\xFB'
# plains (hills): 		    158 100 206 230:	3872285854     9E 64 CE E6    b'\x9E\x64\xCE\xE6'
# plains (mountains):		240 168 185 163:	2746853616     F0 A8 B9 A3    b'\xF0\xA8\xB9\xA3'
# desert: 				    44 10 168 229:		3852995116     2C 0A A8 E5    b'\x2C\x0A\xA8\xE5'
# desert (hills): 		    179 52 65 185:		3108058291     B3 34 41 B9    b'\xB3\x34\x41\xB9'
# desert (mountains):   	249 190 144 84:		1418772217     F9 BE 90 54    b'\xF9\xBE\x90\x54
# tundra: 				    171 158 242 72:		1223859883     AB 9E F2 48    b'\xAB\x9E\xF2\x48'
# tundra (hills):			246 176 98 235:		3949113590     F6 B0 62 EB    b'\xF6\xB0\x62\xEB'
# tundra (mountains):		189 221 73 223:		3746160061     BD DD 49 DF    b'\xBD\xDD\x49\xDF'
# snow: 					15 132 234 103:		1743422479     0F 84 EA 67    b'\x0F\x84\xEA\x67'
# snow (hills): 			128 18 3 229:		3842183808     80 12 03 E5    b'\x80\x12\x03\xE5'
# snow (mountains):		    244 70 177 41:		699483872      E0 46 B1 29    b'\xE0\x46\xB1\x29'
# Ocean: 					221 9 201 71:		1204357597     DD 09 C9 47    b'\xDD\x09\xC9\x47'
# Coast: 					17 122 112 74:		1248885265     11 7A 70 4A    b'\x11\x7A\x70\x4A'

Terrains = {
    2213004848: {"TerrainType": "grassland",                "color": np.array([103, 125, 48]) / 255},
    1855786096: {"TerrainType": "grassland (hills)",        "color": np.array([103, 125, 48]) / 255},
    1602466867: {"TerrainType": "grassland (mountains)",    "color": np.array([173, 137, 124]) / 255},
    4226188894: {"TerrainType": "plains",                   "color": np.array([159, 159, 53]) / 255},
    3872285854: {"TerrainType": "plains (hills)",           "color": np.array([159, 159, 53]) / 255},
    2746853616: {"TerrainType": "plains (mountains)",       "color": np.array([173, 137, 124]) / 255},
    3852995116: {"TerrainType": "desert",                   "color": np.array([236, 196, 111]) / 255},
    3108058291: {"TerrainType": "desert (hills)",           "color": np.array([236, 196, 111]) / 255},
    1418772217: {"TerrainType": "desert (mountains)",       "color": np.array([173, 137, 124]) / 255},
    1223859883: {"TerrainType": "tundra",                   "color": np.array([171, 170, 139]) / 255},
    3949113590: {"TerrainType": "tundra (hills)",           "color": np.array([171, 170, 139]) / 255},
    3746160061: {"TerrainType": "tundra (mountains)",       "color": np.array([173, 137, 124]) / 255},
    1743422479: {"TerrainType": "snow",                     "color": np.array([204, 223, 243]) / 255},
    3842183808: {"TerrainType": "snow (hills)",             "color": np.array([204, 223, 243]) / 255},
    699483872:  {"TerrainType": "snow (mountains)",         "color": np.array([173, 137, 124]) / 255},
    1204357597: {"TerrainType": "Ocean",                    "color": np.array([45, 49, 86]) / 255},
    1248885265: {"TerrainType": "Coast",                    "color": np.array([45, 89, 120]) / 255},
}

Features = {
    4294967295: {"FeatureType": "NoFeature",                "color": np.array([0, 0, 0])},
    1542194068: {"FeatureType": "Ice",                      "color": np.array([171, 188, 219]) / 255},
    226585075:  {"FeatureType": "Galapagos",                "color": np.array([243, 212, 1]) / 255},
    1434118760: {"FeatureType": "GoodyHut",                 "color": np.array([241, 209, 100]) / 255},
    3727362748: {"FeatureType": "BarbCamp",                 "color": np.array([183, 20, 20]) / 255},
}
# Features:
# No feature: 			    255 255 255 255:	FF FF FF FF
# Rainforest:				57 84 17 233:		39 54 11 E9
# Woods:					68 9 34 10: 		44 09 22 0A
# March (grassland only):	195 89 85 35:		C3 59 55 23
# Oasis (desert only):	    163 83 31 98:		A3 53 1F 62
# Floodlands(desert only):  38 119 181 82:		26 77 B5 52
# Ice (ocean/coast):		148 3 236 91:		94 03 EC 5B
#
# Goody hut: 									EA CD 58 15		1434118760
# Barb: ‭										BC 0A 2B DE		DE 2B 0A BC		3727362748
#
# Terrain2?:
# Sea:					    255 255 255 255: 	FF FF FF FF
# Land:					    197 141 5 214:		C5 8D 05 D6
# Snow:					    234 205 88 21:		EA CD 58 15

class GameDataHandler():
    def __init__(self, dataFolder, fileExt=".Civ6Save"):
        self.dataFolder = dataFolder
        self.recursive = False
        self.gameData = []
        self.borderColors = []
        self.envColors = []
        self.goodyHuts = []
        self.fileExt = fileExt
        self.pColors = np.random.rand(20, 3)

    def parseData(self):
        snapshot = DirectorySnapshot(self.dataFolder, self.recursive)
        for filePath in sorted(snapshot.paths):
            if self.fileExt == os.path.splitext(filePath)[1]:
                f = open(filePath, "rb")
                data = f.read()
                f.close()
                self.gameData.append(save_to_map_json(data))

    def calculateOtherStuff(self):
        for turn in self.gameData:
            goodyHutsAtTurn = []
            for ii, tile in enumerate(turn["tiles"]):
                terrainType = tile["TerrainType"]
                featureType = tile["FeatureType"]
                GoodyHut = tile["GoodyHut"]
                try:
                    if Features[GoodyHut]["FeatureType"] == "GoodyHut" or \
                            Features[GoodyHut]["FeatureType"] == "BarbCamp":
                        goodyHutsAtTurn.append(Features[GoodyHut]["color"])
                    else:
                        goodyHutsAtTurn.append(np.zeros(4, ))
                except:
                    print("x: {}, y: {}, goodyHut: {}".format(tile["x"], tile["y"], GoodyHut))
                    goodyHutsAtTurn.append(np.zeros(4,))
                self.goodyHuts.append(goodyHutsAtTurn)

    def calculateEnvColors(self):
        if len(self.gameData) != 0:
            turn = self.gameData[0]
            for ii, tile in enumerate(turn["tiles"]):
                terrainType = tile["TerrainType"]
                featureType = tile["FeatureType"]
                try:
                    if (Terrains[terrainType]["TerrainType"] == "Ocean" or
                            Terrains[terrainType]["TerrainType"] == "Coast"):
                        if Features[featureType]["FeatureType"] == "Ice":
                            self.envColors.append(Features[featureType]["color"])
                        else:
                            self.envColors.append(Terrains[terrainType]["color"])
                    else:
                        self.envColors.append(Terrains[terrainType]["color"])
                except:
                    print("x: {}, y: {}, type: {}".format(tile["x"], tile["y"], terrainType))
                    self.envColors.append(np.zeros(3,))

    def calculateBorderColors(self):
        for turn in self.gameData:
            borderColorsAtTurn = []
            for ii, tile in enumerate(turn["tiles"]):
                if tile["OwnershipBuffer"] >= 64:
                    tileBufferData = tile["buffer"]
                    playerID = tileBufferData[-5]
                    borderColorsAtTurn.append(np.append(self.pColors[playerID, :], 0.9))
                else:
                    borderColorsAtTurn.append(np.zeros(4, ))
            self.borderColors.append(borderColorsAtTurn)

    def getMapSize(self):
        if len(self.gameData) != 0:
            return self.gameData[0]["mapSize"][0], self.gameData[0]["mapSize"][1]
        else:
            return None

    def getTurnCount(self):
        return len(self.gameData)
