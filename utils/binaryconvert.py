import struct

def readUInt8(buf, idx):
    return int(*struct.unpack('B', buf[idx:idx+1]))

def readUInt16(buf, idx):
    return int(*struct.unpack('H', buf[idx:idx+2]))

def readUInt32(buf, idx):
    return int(*struct.unpack('I', buf[idx:idx+4]))

def readInt8(buf, idx):
    return int(*struct.unpack('b', buf[idx:idx+1]))

def readInt16(buf, idx):
    return int(*struct.unpack('h', buf[idx:idx+2]))

def readInt32(buf, idx):
    return int(*struct.unpack('i', buf[idx:idx+4]))

def writeUInt32LE(value):
    return struct.pack('<I', value)


