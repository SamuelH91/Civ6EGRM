import pyqtgraph as pg
import numpy as np

Terrains = {
    2213004848: {"TerrainType": "grassland",                "color": pg.mkBrush(pg.mkColor(np.array([103, 125, 48])))},
    1855786096: {"TerrainType": "grassland (hills)",        "color": pg.mkBrush(pg.mkColor(np.array([103, 125, 48])))},
    1602466867: {"TerrainType": "grassland (mountains)",    "color": pg.mkBrush(pg.mkColor(np.array([132, 133, 134])))},
    4226188894: {"TerrainType": "plains",                   "color": pg.mkBrush(pg.mkColor(np.array([159, 159, 53])))},
    3872285854: {"TerrainType": "plains (hills)",           "color": pg.mkBrush(pg.mkColor(np.array([159, 159, 53])))},
    2746853616: {"TerrainType": "plains (mountains)",       "color": pg.mkBrush(pg.mkColor(np.array([132, 133, 134])))},
    3852995116: {"TerrainType": "desert",                   "color": pg.mkBrush(pg.mkColor(np.array([236, 196, 111])))},
    3108058291: {"TerrainType": "desert (hills)",           "color": pg.mkBrush(pg.mkColor(np.array([236, 196, 111])))},
    1418772217: {"TerrainType": "desert (mountains)",       "color": pg.mkBrush(pg.mkColor(np.array([132, 133, 134])))},
    1223859883: {"TerrainType": "tundra",                   "color": pg.mkBrush(pg.mkColor(np.array([171, 170, 139])))},
    3949113590: {"TerrainType": "tundra (hills)",           "color": pg.mkBrush(pg.mkColor(np.array([171, 170, 139])))},
    3746160061: {"TerrainType": "tundra (mountains)",       "color": pg.mkBrush(pg.mkColor(np.array([132, 133, 134])))},
    1743422479: {"TerrainType": "snow",                     "color": pg.mkBrush(pg.mkColor(np.array([204, 223, 243])))},
    3842183808: {"TerrainType": "snow (hills)",             "color": pg.mkBrush(pg.mkColor(np.array([204, 223, 243])))},
    699483892:  {"TerrainType": "snow (mountains)",         "color": pg.mkBrush(pg.mkColor(np.array([132, 133, 134])))},
    1204357597: {"TerrainType": "Ocean",                    "color": pg.mkBrush(pg.mkColor(np.array([45, 49, 86])))},
    1248885265: {"TerrainType": "Coast",                    "color": pg.mkBrush(pg.mkColor(np.array([45, 89, 120])))},
}

Features = {  # + goodyhut codes
    4294967295: {"FeatureType": "NoFeature",            "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    662085235:  {"FeatureType": "Aerodome",             "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2588244546: {"FeatureType": "Alcazar",              "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    3727362748: {"FeatureType": "BarbCamp",             "color": pg.mkBrush(pg.mkColor(np.array([183, 20, 20])))},
    3000670711: {"FeatureType": "BurntWoods",           "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    172143503:  {"FeatureType": "BurntRainforest",      "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1957694686: {"FeatureType": "CahokiaMounds",        "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2475408324: {"FeatureType": "Camp",                 "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2176791945: {"FeatureType": "ColossalHead",         "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1387624230: {"FeatureType": "DesertFloodplains",    "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1555056577: {"FeatureType": "GeothermalFissure",    "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2686085371: {"FeatureType": "GolfCourse",           "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1434118760: {"FeatureType": "GoodyHut",             "color": pg.mkBrush(pg.mkColor(np.array([241, 209, 100])))},
    2414989200: {"FeatureType": "GreatWall",            "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2973166745: {"FeatureType": "GrasslandFloodplains", "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    168372657:  {"FeatureType": "Farm",                 "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    578093457:  {"FeatureType": "FishingBoats",         "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1694280827: {"FeatureType": "Fort",                 "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1542194068: {"FeatureType": "Ice",                  "color": pg.mkBrush(pg.mkColor(np.array([171, 188, 219])))},
    874973008:  {"FeatureType": "Kampung",              "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    3808671749: {"FeatureType": "Kurgan",               "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2048582848: {"FeatureType": "LumberMill",           "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    592796099:  {"FeatureType": "March",                "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    590245655:  {"FeatureType": "Mekewap",              "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    933499311:  {"FeatureType": "MeteorSite",           "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1001859687: {"FeatureType": "Mine",                 "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2970879537: {"FeatureType": "Moai",                 "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2457279608: {"FeatureType": "Monastery",            "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    3108964764: {"FeatureType": "MountainTunnel",       "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1163354216: {"FeatureType": "NazcaLine",            "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1646220195: {"FeatureType": "Oasis",                "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    3898338829: {"FeatureType": "OffshoreOilRig",       "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1058336991: {"FeatureType": "OffshoreWindFarm",     "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2939453696: {"FeatureType": "OilWell",              "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1151932567: {"FeatureType": "OutbackStation",       "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1719494282: {"FeatureType": "Pairidaeza",           "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    154488225:  {"FeatureType": "Pasture",              "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1523996587: {"FeatureType": "Plantation",           "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    4214473799: {"FeatureType": "Quarry",               "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    3910227001: {"FeatureType": "Rainforest",           "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    3943953367: {"FeatureType": "Reef",                 "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1195876395: {"FeatureType": "RomanFort",            "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    570930386:  {"FeatureType": "SeasideResort",        "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2182120684: {"FeatureType": "Sphinx",               "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2135005470: {"FeatureType": "SkiResort",            "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2127465633: {"FeatureType": "SolarFarm",            "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2005950930: {"FeatureType": "VolcanicSoil",         "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2771557557: {"FeatureType": "Volcano",              "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    520634903:  {"FeatureType": "WindFarm",             "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2265104033: {"FeatureType": "Unknown",              "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    170002756:  {"FeatureType": "Unknown",              "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},

    # Wonders
    2773098215: {"FeatureType": "ChocolateHills",       "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1: {"FeatureType": "CliffsOfDover",        "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1253249868: {"FeatureType": "CraterLake",           "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1894931018: {"FeatureType": "DeadSea",              "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1781837174: {"FeatureType": "DelicateArch",         "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    656656409:  {"FeatureType": "EyeOfTheSahara",       "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    853279971:  {"FeatureType": "Eyjafjallajokull",     "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    226585075:  {"FeatureType": "Galapagos",            "color": pg.mkBrush(pg.mkColor(np.array([243, 212, 1])))},
    1653648472: {"FeatureType": "GiantsCauseway",       "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    978567123:  {"FeatureType": "Gobustan",             "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    3583470385: {"FeatureType": "GreatBarrierReef",     "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    172143503:  {"FeatureType": "FountainOfYouth",      "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1084731038: {"FeatureType": "HalongBay",            "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    501201242:  {"FeatureType": "IkKil",                "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    482180537:  {"FeatureType": "LakeRetba",            "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    308108439:  {"FeatureType": "Lysefjord",            "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    3082807326: {"FeatureType": "MatoTipila",           "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    224663563:  {"FeatureType": "Matterhorn",           "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    12: {"FeatureType": "MountEverest",         "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2354893825: {"FeatureType": "MountKilimanjaro",     "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    3861018290: {"FeatureType": "MountRoraima",         "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2284878731: {"FeatureType": "MountVesuvius",        "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1491718565: {"FeatureType": "Pamukkale",            "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1394593257: {"FeatureType": "Pantanal",             "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    1624801336: {"FeatureType": "Piopiotahi",           "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    3738443622: {"FeatureType": "SaharaElBeyda",        "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    2666510884: {"FeatureType": "TorresDelPaine",       "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    981353664:  {"FeatureType": "TsingyDeBemaraha",     "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    21: {"FeatureType": "UbsunurHollow",        "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    4277999168: {"FeatureType": "Uluru",                "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
    22: {"FeatureType": "Yosemite",             "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},  # 1253249868
    23: {"FeatureType": "ZhangyeDanxia",        "color": pg.mkBrush(pg.mkColor(np.array([0, 0, 0])))},
}
