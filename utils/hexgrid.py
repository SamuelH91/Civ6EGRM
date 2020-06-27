from utils.hexagon import Hexagon
import numpy as np

Y0 = np.sqrt(3)/2
Y1 = 1/np.sqrt(3)
Y2 = 1/2/np.sqrt(3)
X1 = 0.0
X2 = 0.5

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
# 179, 185, 178
# Features:
# No feature: 			    255 255 255 255:	FF FF FF FF
# Rainforest:				57 84 17 233:		39 54 11 E9
# Woods:					68 9 34 10: 		44 09 22 0A
# March (grassland only):	195 89 85 35:		C3 59 55 23
# Oasis (desert only):	    163 83 31 98:		A3 53 1F 62
# Floodlands(desert only):  38 119 181 82:		26 77 B5 52
# Ice (ocean/coast):		148 3 236 91:		94 03 EC 5B
#
# Goody hut: 									EA CD 58 15
#
# Terrain2?:
# Sea:					    255 255 255 255: 	FF FF FF FF
# Land:					    197 141 5 214:		C5 8D 05 D6
# Snow:					    234 205 88 21:		EA CD 58 15


class HexGrid:
    def __init__(self, x, y, numOfPlayers=10):
        self.X = x
        self.Y = y
        self.numOfPlayers = numOfPlayers
        self.pColors = np.random.rand(numOfPlayers, 3)
        self.patches_list = []
        self.color_list = []
        # self.temp = []
        for yy in range(y):
            xOffset = X2 if yy % 2 == 1 else X1
            yval = yy*Y0
            for xx in range(x):
                self.patches_list.append(Hexagon(np.array([[xx + xOffset], [yval]])))
                self.color_list.append(np.random.rand(3,))

    def set_environment_colors(self, map):
        self.color_list = []
        for tile in map["tiles"]:
            terrainType = tile["TerrainType"]
            try:
                color = Terrains[terrainType]["color"]
                self.color_list.append(color)
            except:
                print("x: {}, x: {}, type: {}".format(tile["x"], tile["y"], terrainType))
                self.color_list.append(np.zeros(3,))

    def set_fill(self, fill):
        for patch in self.patches_list:
            patch.set_fill(fill)

    def set_lw(self, lw):
        for patch in self.patches_list:
            patch.set_linewidth(lw)

    def update_border_colors(self, map):
        self.color_list = []
        for ii, tile in enumerate(map["tiles"]):
            #self.color_list.append(np.ones(3,)*tile["TerrainType"]/4294967295)
            #self.color_list.append(np.ones(3,)*tile["TerrainType2"]/4294967295)
            #self.color_list.append(np.ones(3,)*tile["IceLevelForest"]/4294967295)
            #self.color_list.append(np.ones(3,)*tile["River border count"]/255)
            #self.color_list.append(np.ones(3,)*tile["rivermap"]/255)
            #self.color_list.append(np.ones(3,)*tile["cliffmap"]/255)
            #self.color_list.append(np.ones(3,)*tile["RoadLevel"]/255)
            #self.color_list.append(np.ones(3,)*tile["landmass index"]/65535)
            # if tile["OwnershipBuffer"] >= 64:
            #     tileBufferData = tile["buffer"]
            #     playerID = tileBufferData[-5]
            #     self.color_list.append(np.append(self.pColors[playerID, :], 0.5))
            # else:
            #     self.color_list.append(np.zeros(4,))
            if tile["OwnershipBuffer"] >= 64:
                tileBufferData = tile["buffer"]
                playerID = tileBufferData[-5]
                self.patches_list[ii].set_ec(np.append(self.pColors[playerID, :], 0.5))
            else:
                self.patches_list[ii].set_ec(np.zeros(4,))


        # self.patches_list = []
        # yy = np.round(ii / self.X)
        # xOffset = X2 if yy % 2 == 1 else X1
        # yval = yy * Y0
        # xx = ii % self.X
        # self.patches_list.append(Hexagon(np.array([[xx + xOffset], [yval]])))


        # myorder = np.transpose(np.arange(self.X*self.Y).reshape(self.X, self.Y)).flatten()
        # self.color_list = [self.color_list[i] for i in myorder]

