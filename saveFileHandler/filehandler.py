import zlib
import numpy as np
from utils.binaryconvert import *
from saveFileHandler.features import Terrains, Features

CHUNKSIZE = 64 * 1024


# /**
#  * Output a decompressed buffer from the primary zlib zip of the .Civ6Save file
#  * @param {Buffer} savefile
#  * @return {Buffer} decompressed
#  */
def decompress(saveFileBuffer):
    civsav = saveFileBuffer
    # just skip this part for now
    header, idxH = parseHeader(saveFileBuffer)
    # jsons = parseJson(saveFileBuffer, idxH)
    modindex = civsav.rfind(b'MOD_TITLE')
    bufstartindex = civsav.index(b'\x78\x9c', modindex)
    bufendindex = civsav.index(b'\x00\x00\xFF\xFF', bufstartindex)  # Find next end flag

    data = civsav[bufstartindex:bufendindex]

    # drop 4 bytes away after every chunk
    compressedData = b''
    pos = 0
    while pos < len(data):
        compressedData += data[pos:pos + CHUNKSIZE]
        pos += CHUNKSIZE + 4

    zobj = zlib.decompressobj()  # use this to prevent errors instead of zlib.decompresss()
    decompressed = zobj.decompress(compressedData)
    return decompressed


def recompress(saveFileBuffer, decompressedData):
    zobj = zlib.compressobj()  # use this to prevent errors instead of zlib.decompresss()
    compressedData = zobj.compress(decompressedData)
    compressedData += zobj.flush()
    compressedDataWithLengths = b''

    pos = 0
    while pos < len(compressedData):
        compressedDataSlice = compressedData[pos:pos + CHUNKSIZE]
        compressedDataWithLengths += writeUInt32LE(len(compressedDataSlice))
        compressedDataWithLengths += compressedDataSlice
        pos += CHUNKSIZE

    civsav = saveFileBuffer
    modindex = civsav.rfind(b'MOD_TITLE')
    bufstartindex = civsav.index(b'\x78\x9c', modindex) - 4
    bufendindex = civsav.rindex(b'\x00\x00\xFF\xFF')

    merged = b''
    merged += civsav[:bufstartindex]
    merged += compressedDataWithLengths[:-4]
    merged += civsav[bufendindex:]

    return merged


def revealMap(decompressedData):
    modifiedData = b''
    baseindex = decompressedData.index(b'\x26\x10\x35\x11')
    tiles = readInt32(decompressedData, baseindex + 8)
    mapIndex = baseindex - tiles - 4
    modifiedData += decompressedData[:mapIndex]
    for tileIdx in range(tiles):
        modifiedData += b'\x01'
    modifiedData += decompressedData[mapIndex+tiles:]
    return modifiedData


# def seeAll(decompressedData):
#     modifiedData = b''
#     baseindex = decompressedData.index(b'\x26\x10\x35\x11')
#     tiles = readInt32(decompressedData, baseindex + 8)
#     mapIndex = baseindex + 20
#     modifiedData += decompressedData[:mapIndex]
#     for tileIdx in range(tiles*2):
#         if tileIdx % 2 == 0:
#             modifiedData += b'\x03'
#         else:
#             modifiedData += b'\x00'
#     modifiedData += decompressedData[mapIndex+tiles*2:]
#     return modifiedData


def parseHeader(saveFileBuffer):
    gamespeedlen = readUInt16(saveFileBuffer, 20)
    idx0 = 28 + gamespeedlen
    # After game speed there might be some json information about modes
    idx1 = saveFileBuffer.index(b'\x40\x5C\x83\x0B\x05\x00\x00\x00')
    mapsizelen = readUInt16(saveFileBuffer, idx1 + 8)
    idx2 = idx1 + mapsizelen + 16
    header = {
        "FileHeader": saveFileBuffer[:4],
        "h1_": readUInt32(saveFileBuffer, 4),
        "h2_": readUInt32(saveFileBuffer, 8),
        "h3_": readUInt32(saveFileBuffer, 12),
        "h4_": readUInt32(saveFileBuffer, 16),
        "GameSpeedLen": gamespeedlen,
        "GameSpeedLen1_": readUInt16(saveFileBuffer, 22),
        "GameSpeedLen2_": readUInt32(saveFileBuffer, 24),
        "GameSpeed": saveFileBuffer[28:idx0],
        # some json about modes
        "h5_": readUInt32(saveFileBuffer, idx1),
        "h6_": readUInt32(saveFileBuffer, idx1 + 4),
        "MapSizeLen": mapsizelen,
        "MapSizeLen1_": readUInt16(saveFileBuffer, idx1 + 10),
        "MapSizeLen2_": readUInt32(saveFileBuffer, idx1 + 12),
        "MapSize": saveFileBuffer[idx1 + 16:idx2],
        "h7_": readUInt32(saveFileBuffer, idx2),
        "h8_": readUInt32(saveFileBuffer, idx2 + 4),
        "h9_": readUInt32(saveFileBuffer, idx2 + 8),
        "h10_": readUInt32(saveFileBuffer, idx2 + 12),
        "epoch": readUInt32(saveFileBuffer, idx2 + 16),
        "epoch_": readUInt32(saveFileBuffer, idx2 + 20),
        "h11_": readUInt32(saveFileBuffer, idx2 + 24),
        "h12_": readUInt32(saveFileBuffer, idx2 + 28),
    }
    return header, idx2 + 32


def parseJson(saveFileBuffer, idxH):
    json1len = readUInt16(saveFileBuffer, idxH)
    idx1 = idxH + json1len + 8
    json2len = readUInt16(saveFileBuffer, idx1 + 8)
    idx2 = idx1 + json2len + 16
    fol4len = readUInt16(saveFileBuffer, idx2 + 8)
    zliblen = readUInt32(saveFileBuffer, idx2 + 24)
    idx3 = idx2 + 28 + zliblen

    compressedData = saveFileBuffer[idx2 + 28:idx3]
    zobj = zlib.decompressobj()  # use this to prevent errors instead of zlib.decompresss()
    decompressed = zobj.decompress(compressedData)

    Jsons = {
        "Json1Len": json1len,
        "Json1Len1_": readUInt16(saveFileBuffer, idxH + 2),
        "Json1Len2_": readUInt32(saveFileBuffer, idxH + 4),
        "JSON1": saveFileBuffer[idxH + 8:idx1],
        "j1_": readUInt32(saveFileBuffer, idx1),
        "j2_": readUInt32(saveFileBuffer, idx1 + 4),
        "Json2Len": json2len,
        "Json2Len1_": readUInt16(saveFileBuffer, idx1 + 10),
        "Json2Len2_": readUInt32(saveFileBuffer, idx1 + 12),
        "JSON2": saveFileBuffer[idx1 + 16:idx2],
        "j3_": readUInt32(saveFileBuffer, idx2),
        "j4_": readUInt32(saveFileBuffer, idx2 + 4),
        "Fol4Len": fol4len,
        "FolLen1_": readUInt16(saveFileBuffer, idx2 + 10),
        "FolLen2_": readUInt32(saveFileBuffer, idx2 + 12),
        "j5_": readUInt32(saveFileBuffer, idx2 + 16),
        "j6_": readUInt32(saveFileBuffer, idx2 + 20),
        "ZlibLen": zliblen,
        "decomp1": decompressed
    }
    return Jsons


#
# # /**
# #  * Output a .Civ6Save buffer built from an existing .Civ6Save buffer and a decompressed bin buffer
# #  * @param {Buffer} savefile
# #  * @param {Buffer} binfile
# #  * @return {Buffer} newsave
# #  */
# def recompress(savefile, binfile):
#   # We need to insert an extra 4 bytes every 64 * 1024 bytes of data to indicate length of the upcoming chunk
#
#   compressedBuffer = zlib.deflateSync(binfile, {finishFlush: zlib.Z_SYNC_FLUSH})
#   length = compressedBuffer.length
#   CHUNK_LENGTH = 64 * 1024
#   chunks = []
#
#   for (let i = 0 i < length i += CHUNK_LENGTH):
#     slice = compressedBuffer.slice(i, i + CHUNK_LENGTH)
#     if i !== 0:
#       intbuf = new Buffer(4)
#       intbuf.writeInt32LE(slice.length)
#       chunks.push(intbuf)
#     chunks.push(compressedBuffer.slice(i, i + CHUNK_LENGTH))
#
#   finalBuffer = Buffer.concat(chunks)
#
#   civsav = savefile
#
#   # Find the last index of MOD_TITLE string
#   # There are many compressed buffers in the .Civ6Save file, but the largest one and one we need
#   # can be found after the last instance of this string
#   modindex = civsav.lastIndexOf('MOD_TITLE')
#
#   # Hex sequence 78 9c indicates the beginning of a zlib compressed buffer, and 00 00 FF FF indicates  the end
#   bufstartindex = civsav.indexOf(new Buffer([0x78, 0x9c]), modindex)
#   bufendindex = civsav.lastIndexOf(new Buffer([0x00, 0x00, 0xFF, 0xFF])) + 4
#
#   merged = Buffer.concat([civsav.slice(0, bufstartindex), finalBuffer, civsav.slice(bufendindex)])
#
#   return merged
#
#
# # /**
# #  * Take in a .Civ6Save file, decompress it into a bin, run a callback on the bin, and recombine and return a new save
# #  * @param {Buffer} savefile
# #  * @param {Function} callback
# #  * @return {Buffer} newsavefile
# #  */
# def modify(savefile, callback = (x => x)):
#   bin = decompress(savefile)
#   moddedbin = callback(bin)
#   return recompress(savefile, moddedbin)
#
#
# # /**
# #  * Take in a .Civ6Save file, decompress it into a bin, run a callback on each tile buffer, and recombine into new save
# #  * @param {Buffer} savefile
# #  * @param {Function} callback
# #  * @return {Buffer} newsavefile
# #  */
# def modify_tiles(savefile, callback = (b => b)):
#   return modify(savefile, bin => {
#     searchBuffer = new Buffer([0x0E, 0x00, 0x00, 0x00, 0x0F, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00])
#     mapstartindex = bin.indexOf(searchBuffer)
#     tiles = bin.readInt32LE(mapstartindex + 12)
#
#     let mindex = mapstartindex + 16
#     for (let i = 0 i < tiles i++) {
#       num2 = bin.readUInt8(mindex + 49)
#       num = bin.readUInt32LE(mindex + 51)
#       let buflength = 0
#
#       num && (buflength += 24)
#       (num2 >= 64) && (buflength += 17)
#
#       tilebuf = bin.slice(mindex, mindex + 55 + buflength)
#       newtilebuf = callback(tilebuf)
#       newtilebuf.copy(bin, mindex)
#
#       mindex += 55 + buflength
#     }
#
#     return bin
#   })
#
#
# # /**
# #  * If there isn't a certain extension suffix on the file name, add it
# #  * @param {string} filename
# #  * @param {string} extension
# #  * @return {string} newfilename
# #  */
# def verify_extension(filename, ext = '.Civ6Save'):
#   if filename.slice(-9) != ext:
#     return filename + ext
#   return filename
#
#

def get_civ_data(data):

    civ_id_start_key = b'\x54\xB4\x8A\x0D\x02'
    civ_id_end_key = b'\x58\xBA\x7F\x4C\x02'  # old one not reliable: b'\x2F\x52\x96\x1A\x02'  # Just before this one
    civ_adjective_key = b'\x31\xEB\x88\x62'
    civ_leader_key = b'\x5F\x5E\xCD\xE8'

    bin = data
    civs = []
    try:
        civNameIndex = bin.index(civ_adjective_key)
        # There is some religion info as well at same section
        while civNameIndex:
            civNameLength = readUInt16(bin, civNameIndex + 8)
            civName = bin[civNameIndex + 16 + 17:civNameIndex + 16 + civNameLength - 11].decode("utf-8")
            try:
                civIndex = bin.rfind(civ_id_end_key, 0, civNameIndex) - 4
                civIdx = readUInt16(bin, civIndex)
            except:
                print("Error finding civ index")
                civIdx = -1
            if civIdx != 63:  # or known as BARBARIAN
                try:
                    leaderIndex = bin.find(civ_leader_key, civNameIndex)
                    leaderNameLength = readUInt16(bin, leaderIndex + 8)
                    leaderName = bin[leaderIndex + 16 + 7:leaderIndex + 16 + leaderNameLength - 1].decode("utf-8")
                except:
                    print("Error finding leader")
                    leaderName = None
                civs.append({
                    "CivName": civName,
                    "LeaderName": leaderName,
                    "CivIndex": civIdx,
                })
            try:
                civNameIndex = bin.index(civ_adjective_key, civNameIndex + 8)
            except:
                break
    except:
        print("Error no civs!!!")
        pass
    civsOrdered = [None] * len(civs)
    leadersOrdered = [None] * len(civs)
    for civ in civs:
        idx = civ["CivIndex"]
        civsOrdered[idx] = civ["CivName"]
        leadersOrdered[idx] = civ["LeaderName"]
    return civsOrdered, leadersOrdered


MAPSIZEDATA = {
    '1144': {"x": 44, "y": 26},
    '2280': {"x": 60, "y": 38},
    '3404': {"x": 74, "y": 46},
    '3696': {"x": 84, "y": 44},  # YnAMP - Small
    '4536': {"x": 84, "y": 54},
    '4800': {"x": 96, "y": 50},  # YnAMP - Standard
    '5760': {"x": 96, "y": 60},
    '5767': {"x": 79, "y": 73},  # YnAMP - Large Europe
    '6048': {"x": 108, "y": 56},  # YnAMP - Large
    '6656': {"x": 104, "y": 64},  # YnAMP - Greatest Earth Map
    '6996': {"x": 106, "y": 66},
    '7344': {"x": 108, "y": 68},  # YnAMP - Huge Europe
    '7440': {"x": 120, "y": 62},  # YnAMP - Huge
    '10360': {"x": 140, "y": 74},  # YnAMP - Enormous
    '16920': {"x": 180, "y": 94},  # YnAMP - Giant
    '20800': {"x": 200, "y": 104},  # YnAMP - Ludicrous
    '26680': {"x": 230, "y": 116},  # YnAMP - Largest Earth Map
}

def find_mapstart_idx(bin, key, offset=0):
    mapstartindex = bin.index(key)
    tiles = readInt32(bin, mapstartindex + len(key) + offset)
    tileskey = str(tiles)
    tilesmap = {"tiles": [], "mapSize": [MAPSIZEDATA[tileskey]["x"], MAPSIZEDATA[tileskey]["y"]]}
    mindex = mapstartindex + len(key) + 4
    return mindex, tiles, tileskey, tilesmap

# /**
#  * Convert compressed tile data in .Civ6Save file into json format
#  * @param {buffer} savefile
#  * @return {object} tiles
#  */
def save_to_map_json(mainDecompressedData, idx):
    bin = mainDecompressedData
    try:
        mindex, tiles, tileskey, tilesmap =\
            find_mapstart_idx(bin, b'\x0E\x00\x00\x00\x0F\x00\x00\x00\x06\x00\x00\x00')
    except:
        try:
            # print(f"File #{idx}: Warning default map start index not found, trying second guess!!!")
            mindex, tiles, tileskey, tilesmap =\
                find_mapstart_idx(bin, b'\x16\x00\x00\x00\x17\x00\x00\x00\x06\x00\x00\x00')
        except:
            try:
                # print(f"File #{idx}: Warning default map start index not found, trying third guess!!!")
                mindex, tiles, tileskey, tilesmap =\
                    find_mapstart_idx(bin, b'\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x06\x00\x00\x00')
            except:
                # Print("Try some heuristic search")
                # Usually something like this at the beginning of tiles
                # mapstartindex = bin.index(b'\x00\x00\x01\x00\x00\x00\x01\x00\xFF\xFF\xFF\xFF') - 16
                print(f"File #{idx}: Couldn't find map start idx, contact support with autosave files + mods what are you using")

    SX = MAPSIZEDATA[tileskey]["x"]
    SY = MAPSIZEDATA[tileskey]["y"]

    for i in range(tiles):
        OwnershipBuffer = readUInt8(bin, mindex + 49)
        TileOverlayNum = readUInt32(bin, mindex + 51)
        GoodyHut = readUInt32(bin, mindex + 33)
        buflength = 0

        if TileOverlayNum == 1:
            buflength += 24
        elif TileOverlayNum == 2:
            buflength += 44
        if OwnershipBuffer >= 64:
            buflength += 17

        FeatureType = readUInt32(bin, mindex + 16)
        TerrainType = readUInt32(bin, mindex + 12)
        if FeatureType not in Features:
            print(f"File #{idx}: Add feature: {FeatureType}, x: {i % SX}, y: {np.floor(i / SX)}")

        # ski resort + mountain tunnel + galapagos (initial guess)
        if GoodyHut == 2135005470 or GoodyHut == 3108964764 or FeatureType == 226585075:
            buflength += 20

        # galapagos heuristic check, that confirms correct buffer length by testing next feature and terrain validity
        if FeatureType == 226585075:
            # print("Galapagos on map, check for black tiles, remove this comment later if no issues")
            # Check validity of next feature
            if i < tiles - 1:
                NextFeatureType = readUInt32(bin, mindex + 55 + buflength + 16)
                NextTerrainType = readUInt32(bin, mindex + 55 + buflength + 12)
                if NextFeatureType not in Features or NextTerrainType not in Terrains:
                    buflength -= 20

        # See bin-structure.md for WIP documentation on what each of these values are
        tilesmap["tiles"].append({
            "x": i % SX,
            "y": np.floor(i / SX),
            "hexbin-location": mindex,
            "tile-length": 55 + buflength,
            "int16-1": readUInt16(bin, mindex),
            "int16-2": readUInt16(bin, mindex + 2),
            "int16-3": readUInt16(bin, mindex + 4),
            "int16-4": readUInt16(bin, mindex + 6),
            "Landmass": readUInt16(bin, mindex + 8),
            "Landmass1": readUInt16(bin, mindex + 10),
            "TerrainType": TerrainType,
            "FeatureType": FeatureType,
            "?-1": readUInt16(bin, mindex + 20),
            "LandSnowSea": readUInt32(bin, mindex + 22),
            "?-2": readUInt8(bin, mindex + 26),
            "Resource": readUInt32(bin, mindex + 27),
            "ResourceBoolean": readUInt16(bin, mindex + 31),
            "GoodyHut": GoodyHut,
            "?-3": readUInt8(bin, mindex + 37),
            "RoadLevel": readInt8(bin, mindex + 38),
            "?-4": readUInt8(bin, mindex + 39),
            "TileAppeal": readInt16(bin, mindex + 40),
            "?-5": readUInt8(bin, mindex + 42),
            "?-6": readUInt8(bin, mindex + 43),
            "?-7": readUInt8(bin, mindex + 44),
            "RiverBorders": readUInt8(bin, mindex + 45),
            "RiverBitMap": readUInt8(bin, mindex + 46),  # bin.readUInt8(mindex + 46).toString(2).padStart(6, "0"),
            "CliffBitMap": readUInt8(bin, mindex + 47),  # bin.readInt8(mindex + 47).toString(2).padStart(6, "0"),
            "?-8": bin[mindex + 48:mindex + 51],
            "OwnershipBuffer": OwnershipBuffer,
            "TileOverlayNum": TileOverlayNum,
            "buffer": bin[mindex + 55:mindex + 55 + buflength],
        })

        mindex += 55 + buflength

    return tilesmap

def getCityData(mainDecompressedData):
    bin = mainDecompressedData
    cities = {"cities": []}
    try:
        cityIndex = bin.index(b'\x04\x00\x00\x00\x43\x69\x74\x79')
        # There is some religion info as well at same section
        while cityIndex:
            cityNameLength = readUInt32(bin, cityIndex + 8)
            cityName = " ".join([x.capitalize() for x in bin[cityIndex + 12 + 14:cityIndex + 12 + cityNameLength].decode("utf-8").replace("_", " ").lower().split()])
            idx = cityIndex + 12 + cityNameLength
            cityCivIdx = readUInt16(bin, idx)
            # Unknown 1xUInt16
            civCityOrderIdx = readUInt16(bin, idx + 4)
            civCityOrderIdx1 = readUInt16(bin, idx + 6)
            cityLocationIdx = readUInt16(bin, idx + 8)
            # could be 32
            # 2x 00 00 00 00?
            cityOrderIdx = readUInt16(bin, idx + 18)
            cities["cities"].append({
                "CityName": cityName,
                "CivIndex": cityCivIdx,
                "CivCityOrderIdx": civCityOrderIdx,
                "CivCityOrderIdx1": civCityOrderIdx1,
                "LocationIdx": cityLocationIdx,
                "CityOrderIdx": cityOrderIdx,
            })
            try:
                cityIndex = bin.index(b'\x04\x00\x00\x00\x43\x69\x74\x79', cityIndex + 8)
            except:
                break
    except:
        print("No cities!")
        pass
    return cities

notiEnd = "_MESSAGE"  # or "_SUMMARY"

# Are these only player based notifications
def getNotifications(mainDecompressedData):
    binaryData = mainDecompressedData
    notifications = []
    try:
        notiIndex = binaryData.index(b'LOC_NOTIFICATION_')
        while notiIndex:
            notiNameLength = readUInt32(binaryData, notiIndex - 4)
            notiName = binaryData[notiIndex:notiIndex + notiNameLength].decode("utf-8")
            idx = notiIndex + notiNameLength

            notifications.append({
                "NotiName": notiName,
                "BinaryIdx": notiIndex,
            })
            try:
                notiIndex = binaryData.index(b'LOC_NOTIFICATION_', idx)
            except:
                break
    except:
        print("No notifications!")
        pass
    return notifications


def getDiploStates(mainDecompressedData, turn):
    base = b'\x05\x00\x00\x00'
    binaryData = mainDecompressedData
    diploStates = {}

    try:
        diploIndex = binaryData.index(b'DIPLO_STATE_') - 16
        currentPlayerId = readUInt32(binaryData, diploIndex + 4)
        currentPlayerBin = writeUInt32LE(currentPlayerId)
        targetPlayerId = readUInt32(binaryData, diploIndex + 8)

        while diploIndex:
            diploStateLength = readUInt32(binaryData, diploIndex + 12)
            diploState = binaryData[diploIndex + 16:diploIndex + 16 + diploStateLength].decode("utf-8")
            idx = diploIndex + 16 + diploStateLength

            targetPlayerId += 1
            targetPlayerBin = writeUInt32LE(targetPlayerId)

            nextSearch = base + currentPlayerBin + targetPlayerBin

            try:
                diploIndexCandidate = binaryData.index(nextSearch, idx)
                num1 = readUInt32(binaryData, diploIndexCandidate - 8)  # Major/Minor/Alive/Dead?
                num2 = readUInt32(binaryData, diploIndexCandidate - 4)  # Major/Minor/Alive/Dead?

                if currentPlayerId not in diploStates:
                    diploStates[currentPlayerId] = {}
                diploStates[currentPlayerId][targetPlayerId - 1] = {"state": diploState[12:], "num1": num1, "num2": num2}

                if binaryData[diploIndexCandidate + 16:diploIndexCandidate + 28] == b'DIPLO_STATE_':
                    diploIndex = diploIndexCandidate
                else:
                    # Find next player
                    currentPlayerId += 1
                    currentPlayerBin = writeUInt32LE(currentPlayerId)
                    try:
                        while True:
                            diploIndex = binaryData.index(b'DIPLO_STATE_', diploIndexCandidate + 28) - 16
                            currentPlayerId = readUInt32(binaryData, diploIndex + 4)
                            currentPlayerBin = writeUInt32LE(currentPlayerId)
                            targetPlayerId = readUInt32(binaryData, diploIndex + 8)
                            if targetPlayerId != 62:
                                break
                            else:
                                diploIndexCandidate = diploIndex
                    except:
                        # print("Couldn't find next player")
                        break
            except:
                print(f"File #{turn}: Something unexpected happened, "
                      f"when searching diploStates! nextSearch: {nextSearch}")
                pass
    except:
        print("No diplo states!")
        pass
    return diploStates


def getWars(mainDecompressedData, fileIdx):
    # # Always paired?
    # wRecTag = b'WarsReceived'
    # wDecTag = b'WarsDeclared'
    # # Cyclic war declarations can't be solved from these?
    #
    # binaryData = mainDecompressedData
    # wars = {}
    #
    # warCountIndexR = binaryData.index(wRecTag)
    # warCountIndexD = binaryData.index(wDecTag)

    wDecTag = b'LOC_HOF_GRAPH_PLAYER_WARS_DECLARED'
    wRecTag = b'LOC_HOF_GRAPH_PLAYER_WARS_RECEIVED'
    binaryData = mainDecompressedData

    receivers = getWarTagData(binaryData, wRecTag)
    declarers = getWarTagData(binaryData, wDecTag)

    return {"declarers": declarers, "receivers": receivers}


def getWarTagData(binaryData, wTag):

    warCountIndex = binaryData.index(wTag) + len(wTag) + 9
    warCounts = readUInt32(binaryData, warCountIndex)

    tags = []
    idx = warCountIndex + 4

    for i in range(warCounts):
        id = readUInt32(binaryData, idx)
        turnNum = readUInt32(binaryData, idx + 4)
        idx += 12
        tags.append({"turn": turnNum, "id": id})
    tags.sort(key=lambda war: war["turn"])
    return tags




