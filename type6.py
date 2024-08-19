from pyais import  encode,util
from BinaryMessageTypes import MessageType_IMO289

bits=MessageType_IMO289.create().to_bitarray()
# print(bits)
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

