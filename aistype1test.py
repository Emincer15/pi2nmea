from pyais.encode import encode_dict
data = {
    "type" : 1,
    "mmsi":338338338,
    "status" : 0,
    "turn" :0,
    "speed" :0,
    "lon" : -70.67,
    "lat" : 42.52,
    "course" : 3600,
    "heading" : 359,
    "second" : 59,

}
encoded=encode_dict(data,talker_id="AIVDM")
print(encoded)