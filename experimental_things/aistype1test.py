# NOT ACTUALLY USED IN PRGORAM
# This is a code to test a type 1 ais message. It creates a ship near the iselin lab in woods hole
from pyais.encode import encode_dict
import serial
data = {
    "type" : 1,
    "mmsi":338338338,
    "status" : 0,
    "turn" :0,
    "speed" :0,
    "lon" : -70.672167,
    "lat" : 41.524268,
    "course" : 3600,
    "heading" : 359,
    "second" : 59,

}
encoded=encode_dict(data,talker_id="AIVDM")
print(encoded)

ser=serial.Serial('/dev/ttyS0',38400)
ser.write((bytes(encoded[0]+"\r\n",'utf-8')))
