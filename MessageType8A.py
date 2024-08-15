# this is to try to replicate the message from the example to see if it works. DAC AND FID wouldn't be in my library in real life
from pyais import messages
import attr
import datetime

@attr.s(slots=True)
class MessageType8A(messages.Payload):
    MLID=messages.bit_field(width=10,d_type=int,default=0)
    ND=messages.bit_field(width=7,d_type=int,default=0)
    Month=messages.bit_field(width=4,d_type=int, default=datetime.datetime.now().month)
    Day=messages.bit_field(width=5,d_type=int,default=datetime.datetime.now().hour)
    Hour=messages.bit_field(width=5, d_type=int, default=datetime.datetime.now().minute)
    Minute=messages.bit_field(width=6,d_type=int, default=34)
    Duration=messages.bit_field(width=18, d_type=int, default=1)
    shape=messages.bit_field(width=3,d_type=int,default=0)
    scale=messages.bit_field(width=2,d_type=int,default=1)
    lon = messages.bit_field(width=25, d_type=float, from_converter=messages.from_lat_lon, to_converter=messages.to_lat_lon, default=-70.67, signed=True) #will eventually pull this from json
    lat = messages.bit_field(width=24, d_type=float, from_converter=messages.from_lat_lon, to_converter=messages.to_lat_lon, default=41.52, signed=True)
    precision=messages.bit_field(width=3,d_type=int, default=4)
    radius=messages.bit_field(width=12,d_type=int, default=33120)
    spare=messages.bit_field(width=18,d_type=bytes, default=b'')#not sure if this should be 16 or 18


# encoded=MessageType8A.create().to_bitarray()
# print(encoded)
