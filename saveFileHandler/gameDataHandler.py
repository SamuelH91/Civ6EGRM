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
# snow (mountains):		    244 70 177 41:		699483892      F4 46 B1 29    b'\xF4\x46\xB1\x29'
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
    699483892:  {"TerrainType": "snow (mountains)",         "color": np.array([173, 137, 124]) / 255},
    1204357597: {"TerrainType": "Ocean",                    "color": np.array([45, 49, 86]) / 255},
    1248885265: {"TerrainType": "Coast",                    "color": np.array([45, 89, 120]) / 255},
}

Features = {  # + goodyhut codes
    4294967295: {"FeatureType": "NoFeature",                "color": np.array([0, 0, 0])},
    1542194068: {"FeatureType": "Ice",                      "color": np.array([171, 188, 219]) / 255},
    226585075:  {"FeatureType": "Galapagos",                "color": np.array([243, 212, 1]) / 255},
    1434118760: {"FeatureType": "GoodyHut",                 "color": np.array([241, 209, 100]) / 255},
    3727362748: {"FeatureType": "BarbCamp",                 "color": np.array([183, 20, 20]) / 255},
    1523996587: {"FeatureType": "Plantation",               "color": np.array([0, 0, 0])},
    168372657:  {"FeatureType": "Farm",                     "color": np.array([0, 0, 0])},
    2475408324: {"FeatureType": "Camp",                     "color": np.array([0, 0, 0])},
    2048582848: {"FeatureType": "LumberMill",               "color": np.array([0, 0, 0])},
    1001859687: {"FeatureType": "Mine",                     "color": np.array([0, 0, 0])},
    4214473799: {"FeatureType": "Quarry",                   "color": np.array([0, 0, 0])},
    154488225:  {"FeatureType": "Pasture",                  "color": np.array([0, 0, 0])},
    578093457:  {"FeatureType": "FishingBoats",             "color": np.array([0, 0, 0])},
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

# Replay files don't appear to include colors
# window.CIV_COLORS = {
# 	America:           {city: [255, 255, 255], territory: [ 31,  51, 120]},
# 	Arabia:            {city: [146, 221,   9], territory: [ 43,  87,  45]},
# 	Assyria:           {city: [255, 168,  12], territory: [255, 243, 173]},
# 	Austria:           {city: [255, 255, 255], territory: [234,   0,   0]},
# 	Babylon:           {city: [200, 248, 255], territory: [ 43,  81,  97]},
# 	Brazil:            {city: [ 41,  83,  44], territory: [149, 221,  10]},
# 	Byzantium:         {city: [ 60,   0, 108], territory: [113, 161, 232]},
# 	Carthage:          {city: [ 80,   0, 136], territory: [204, 204, 204]},
# 	China:             {city: [255, 255, 255], territory: [  0, 148,  82]},
# 	Denmark:           {city: [239, 231, 179], territory: [108,  42,  20]},
# 	Egypt:             {city: [ 82,   0, 208], territory: [255, 251,   3]},
# 	England:           {city: [255, 255, 255], territory: [108,   2,   0]},
# 	Ethiopia:          {city: [255,  45,  45], territory: [  1,  39,  14]},
# 	France:            {city: [235, 235, 138], territory: [ 65, 141, 253]},
# 	Germany:           {city: [ 36,  43,  32], territory: [179, 177, 184]},
# 	Greece:            {city: [ 65, 141, 253], territory: [255, 255, 255]},
# 	India:             {city: [255, 153,  49], territory: [ 18, 135,   6]},
# 	Indonesia:         {city: [158,  46,  28], territory: [110, 210, 217]},
# 	Japan:             {city: [184,   0,   0], territory: [255, 255, 255]},
# 	Korea:             {city: [255,   0,   0], territory: [ 26,  32,  96]},
# 	Mongolia:          {city: [255, 120,   0], territory: [ 81,   0,   8]},
# 	Morocco:           {city: [ 39, 178,  79], territory: [144,   2,   0]},
# 	Persia:            {city: [245, 230,  55], territory: [176,   7,   3]},
# 	Poland:            {city: [ 56,   0,   0], territory: [244,   5,   0]},
# 	Polynesia:         {city: [255, 255,  74], territory: [217,  88,   0]},
# 	Portugal:          {city: [  3,  20, 124], territory: [255, 255, 255]},
# 	Rome:              {city: [239, 198,   0], territory: [ 70,   0, 118]},
# 	Russia:            {city: [  0,   0,   0], territory: [238, 238, 238]},
# 	Siam:              {city: [176,   7,   3], territory: [245, 230,  55]},
# 	Songhai:           {city: [ 90,   0,   9], territory: [213, 145,  19]},
# 	Spain:             {city: [244, 168, 168], territory: [ 83,  26,  26]},
# 	Sweden:            {city: [248, 246,   2], territory: [  7,   7, 165]},
# 	Venice:            {city: [255, 254, 215], territory: [102,  33, 161]},
# 	'The Aztecs':      {city: [136, 238, 212], territory: [161,  57,  34]},
# 	'The Celts':       {city: [147, 169, 255], territory: [ 21,  91,  62]},
# 	'The Huns':        {city: [ 69,   0,   3], territory: [179, 177, 163]},
# 	'The Inca':        {city: [  6, 159, 119], territory: [255, 184,  33]},
# 	'The Iroquois':    {city: [251, 201, 129], territory: [ 65,  86,  86]},
# 	'The Maya':        {city: [ 23,  62,  65], territory: [197, 140,  98]},
# 	'The Netherlands': {city: [255, 255, 255], territory: [255, 143,   0]},
# 	'The Ottomans':    {city: [ 18,  82,  30], territory: [247, 248, 199]},
# 	'The Shoshone':    {city: [ 24, 239, 206], territory: [ 73,  58,  45]},
# 	'The Zulus':       {city: [106,  49,  24], territory: [255, 231, 213]}
# }

cityColors = np.array([
[255, 255, 255],
[146, 221,   9],
[255, 168,  12],
[255, 255, 255],
[200, 248, 255],
[ 41,  83,  44],
[ 60,   0, 108],
[ 80,   0, 136],
[255, 255, 255],
[239, 231, 179],
[ 82,   0, 208],
[255, 255, 255],
[255,  45,  45],
[235, 235, 138],
[ 36,  43,  32],
[ 65, 141, 253],
[255, 153,  49],
[158,  46,  28],
[184,   0,   0],
[255,   0,   0],
[255, 120,   0],
[ 39, 178,  79],
[245, 230,  55],
[ 56,   0,   0],
[255, 255,  74],
[  3,  20, 124],
[239, 198,   0],
[  0,   0,   0],
[176,   7,   3],
[ 90,   0,   9],
[244, 168, 168],
[248, 246,   2],
[255, 254, 215],
[136, 238, 212],
[147, 169, 255],
[ 69,   0,   3],
[  6, 159, 119],
[251, 201, 129],
[ 23,  62,  65],
[255, 255, 255],
[ 18,  82,  30],
[ 24, 239, 206],
[106,  49,  24],
])

civColors = np.array([
[ 31,  51, 120],
[ 43,  87,  45],
[255, 243, 173],
[234,   0,   0],
[ 43,  81,  97],
[149, 221,  10],
[113, 161, 232],
[204, 204, 204],
[  0, 148,  82],
[108,  42,  20],
[255, 251,   3],
[108,   2,   0],
[  1,  39,  14],
[ 65, 141, 253],
[179, 177, 184],
[255, 255, 255],
[ 18, 135,   6],
[110, 210, 217],
[255, 255, 255],
[ 26,  32,  96],
[ 81,   0,   8],
[144,   2,   0],
[176,   7,   3],
[244,   5,   0],
[217,  88,   0],
[255, 255, 255],
[ 70,   0, 118],
[238, 238, 238],
[245, 230,  55],
[213, 145,  19],
[ 83,  26,  26],
[  7,   7, 165],
[102,  33, 161],
[161,  57,  34],
[ 21,  91,  62],
[179, 177, 163],
[255, 184,  33],
[ 65,  86,  86],
[197, 140,  98],
[255, 143,   0],
[247, 248, 199],
[ 73,  58,  45],
[255, 231, 213]]
) / 255

class GameDataHandler():
    def __init__(self, dataFolder, fileExt=".Civ6Save"):
        self.dataFolder = dataFolder
        self.recursive = False
        self.tileData = []
        self.cityData = []
        self.borderColors = []
        self.cityColors = []
        self.envColors = []
        self.riverColors = []
        self.goodyHuts = []
        self.fileExt = fileExt
        self.pColors = civColors
        self.X = -1
        self.Y = -1
        self.neighbours_list = []

    def parseData(self):
        snapshot = DirectorySnapshot(self.dataFolder, self.recursive)
        for filePath in sorted(snapshot.paths):
            if self.fileExt == os.path.splitext(filePath)[1]:
                f = open(filePath, "rb")
                data = f.read()
                f.close()
                mainDecompressedData = decompress(data)
                self.tileData.append(save_to_map_json(mainDecompressedData))
                self.cityData.append(getCityData(mainDecompressedData))

    def calculateOtherStuff(self):
        for turn in self.tileData:
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
            self.goodyHuts.append(np.copy(goodyHutsAtTurn))
            # count = 0
            # for color in goodyHutsAtTurn:
            #     if color[2] > 0:
            #         count += 1

    def calculateEnvColors(self):
        if len(self.tileData) != 0:
            turn = self.tileData[0]
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

    def calculateRiverColors(self):
        if len(self.tileData) != 0:
            turn = self.tileData[0]
            for ii, tile in enumerate(turn["tiles"]):
                RiverBorders = tile["RiverBorders"]
                if RiverBorders > 0:
                    RiverBitMap = tile["RiverBitMap"]
                    for ii in range(6):
                        if RiverBitMap >> ii & 1:
                            self.riverColors.append(np.array((45, 89, 120, 255)) / 255)
                        else:
                            self.riverColors.append(np.zeros(4, ))
                else:
                    for jj in range(6):
                        self.riverColors.append(np.zeros(4, ))

    def calculateBorderColors(self, outsideBordersOnly=False):
        self.X, self.Y = self.getMapSize()
        if outsideBordersOnly:
            for ii in range(self.X*self.Y):
                self.neighbours_list.append(self.getNeighbourIndexes(ii))
        for turn in self.tileData:
            borderColorsAtTurn = []
            for ii, tile in enumerate(turn["tiles"]):
                playerID = self.getPlayerID(tile)
                if playerID >= 0:
                    if outsideBordersOnly:
                        for neighbour in self.neighbours_list[ii]:
                            if neighbour < self.X*self.Y:
                                neighbourID = self.getPlayerID(turn["tiles"][neighbour])
                                if neighbourID == playerID:
                                    borderColorsAtTurn.append(np.zeros(4, ))
                                else:
                                    borderColorsAtTurn.append(np.append(self.pColors[playerID, :], 0.9))
                            else:
                                borderColorsAtTurn.append(np.append(self.pColors[playerID, :], 0.9))
                    else:
                        borderColorsAtTurn.append(np.append(self.pColors[playerID, :], 0.9))
                else:
                    if outsideBordersOnly:
                        for jj in range(6):
                            borderColorsAtTurn.append(np.zeros(4, ))
                    else:
                        borderColorsAtTurn.append(np.zeros(4, ))

            self.borderColors.append(borderColorsAtTurn)

    def calculateCityColors(self):
        cityColorsAtTurnEmpty = []
        for ii in range(self.X*self.Y):
            cityColorsAtTurnEmpty.append(np.zeros(4, ))
        for turn in self.cityData:
            cityColorsAtTurn = cityColorsAtTurnEmpty
            for city in turn["cities"]:
                cityColorsAtTurn[city["LocationIdx"]] = np.append(self.pColors[city["CivIndex"], :], 0.9)
            self.cityColors.append(np.copy(cityColorsAtTurn))
            # count = 0
            # for color in cityColorsAtTurn:
            #     if color[3] > 0:
            #         count += 1

    def getPlayerID(self, tile):
        if tile["OwnershipBuffer"] >= 64:
            tileBufferData = tile["buffer"]
            return tileBufferData[-5]
        else:
            return -1

    def getMapSize(self):
        if len(self.tileData) != 0:
            return self.tileData[0]["mapSize"][0], self.tileData[0]["mapSize"][1]
        else:
            return None

    def getTurnCount(self):
        return len(self.tileData)

    def index2XY(self, index):
        y = int(np.floor(index / self.X))
        x = int(index % self.X)
        if 0 <= y < self.Y:
            return x, y
        else:
            return self.X, self.Y

    #   5   0
    # 4   x   1
    #   3   2
    def getNeighbourIndexes(self, index):
        neighbours = np.array([index]*6)
        nanvalue = self.X*self.Y
        x, y = self.index2XY(index)

        if y % 2 == 0:
            offsets = np.array([self.X, 1, -self.X, -self.X-1, -1, self.X-1])
        else:
            offsets = np.array([self.X+1, 1, -self.X+1, -self.X, -1, self.X])

        neighbours += offsets
        if y == self.Y - 1:
            # Top row, -> no 0, 5 neighbours
            neighbours[0] = nanvalue
            neighbours[5] = nanvalue
        elif y == 0:
            # Bottom row, -> no 2, 3 neighbours
            neighbours[2] = nanvalue
            neighbours[3] = nanvalue
        if x % self.X == 0:
            # First column, [4] += self.X
            neighbours[4] += self.X
            if (0 < y < self.Y - 1) and (y % 2 == 0):
                # If not top/bottom row, and even row -> [3/5] += self.X
                neighbours[3] += self.X
                neighbours[5] += self.X
        elif x % self.X == self.X - 1:
            # Last column, [1] -= self.X
            neighbours[1] -= self.X
            if (0 < y < self.Y - 1) and (y % 2 == 1):
                # If not top/bottom row, and uneven row -> [0/2] -= self.X
                neighbours[0] -= self.X
                neighbours[2] -= self.X
        return neighbours

    def randomCivColors(self, N):
        oldColors = self.pColors
        self.pColors = np.random.rand(N, 3)
        for borderColorsAtTurn in self.borderColors:
            for ii, color in enumerate(borderColorsAtTurn):
                idx = np.where((oldColors[:, 0] == color[0]) & (oldColors[:, 1] == color[1]) & (oldColors[:, 2] == color[2]))[0]
                if len(idx) > 0:
                    borderColorsAtTurn[ii] = np.append(self.pColors[idx], 0.9)
