
from saveFileHandler.filehandler import *

f = open("data/GANDHI 2 3960 BC 4.Civ6Save", "rb")
data = f.read()
f.close()

decompressedData = decompress(data)
#decompressedData = seeAll(decompressedData)
decompressedData = revealMap(decompressedData)

data2 = recompress(data, decompressedData)

f = open("data/GANDHI 2 3960 BC 4 r.Civ6Save", "wb")
data = f.write(data2)
f.close()