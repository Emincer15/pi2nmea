import json
from pyais.encode import encode_dict
import serial


class dotdict(dict):
    """
    enables .access on dicts
    """
    def __getattr__(self, attr):
        if attr.startswith('__'):
            raise AttributeError
        return self.get(attr, None)
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__



def getlatlon(msg):
    msg=json.loads(msg)
    lat=msg.get('lat')
    lon=msg.get('lon')
    return lat, lon
null=None
true=True
false=False
message={"px": 447, "py": 143, "bbw": 18, "bbh": 18, "prob": 0.76, "prob_int": 760, "score": 8, "activity": 0.003, "id": 18, "source_id": 0, "ts": "2024-03-04 18:11:51", "ts_date": "2024-03-04", "ts_time": "18:11:51", "ts_file": "20240304-181151", "project": "APSOUTH", "camcalib": "../gcfg/camcalib_apsouth_202308.json", "dist": 979, "bearing": 148.36, "lat": 48.85308637037716, "lon": -123.34530416468988, "path": "/media/active/ws/2024/03/04/18", "file": "20240304-181151_x447y143_prob0760_score8_id18_APSOUTH_cam0.mp4", "base_path": "ws_apsouth", "sample_path": "/mnt/ws_data/ws_apsouth/2024/03/04/18", "sample_rgbfile": null, "x_offset": null, "new_label": "1", "tag_label": null, "exclude_tag": null, "parent": null, "child": null, "manual": null, "user": null, "last_modified": null, "comment": null, "project_id": 6, "evaluation_id": 9, "distance_str": "979 m", "video_url": "http://131.188.117.95:8881/data/ws_apsouth/2024/03/04/18/20240304-181151_x447y143_prob0760_score8_id18_APSOUTH_cam0.mp4", "username": "RT_team", "last_modified_ts": "2024-03-04 18:12:04", "species_name": "Killer Whale", "cue_ir": null, "cue_vis": null, "project_name": "APSOUTH", "timestamp": "2024-03-04 18:11:51", "event_id": 18, "prev_not_true": true, "first_modified": "2024-03-04 18:12:04"}
body=json.dumps(message, allow_nan=True, default=str)
lat,lon=getlatlon(body)

def createmessage(lat,lon):
    data={
        "mmsi": 993338338,
        'type':21,
        'aid_type':28,#from NAVAID TYPES for isolated danger
        'name':"WHALE",
        "lon": lon,
        "lat":lat,
        "seconds":'60',
        "to_bow":'1000',
        "to_stern":'1000',
        "to_port":'1000',
        "to_starboard":'1000'
    }
    encoded = encode_dict(data, talker_id="AIVDM")
    return encoded
# message=createmessage(42,42)
# print(message)


def sendmessage(sending):
    ser=serial.Serial('/dev/ttyS0',38400)
    ser.write((bytes(sending[0]+"\r\n",'utf-8')))#I think these are right carriage returns. I don't know.
    #print(bytes(sending[0]+'/r/n','utf-8'))
# testsend=sendmessage(['!AIVDM,1,1,,A,E>kDSpf;T0V2P000000000000001P8F0<12h7wwwwp000000000000000000,4*67'])
