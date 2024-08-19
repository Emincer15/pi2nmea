from pyais import  encode, util
from MessageType_IM0289 import MessageType_IM0289

# 1)
bits=MessageType_IM0289.create().to_bitarray()
print(bits)
bytes=util.bits2bytes(bits)
print(bytes)
data={
    "mmsi": "003669739", #993 is for shore based or mobile station 00MID is for base station
    "dac":"001",
    "fid":"22",
    'type':8,
    'data': bytes
}
encoded=encode.encode_dict(data,'AIVDM')
print(encoded)


