from pyais import  encode,util
from MessageType_IM0289 import MessageType_IM0289

# 1)
bits=MessageType_IM0289.create().to_bitarray()
print(bits)
bytes=util.bits2bytes(bits)
data={
    "mmsi": "003383383", #993 is for shore based or mobile station 00MID is for base station
    "dest_mmsi":"338338338",
    "dac":"001",
    "fid":"23",
    'type':6,
    'data': bytes
}
encoded=encode.encode_dict(data,'AIVDM')
print(encoded)

