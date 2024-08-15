from pyais import  encode,util
from MessageType6A import MessageType6A

# 1)
bits=MessageType6A.create().to_bitarray()
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

