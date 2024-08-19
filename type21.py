

from pyais.encode import encode_dict

data={
    "mmsi": 993338338,
    'type':21,
    'aid_type':28,#from NAVAID TYPES for isolated danger
    'name':"WHALE",
    'virtual_aid':1,
    "lon": -70.67,#minutes/10000, need to write code to calculate this. I think its multiply lon/lat by 600000. didn't work. will try with regular
    "lat":41.52,#minutes/10000 #need to write code to calculate this
    "seconds":'60',#it wants seconds. for no2 doing 60=not available
    "to_bow":'1000',
    "to_stern":'1000',
    "to_port":'1000',
    "to_starboard":'1000'

}

encoded = encode_dict(data, talker_id="AIVDM")


print(encoded)
