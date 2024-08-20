# I created this library to develop type 6 and 8 binary AIS messages. write now I only coded for IM0289. 
# Usage of the library can be seen in type6.py or type8.py
from pyais import messages
import attr
import datetime

# Default values are just the values that are being used. There is no reason to enter data later when can just set as default
@attr.s(slots=True)
class MessageType_IMO289(messages.Payload):
    # this has all the info: https://vislab-ccom.unh.edu/~schwehr/papers/2010-IMO-SN.1-Circ.289.pdf
    MLID=messages.bit_field(width=10,d_type=int,default=0)
    ND=messages.bit_field(width=7,d_type=int,default=2)
    Month=messages.bit_field(width=4,d_type=int, default=datetime.datetime.now().month)
    Day=messages.bit_field(width=5,d_type=int,default=datetime.datetime.now().day)
    Hour=messages.bit_field(width=5, d_type=int, default=datetime.datetime.now().hour)
    Minute=messages.bit_field(width=6,d_type=int, default=datetime.datetime.now().minute)
    Duration=messages.bit_field(width=18, d_type=int, default=1)
    Subshape=messages.bit_field(width=3,d_type=int, default = 0)
    shape=messages.bit_field(width=3,d_type=int,default=0)
    scale=messages.bit_field(width=2,d_type=int,default=1)
     #if were to use, would pull lat and lon this from json. right now its for whale next to woods hole
    lon = messages.bit_field(width=25, d_type=float, from_converter=messages.from_lat_lon, to_converter=messages.to_lat_lon, default=-70.67, signed=True)
    lat = messages.bit_field(width=24, d_type=float, from_converter=messages.from_lat_lon, to_converter=messages.to_lat_lon, default=41.52, signed=True)
    precision=messages.bit_field(width=3,d_type=int,default=4)
    radius=messages.bit_field(width=12,d_type=int, default=4000)
    spare=messages.bit_field(width=18,d_type=bytes, default=b'')#not sure if this should be 16 or 18. I think 18 but conflicting sources

# print(MessageType_IMO289.create())
