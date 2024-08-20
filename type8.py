# for comments look at type6.py. slight differences in data field here but the rest the same
from pyais import  encode, util
from BinaryMessageTypes import MessageType_IMO289

bits=MessageType_IMO289.create().to_bitarray()
# print(bits)
bytes=util.bits2bytes(bits)
# print(bytes)


data={
    "mmsi": "003669739", #993 is for shore based or mobile station 00MID is for base station
    "dac":"001",
    "fid":"22",
    'type':8,
    'data': bytes
}
encoded=encode.encode_dict(data,'AIVDM')
print(encoded)


