from watchdog.utils.dirsnapshot import DirectorySnapshot
import os
from saveFileHandler.filehandler import *
from saveFileHandler.features import Terrains, Features
import time
import multiprocessing as mp
import pyqtgraph as pg
import copy
from collections import defaultdict
import numpy as np
from saveFileHandler.civColors import CIV_LEADER_COLORS, COLORS_PRISM, CIV_OVERFLOW_COLORS,\
    CS_COLOR_MAP, CS_TYPES, CS_UNICODE_MAP  # CIV_COLORS
try:
    from saveFileHandler.civLocalization import CIV_LEADER_NAMES, CIV_NAMES, CITY_NAMES
    civLocalizationImportSuccess = True
except:
    civLocalizationImportSuccess = False
    pass
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
)
civColors = np.concatenate((civColors, np.random.rand(213, 3) * 255))
# Usually Free city civ index is 62, so in theory there can't be more than 62 civs major/minor
civColors[62, :] = np.array([25, 25, 25])
civColors[255, :] = np.array([0, 0, 255])  # sea level rise when no other owner
civColorsInner = np.copy(civColors)
civColorsMinor = np.copy(civColors)

civColorsPen = []
civColorsBrush = []
civColorsPenInner = []
civColorsBrushInner = []
civColorsBrushMinor = []
for color in civColors:
    qcolor = pg.mkColor(color)
    civColorsPen.append(pg.mkPen(qcolor, width=3))
    civColorsPenInner.append(pg.mkPen(qcolor, width=3))
    civColorsBrush.append(pg.mkBrush(qcolor))
    civColorsBrushInner.append(pg.mkBrush(qcolor))
    civColorsBrushMinor.append(pg.mkBrush(qcolor))

riverPen = pg.mkPen(pg.mkColor(np.array((45, 89, 120, 255))), width=4)

emptyBrush = pg.mkBrush(pg.mkColor(np.zeros(4, )))
blackBrush = pg.mkBrush(pg.mkColor(np.zeros(3,)))
emptyPen = pg.mkPen(pg.mkColor(np.zeros(4, )))
blackPen = pg.mkPen(pg.mkColor(np.array((24, 24, 24))), width=3)

FREE_CITY_IDX = 62

def parseLeader(leaderIn):
    cityState = False
    leader = leaderIn
    if leader[:10] == "MINOR_CIV_":
        cityState = True
        leader = "City State"
    else:
        leader = " ".join(x.capitalize() for x in leader.split("_"))
    return leader, cityState


def map_civ_colors(civdata):
    added_colors = []
    print(f"Civilization colors are determined by first-come-first-serve")
    print(f"according to the jerseys used in Prismatic - Color and Jersey Overhaul mod (version 28.01.2021)")
    print(f"https://steamcommunity.com/sharedfiles/filedetails/?id=1661785509")
    for i, civ in enumerate(civdata):
        try:
            colorset = False
            for ii in range(4):
                color = COLORS_PRISM[CIV_LEADER_COLORS[civ][ii*2]]
                colorInner = COLORS_PRISM[CIV_LEADER_COLORS[civ][ii*2+1]]
                if color not in added_colors:
                    colorset = True
                    added_colors.append(color)
                    print(f"{civ} border color set to {color}/{colorInner} (option #{ii})")
                    break
            if not colorset:
                for jj in range(int(len(CIV_OVERFLOW_COLORS)/2)):
                    color = COLORS_PRISM[CIV_OVERFLOW_COLORS[jj * 2]]
                    colorInner = COLORS_PRISM[CIV_OVERFLOW_COLORS[jj * 2 + 1]]
                    if color not in added_colors:
                        added_colors.append(color)
                        print(f"{civ} border color set to {color}/{colorInner} (overflow option #{jj})")
                        break
        except:
            for jj in range(int(len(CIV_OVERFLOW_COLORS) / 2)):
                color = COLORS_PRISM[CIV_OVERFLOW_COLORS[jj * 2]]
                colorInner = COLORS_PRISM[CIV_OVERFLOW_COLORS[jj * 2 + 1]]
                if color not in added_colors:
                    added_colors.append(color)
                    print(f"{civ} border color set to {color}/{colorInner} (overflow option #{jj})")
                    break
            # continue
        qcolor = pg.mkColor(color)
        qcolorInner = pg.mkColor(colorInner)
        civColors[i] = color
        civColorsInner[i] = colorInner
        civColorsPen[i] = pg.mkPen(qcolor, width=3)
        civColorsBrush[i] = pg.mkBrush(qcolor)
        civColorsPenInner[i] = pg.mkPen(colorInner, width=4)
        civColorsBrushInner[i] = pg.mkBrush(qcolorInner)

        if len(civ) > 10:
            if civ[:10] == "MINOR_CIV_":
                try:
                    city_state = " ".join(x.capitalize() for x in civ[10:].split("_"))
                    colorMinor = COLORS_PRISM[CS_COLOR_MAP[CS_TYPES[city_state]]]
                    qcolorMinor = pg.mkColor(colorMinor)
                except:
                    print("City state not found from mapping: {}".format(civ))
                    qcolorMinor = blackBrush
                    colorMinor = np.zeros(3,)
                civColorsBrushMinor[i] = pg.mkBrush(qcolorMinor)
                civColorsMinor[i] = colorMinor


def fileWorker(idx, filePath):
    f = open(filePath, "rb")
    data = f.read()
    f.close()
    mainDecompressedData = decompress(data)
    civData = []
    leaderData = []
    notifications = []
    diploStates = []
    wars = []
    if idx == 0:
        civData, leaderData = get_civ_data(data)
    # map_civ_colors(civdata)
    tileData = save_to_map_json(mainDecompressedData, idx)
    cityData = getCityData(mainDecompressedData)
    checkCityTileOwner(cityData, tileData)
    reCityData = reorderedCityData(cityData)
    # notifications = getNotifications(mainDecompressedData)
    cityNameData = getCityNameData(mainDecompressedData, idx)
    combineNames(cityData, reCityData, cityNameData)
    getCityLocNames(cityData)
    diploStates = getDiploStates(mainDecompressedData, idx)
    wars = getWars(mainDecompressedData, idx)
    return idx, tileData, cityData, civData, leaderData, notifications, diploStates, wars


def getPlayerID(tile):
    if tile["OwnershipBuffer"] >= 64:
        tileBufferData = tile["buffer"]
        return tileBufferData[-5]
    else:
        return -1


def checkCityTileOwner(cityData, tileData):
    for city in cityData["cities"]:
        pId = getPlayerID(tileData["tiles"][city["LocationIdx"]])
        city["tileOwner"] = pId


def combineNames(cityData, reCityData, cityNameData):
    count = 0
    # Free cities first from the end of the list
    for city in reversed(reCityData):
        if city["tileOwner"] == FREE_CITY_IDX:
            cityData["cities"][city["OldIdx"]]["cityNameData"] = cityNameData["cityNames"][-count]
            count += 1
        else:
            break
    for idx, city in enumerate(reCityData[:-count]):
        cityData["cities"][city["OldIdx"]]["cityNameData"] = cityNameData["cityNames"][idx]


def getCityLocNames(cityData):
    for city in cityData["cities"]:
        if "cityNameData" in city:
            if city["cityNameData"]["Orig"]:
                cityKey = "_".join(x.upper() for x in city["CityName"].split(" "))
                if cityKey in CITY_NAMES:
                    city["cityLocData"] = CITY_NAMES[cityKey]


def reorderedCityData(cityData):
    reorderedCityData = []
    usedCities = []
    for idx, city in enumerate(cityData["cities"]):
        CityName = city["CityName"]
        cityCopy = city.copy()
        cityCopy["OldIdx"] = idx
        # If city exists already remove it from list
        if CityName in usedCities:
            for idx2, insertedCity in enumerate(reorderedCityData):
                if insertedCity["CityName"] == CityName:
                    reorderedCityData.pop(idx2)
                    break
        else:
            usedCities.append(CityName)
        # Find a slot where to insert
        for idx2, insertedCity in enumerate(reorderedCityData):
            insertOrReplace = compareCity(city, insertedCity)
            if insertOrReplace > 0:
                reorderedCityData.insert(idx2, cityCopy)
                break
            elif insertOrReplace == 0:
                reorderedCityData[idx2] = cityCopy
                break
        else:
            reorderedCityData.append(cityCopy)
    return reorderedCityData

def compareCity(city1, city2):
    CivIndex = city1["CivIndex"]
    CivCityOrderIdx = city1["CivCityOrderIdx"]
    tileOwner = city1["tileOwner"]
    CivIndex2 = city2["CivIndex"]
    CivCityOrderIdx2 = city2["CivCityOrderIdx"]
    tileOwner2 = city2["tileOwner"]

    # City 1 is not free city and city 2 is
    if tileOwner != FREE_CITY_IDX and tileOwner2 == FREE_CITY_IDX:
        return 1
    # City 1 is free city and city 2 is not
    elif tileOwner == FREE_CITY_IDX and tileOwner2 != FREE_CITY_IDX:
        return -1
    # Both are either free city or not #TODO: Check that the order is not time related with Free Cities
    else:
        # Civ index priority # 1
        if CivIndex < CivIndex2:
            return 1
        elif CivIndex > CivIndex2:
            return -1
        else:
            # City index priority # 1
            if CivCityOrderIdx < CivCityOrderIdx2:
                return 1
            elif CivCityOrderIdx > CivCityOrderIdx2:
                return -1
            # Both are same replace old index (player has lost an existing city)
            else:
                return 0

class GameDataHandler():
    def __init__(self, dataFolder, fileExt=".Civ6Save"):
        self.dataFolder = dataFolder
        self.recursive = False
        self.tileData = []
        self.cityData = []
        self.civData = []
        self.leaderData = []
        self.notifications = []
        self.diploStates = []
        self.wars = []
        self.borderColors = []
        self.borderColorsInner = []
        self.borderColorsSC = []
        self.cityColors = []
        self.envColors = []
        self.riverColors = []
        self.goodyHuts = []
        self.fileExt = fileExt
        self.pColors = civColors
        self.X = -1
        self.Y = -1
        self.neighbours_list = []
        self.majorCivs = 0
        self.minorCivs = 0
        self.cityCounts = []
        self.razedCityLocs = []
        self.civ_text = []
        self.civHexaCounts = []
        self.playersAlive = []
        self.minorOrigos = {}
        self.minorCivTypes = {}
        self.calculatingCivNames = False

    def parseData(self):
        snapshot = DirectorySnapshot(self.dataFolder, self.recursive)
        count = 0
        filePaths = []
        for filePath in sorted(snapshot.paths):
            if self.fileExt == os.path.splitext(filePath)[1]:
                count += 1
                filePaths.append(filePath)
        self.tileData = [None] * count
        self.cityData = [None] * count
        self.civData = [None] * count
        self.leaderData = [None] * count
        self.notifications = [None] * count
        self.diploStates = [None] * count
        self.wars = [None] * count
        t0 = time.time()
        pool = mp.Pool()
        for ii, filePath in enumerate(filePaths):
            pool.apply_async(fileWorker, args=(ii, filePath), callback=self.saveResult)
            # self.saveResult(fileWorker(ii, filePath))  # debugging single thread
        pool.close()
        pool.join()
        # unique_notifications = self.checkUniqueNotifications()

        self.X, self.Y = self.getMapSize()
        self.neighbours_list = []
        for ii in range(self.X*self.Y):
            self.neighbours_list.append(self.getNeighbourIndexes(ii))

        self.calcMajorCivs()
        self.calcCityCounts()
        self.calcRazedCitys()
        self.calculateCivHexas()
        self.calcPlayersAlive()
        self.calculateCityStateOrigos()
        self.calcIncrementalWars()
        print("Total time {} s for data parsing from {} files".format(time.time() - t0, count))

    def checkUniqueNotifications(self):
        unique_notifications = []
        for turn in self.notifications:
            for notification in turn:
                if notification["NotiName"] not in unique_notifications:
                    unique_notifications.append(notification["NotiName"])
        return unique_notifications

    def saveResult(self, result):
        self.tileData[result[0]] = result[1]
        self.cityData[result[0]] = result[2]
        self.civData[result[0]] = result[3]
        self.leaderData[result[0]] = result[4]
        self.notifications[result[0]] = result[5]
        self.diploStates[result[0]] = result[6]
        self.wars[result[0]] = result[7]

    def calcCityCounts(self):
        self.cityCounts = []
        for i, turn in enumerate(self.cityData):
            cityCounts = [0] * self.majorCivs
            usedCities = {}
            for city in turn["cities"]:
                cityCounts[city["CivIndex"]] += 1
                if city["CityName"] not in usedCities:
                    usedCities[city["CityName"]] = city["CivIndex"]
                else:
                    cityCounts[usedCities[city["CityName"]]] -= 1
            self.cityCounts.append(cityCounts)

    def calcRazedCitys(self):
        self.razedCityLocs = []
        cityLocsHistory = []
        # Add 1st turn city locs to history
        for city in self.cityData[0]["cities"]:
            loc = city["LocationIdx"]
            if loc not in cityLocsHistory:
                cityLocsHistory.append(loc)
        self.razedCityLocs.append([])
        for i, turn in enumerate(self.cityData[1:]):
            razedCitysAtTurn = []
            for oldCityLoc in cityLocsHistory:
                city_exists_still = False
                for city in turn["cities"]:
                    if oldCityLoc == city["LocationIdx"]:
                        city_exists_still = True
                        break
                if not city_exists_still:
                    razedCitysAtTurn.append(oldCityLoc)
            for city in turn["cities"]:
                loc = city["LocationIdx"]
                if loc not in cityLocsHistory:
                    cityLocsHistory.append(loc)
            self.razedCityLocs.append(razedCitysAtTurn)

    def calculateOtherStuff(self):
        t0 = time.time()
        for turnIdx, turn in enumerate(self.tileData):
            goodyHutsAtTurn = []
            count = 0
            for ii, tile in enumerate(turn["tiles"]):
                terrainType = tile["TerrainType"]
                featureType = tile["FeatureType"]
                GoodyHut = tile["GoodyHut"]
                try:
                    if Features[GoodyHut]["FeatureType"] == "GoodyHut" or \
                            Features[GoodyHut]["FeatureType"] == "BarbCamp":
                        goodyHutsAtTurn.append(Features[GoodyHut]["color"])
                    else:
                        goodyHutsAtTurn.append(emptyBrush)
                except:
                    count += 1
                    print("turnIdx: {}, errorCount: {}, x: {}, y: {}, goodyHut: {}".format(turnIdx, count, tile["x"], tile["y"], GoodyHut))
                    goodyHutsAtTurn.append(emptyBrush)
            self.goodyHuts.append(copy.copy(goodyHutsAtTurn))
        print("Total time for goody huts / barb camps: {}".format(time.time() - t0))

    def calculateEnvColors(self):
        t0 = time.time()
        if len(self.tileData) != 0:
            turn = self.tileData[0]
            count = 0
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
                    count += 1
                    print("errorCount: {}, x: {}, y: {}, terrainType: {}, featureType: {}".format(count, tile["x"], tile["y"], terrainType, featureType))
                    self.envColors.append(pg.mkBrush(pg.mkColor(np.zeros(3,))))
        print("Total time for environment colors: {}".format(time.time() - t0))

    def calculateRiverColors(self, lw=4):
        t0 = time.time()
        if len(self.tileData) != 0:
            turn = self.tileData[0]
            for ii, tile in enumerate(turn["tiles"]):
                RiverBorders = tile["RiverBorders"]
                if RiverBorders > 0:
                    RiverBitMap = tile["RiverBitMap"]
                    for ii in range(6):
                        if RiverBitMap >> ii & 1:
                            self.riverColors.append(riverPen)
                        else:
                            self.riverColors.append(emptyPen)
                else:
                    for jj in range(6):
                        self.riverColors.append(emptyPen)
        print("Total time for river colors: {}".format(time.time() - t0))

    def calculateCivHexas(self):
        civNum = self.majorCivs + self.minorCivs
        self.civHexaCounts = []
        for turn in self.tileData:
            civHexaCountsAtTurn = [0] * civNum
            for ii, tile in enumerate(turn["tiles"]):
                playerID = getPlayerID(tile)
                if 0 <= playerID < civNum:
                    civHexaCountsAtTurn[playerID] += 1
            self.civHexaCounts.append(civHexaCountsAtTurn)

    def calcPlayersAlive(self):
        playersNum = self.majorCivs + self.minorCivs
        self.playersAlive = []
        for hexaCounts, cityCounts in zip(self.civHexaCounts, self.cityCounts):
            temp = [x > 0 for x in hexaCounts]
            for i in range(self.majorCivs):
                if temp[i]:
                    continue
                elif cityCounts[i] > 0:
                    temp[i] = True
            self.playersAlive.append(temp)
        turns = len(self.playersAlive)
        for i in range(playersNum):  # For each player
            alive_from_start = False
            for j in range(turns):  # Check when first alive
                if self.playersAlive[j][i]:
                    alive_from_start = True
                if alive_from_start:  # Fill from beginning until first "alive"
                    for k in range(j):
                        self.playersAlive[k][i] = True
                    break

    def calculateBorderColors(self, lw=3, outsideBordersOnly=False, use_civ_colors=True, drawWaterBorders=True):
        if use_civ_colors:
            map_civ_colors(self.leaderData[0])
        t0 = time.time()
        self.borderColors = []
        self.borderColorsInner = []
        self.borderColorsSC = []
        for turn in self.tileData:
            borderColorsAtTurn = []
            borderInnerColorsAtTurn = []
            borderSCColorsAtTurn = []
            for ii, tile in enumerate(turn["tiles"]):
                if not drawWaterBorders:
                    terrainType = tile["TerrainType"]
                    try:
                        if (Terrains[terrainType]["TerrainType"] == "Ocean" or
                                Terrains[terrainType]["TerrainType"] == "Coast"):
                            if outsideBordersOnly:
                                for jj in range(6):
                                    borderColorsAtTurn.append(emptyPen)
                                    borderInnerColorsAtTurn.append(emptyPen)
                                    borderSCColorsAtTurn.append(emptyPen)
                            else:
                                borderColorsAtTurn.append(emptyBrush)
                                borderInnerColorsAtTurn.append(emptyBrush)
                                borderSCColorsAtTurn.append(emptyBrush)
                            continue
                    except:
                        print("drawWaterBorders failure ...")
                        pass
                playerID = getPlayerID(tile)
                if playerID >= 0:
                    if outsideBordersOnly:
                        for neighbour in self.neighbours_list[ii]:
                            if neighbour < self.X*self.Y:
                                neighbourID = getPlayerID(turn["tiles"][neighbour])
                                if neighbourID == playerID:
                                    if not drawWaterBorders:
                                        terrainType = turn["tiles"][neighbour]["TerrainType"]
                                        if (Terrains[terrainType]["TerrainType"] == "Ocean" or
                                                Terrains[terrainType]["TerrainType"] == "Coast"):
                                            borderColorsAtTurn.append(civColorsPen[playerID])
                                            borderInnerColorsAtTurn.append(civColorsPenInner[playerID])
                                            if 255 > playerID >= self.majorCivs:
                                                borderSCColorsAtTurn.append(blackPen)
                                            else:
                                                borderSCColorsAtTurn.append(emptyPen)
                                        else:
                                            borderColorsAtTurn.append(emptyPen)
                                            borderInnerColorsAtTurn.append(emptyPen)
                                            borderSCColorsAtTurn.append(emptyPen)
                                    else:
                                        borderColorsAtTurn.append(emptyPen)
                                        borderInnerColorsAtTurn.append(emptyPen)
                                        borderSCColorsAtTurn.append(emptyPen)
                                else:
                                    borderColorsAtTurn.append(civColorsPen[playerID])
                                    borderInnerColorsAtTurn.append(civColorsPenInner[playerID])
                                    if 255 > playerID >= self.majorCivs:
                                        borderSCColorsAtTurn.append(blackPen)
                                    else:
                                        borderSCColorsAtTurn.append(emptyPen)
                            else:
                                borderColorsAtTurn.append(civColorsPen[playerID])
                                borderInnerColorsAtTurn.append(civColorsPenInner[playerID])
                                if 255 > playerID >= self.majorCivs:
                                    borderSCColorsAtTurn.append(blackPen)
                                else:
                                    borderSCColorsAtTurn.append(emptyPen)
                    else:
                        borderColorsAtTurn.append(civColorsBrush[playerID])
                        borderInnerColorsAtTurn.append(emptyBrush)  # no inner
                        borderSCColorsAtTurn.append(emptyBrush)  # no inner
                else:
                    if outsideBordersOnly:
                        for jj in range(6):
                            borderColorsAtTurn.append(emptyPen)
                            borderInnerColorsAtTurn.append(emptyPen)
                            borderSCColorsAtTurn.append(emptyPen)
                    else:
                        borderColorsAtTurn.append(emptyBrush)
                        borderInnerColorsAtTurn.append(emptyBrush)
                        borderSCColorsAtTurn.append(emptyBrush)
            self.borderColors.append(borderColorsAtTurn)
            self.borderColorsInner.append(borderInnerColorsAtTurn)
            self.borderColorsSC.append(borderSCColorsAtTurn)
        print("Total time for border colors: {}".format(time.time() - t0))

    def calculateCityStateOrigos(self):
        t0 = time.time()
        # self.borderColorsInner = []
        if len(self.tileData) > 1:
            turnIdx = 1
        else:
            turnIdx = 0
        turn = self.tileData[turnIdx]
        self.minorOrigos = {}
        for ii, tile in enumerate(turn["tiles"]):
            playerID = getPlayerID(tile)
            if playerID >= self.majorCivs:  # Minor only
                neighbour_count_inv = 6
                found_orig = True
                for neighbour in self.neighbours_list[ii]:  # If more than 4 are owned (or all actually)
                    if neighbour < self.X*self.Y:
                        neighbourID = getPlayerID(turn["tiles"][neighbour])
                        if neighbourID != playerID:
                            neighbour_count_inv -= 1
                    if neighbour_count_inv <= 3:
                        found_orig = False
                        break
                if found_orig:
                    if playerID not in self.minorOrigos:
                        self.minorOrigos[playerID] = ii
                    else:
                        print("Already found minor origo, something went wrong")


        print("Total time for city state origos: {}".format(time.time() - t0))

    def calcIncrementalWars(self):
        used_turns = []
        self.incWars = []
        for i, (warsAtTurnIdx, diploAtTurnIdx) in enumerate(zip(self.wars, self.diploStates)):
            new_wars = []
            declarers = warsAtTurnIdx["declarers"]
            receivers = warsAtTurnIdx["receivers"]

            while True:
                turn = -1
                for declarer in declarers:
                    if declarer["turn"] not in used_turns:
                        turn = declarer["turn"]
                        used_turns.append(turn)
                        break
                if turn > 0:
                    decs = [declarer["id"] for declarer in declarers if declarer["turn"] == turn]
                    recs = [receiver["id"] for receiver in receivers if receiver["turn"] == turn]
                    if len(decs) == 1:
                        new_wars.append({"turn": turn, "declarer": decs[0], "receiver": recs[0]})
                    else:
                        unique_index = copy.copy(decs)
                        unique_index.extend(recs)
                        unique_index = np.unique(unique_index)
                        graph_size = len(unique_index)
                        g = Graph(graph_size)
                        for dec in decs:
                            for rec in recs:
                                if diploAtTurnIdx[dec][rec]["state"][:3] == "WAR":
                                    g.addEdge(np.where(unique_index == dec)[0][0], np.where(unique_index == rec)[0][0])
                                    new_wars.append({"turn": turn, "declarer": dec, "receiver": rec})
                        if g.isCyclic():
                            print(f"Warning cyclic war declaration during turn #{i}!!")
                else:
                    break
            self.incWars.append(new_wars)


    def getOwner(self, turnIdx, x, y, language=None):
        civ_text = ""
        civs = self.civData[0]
        leaders = self.leaderData[0]
        turn = self.tileData[turnIdx]
        if 0 < x <= self.X and 0 < y <= self.Y:
            tile = turn["tiles"][y * self.X + x]
            playerID = getPlayerID(tile)
            if playerID >= 0:
                if playerID < len(leaders):
                    leader = leaders[playerID]
                    leader_name, cityState = parseLeader(leader)
                    colorhex = ''.join([format(int(c), '02x') for c in civColors[playerID]])
                    colorhexInner = ''.join([format(int(c), '02x') for c in civColorsInner[playerID]])
                    civ = civs[playerID]
                    civ_name = " ".join(x.capitalize() for x in civ.split("_"))

                    civ_name, leader_name = self.languageChanger(language, civ, leader, cityState, civ_name,
                                                                 leader_name)

                    civ_text += "<font color=#" + colorhex + ">" + civ_name + "</font><br>"
                    civ_text += "<font color=#" + colorhexInner + ">" + leader_name + "</font>"
                elif playerID == 62:  # Free City
                    civ_text += "Free City"
                elif playerID == 255:
                    civ_text += "Coastal Flood"
        return civ_text

    def calcMajorCivs(self):
        leaders = self.leaderData[0]
        count = 0
        for leader in leaders:
            if leader[:10] == "MINOR_CIV_":
                break
            count += 1
        self.majorCivs = count
        self.minorCivs = len(leaders) - count
        self.minorCivTypes = {}
        for ii in range(count, len(leaders)):
            civ_name = " ".join(x.capitalize() for x in leaders[ii][10:].split("_"))
            try:
                self.minorCivTypes[ii] = CS_TYPES[civ_name]
            except:
                self.minorCivTypes[ii] = "Unknown"

    def languageChanger(self, language, civ, leader, cityState, civ_name, leader_name):
        if language != "en_EN" and language is not None:
            if civ in CIV_NAMES:
                if language in CIV_NAMES[civ]:
                    civ_name = CIV_NAMES[civ][language]
            if leader in CIV_LEADER_NAMES and not cityState:
                if language in CIV_LEADER_NAMES[leader]:
                    leader_name = CIV_LEADER_NAMES[leader][language]
        return civ_name, leader_name

    def parseCivNames(self, language=None):
        self.calculatingCivNames = True
        civs = self.civData[0]
        leaders = self.leaderData[0]
        self.civ_text = []
        for i, civ in enumerate(civs):
            colorhex = ''.join([format(int(c), '02x') for c in civColors[i]])
            colorhexInner = ''.join([format(int(c), '02x') for c in civColorsInner[i]])
            leader = leaders[i]
            leader_name, cityState = parseLeader(leader)
            civ_name = " ".join(x.capitalize() for x in civ.split("_"))

            civ_name, leader_name = self.languageChanger(language, civ, leader, cityState, civ_name, leader_name)

            # \u2b22 hexa
            if cityState:
                colorhexMinor = ''.join([format(int(c), '02x') for c in civColorsMinor[i]])
                try:
                    symbol = CS_UNICODE_MAP[self.minorCivTypes[i]]
                except:
                    symbol = "&nbsp;\u2b22&nbsp;&nbsp;"
                self.civ_text.append("<font color=#" + colorhexMinor + ">" + symbol + "</font>" +
                                     "<font color=#" + colorhex + ">" + civ_name + "</font> " +
                                     "<font color=#" + colorhexInner + ">" + "CS " + "</font><br>")
            else:
                self.civ_text.append("<font color=#" + colorhex + ">" + civ_name + "</font> - " +
                                     "<font color=#" + colorhexInner + ">" + leader_name + "</font><br>")
        self.calculatingCivNames = False

    def getCivNames(self, turnIdx):
        playersRemaining = self.playersAlive[turnIdx]
        civ_text = ""
        if not self.calculatingCivNames:
            for i, alive in enumerate(playersRemaining):
                # First minor civ
                if i == self.majorCivs:
                    civ_text += "<br>"
                if alive:
                    civ_text += self.civ_text[i]
        return civ_text

    def calculateCityColors(self, useInnerAsCityColor=True, useMinorType=False):
        t0 = time.time()
        cityColorsAtTurnEmpty = [emptyBrush] * self.X*self.Y
        self.cityColors = []
        for ii, turn in enumerate(self.cityData):
            cityColorsAtTurn = cityColorsAtTurnEmpty
            for minor in self.minorOrigos:
                if self.playersAlive[ii][minor] and ii != 0:
                    if useMinorType:
                        cityColorsAtTurn[self.minorOrigos[minor]] = civColorsBrushMinor[minor]
                    else:
                        cityColorsAtTurn[self.minorOrigos[minor]] = civColorsBrushInner[minor]
            for city in turn["cities"]:
                if useInnerAsCityColor:
                    cityColorsAtTurn[city["LocationIdx"]] = civColorsBrushInner[city["CivIndex"]]
                else:
                    cityColorsAtTurn[city["LocationIdx"]] = civColorsBrush[city["CivIndex"]]
            self.cityColors.append(copy.copy(cityColorsAtTurn))
        print("Total time for city colors: {}".format(time.time() - t0))

    def calculateMinorCityColors(self):
        t0 = time.time()
        cityColorsAtTurnEmpty = [emptyBrush] * self.X*self.Y
        self.minorCityColors = []
        for ii, turn in enumerate(self.cityData):
            cityColorsAtTurn = cityColorsAtTurnEmpty
            for minor in self.minorOrigos:
                if self.playersAlive[ii][minor]:
                    cityColorsAtTurn[self.minorOrigos[minor]] = civColorsBrushMinor[minor]
            self.minorCityColors.append(copy.copy(cityColorsAtTurn))
        print("Total time for minor city colors: {}".format(time.time() - t0))



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


# Python program to detect cycle
# in a graph
class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)
        self.V = vertices

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def isCyclicUtil(self, v, visited, recStack):

        # Mark current node as visited and
        # adds to recursion stack
        visited[v] = True
        recStack[v] = True

        # Recur for all neighbours
        # if any neighbour is visited and in
        # recStack then graph is cyclic
        for neighbour in self.graph[v]:
            if visited[neighbour] == False:
                if self.isCyclicUtil(neighbour, visited, recStack) == True:
                    return True
            elif recStack[neighbour] == True:
                return True

        # The node needs to be poped from
        # recursion stack before function ends
        recStack[v] = False
        return False

    # Returns true if graph is cyclic else false
    def isCyclic(self):
        visited = [False] * self.V
        recStack = [False] * self.V
        for node in range(self.V):
            if visited[node] == False:
                if self.isCyclicUtil(node, visited, recStack) == True:
                    return True
        return False
