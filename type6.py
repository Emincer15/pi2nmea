# creating a type six IMO289 message for whale next to woods hole
from pyais import  encode,util
from BinaryMessageTypes import MessageType_IMO289

# creates message using IMO289 library default values which i set to the values I want. Also converts to bitarray.
bits=MessageType_IMO289.create().to_bitarray()

# converts bits to bytes
bytes=util.bits2bytes(bits)
# creates type six message
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

