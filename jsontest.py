import json
f=open('test.json')
data=json.load(f)
print(data.get("lat"))
print(data.get("lon"))
print(data.get("bearing"))
f.close