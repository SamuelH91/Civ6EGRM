import zlib
import numpy as np
from utils.binaryconvert import *

CHUNKSIZE = 64 * 1024


# /**
#  * Output a decompressed buffer from the primary zlib zip of the .Civ6Save file
#  * @param {Buffer} savefile
#  * @return {Buffer} decompressed
#  */
def decompress(saveFileBuffer):
    civsav = saveFileBuffer
    header, idxH = parseHeader(saveFileBuffer)
    jsons = parseJson(saveFileBuffer, idxH)
    modindex = civsav.rfind(b'MOD_TITLE')
    bufstartindex = civsav.index(b'\x78\x9c', modindex)
    bufendindex = civsav.rindex(b'\x00\x00\xFF\xFF')

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
    idx1 = 28 + gamespeedlen
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
        "GameSpeed": saveFileBuffer[28:idx1],
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

MAPSIZEDATA = {
    '1144': {"x": 44, "y": 26},
    '2280': {"x": 60, "y": 38},
    '3404': {"x": 74, "y": 46},
    '4536': {"x": 84, "y": 54},
    '5760': {"x": 96, "y": 60},
    '6996': {"x": 106, "y": 66},
}


# /**
#  * Convert compressed tile data in .Civ6Save file into json format
#  * @param {buffer} savefile
#  * @return {object} tiles
#  */
def save_to_map_json(mainDecompressedData):
    bin = mainDecompressedData
    mapstartindex = bin.index(b'\x0E\x00\x00\x00\x0F\x00\x00\x00\x06\x00\x00\x00')
    tiles = readInt32(bin, mapstartindex + 12)
    tileskey = str(tiles)
    map = {"tiles": [], "mapSize": [MAPSIZEDATA[tileskey]["x"], MAPSIZEDATA[tileskey]["y"]]}

    mindex = mapstartindex + 16

    for i in range(tiles):
        OwnershipBuffer = readUInt8(bin, mindex + 49)
        TileOverlayNum = readUInt32(bin, mindex + 51)
        buflength = 0

        if TileOverlayNum == 1:
            buflength += 24
        elif TileOverlayNum == 2:
            buflength += 44
        if OwnershipBuffer >= 64:
            buflength += 17

        # See bin-structure.md for WIP documentation on what each of these values are
        map["tiles"].append({
            "x": i % MAPSIZEDATA[tileskey]["x"],
            "y": np.floor(i / MAPSIZEDATA[tileskey]["x"]),
            "hexbin-location": mindex,
            "tile-length": 55 + buflength,
            "int16-1": readUInt16(bin, mindex),
            "int16-2": readUInt16(bin, mindex + 2),
            "int16-3": readUInt16(bin, mindex + 4),
            "int16-4": readUInt16(bin, mindex + 6),
            "Landmass": readUInt16(bin, mindex + 8),
            "Landmass1": readUInt16(bin, mindex + 10),
            "TerrainType": readUInt32(bin, mindex + 12),
            "FeatureType": readUInt32(bin, mindex + 16),
            "?-1": readUInt16(bin, mindex + 20),
            "LandSnowSea": readUInt32(bin, mindex + 22),
            "?-2": readUInt8(bin, mindex + 26),
            "Resource": readUInt32(bin, mindex + 27),
            "ResourceBoolean": readUInt16(bin, mindex + 31),
            "GoodyHut": readUInt32(bin, mindex + 33),
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

    return map

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
