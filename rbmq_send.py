# Fox's send file. Only thing changed is the three neccessary lines so python doesn't throw an error
# set to automatically change lat and lon within a small area around woods hole so still visible on map
import pika
from pika.exchange_type import ExchangeType
from datetime import datetime
import json

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


cfg = dotdict()
cfg.rbmq_host = 'deep2.whoi.edu'
cfg.rbmq_port = 5672
cfg.rbmq_user = 'local'
cfg.rbmq_password = 'localingest'
cfg.rbmq_vhost = '/'
cfg.rbmq_exchange = 'ingest'
cfg.rbmq_routing_key = 'sample_validated.DUMMY'
cfg.rbmq_heartbeat_s = 300


credentials = pika.PlainCredentials(cfg.rbmq_user, cfg.rbmq_password)
cfg.connection_parameters = pika.ConnectionParameters(host=cfg.rbmq_host,
                                                  port=cfg.rbmq_port,
                                                  virtual_host=cfg.rbmq_vhost,
                                                  credentials=credentials,
                                                  heartbeat=cfg.rbmq_heartbeat_s)


def connect(params, exchange):
    print("establishing connection to broker ...")
    connection = pika.BlockingConnection(cfg.connection_parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type=ExchangeType.topic)
    return channel

def sendMSG(channel, exchange, routing_key, message):
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=json.dumps(message, allow_nan=True, default=str))


cfg.channel = connect(cfg.connection_parameters,cfg.rbmq_exchange)

if cfg.channel.is_open:
    print("RBMQ channel status:\t OPEN")
else:
    print("RBMQ channel status:\t CLOSED")
# these three lines neccessary
null=None
true=True
false=False
# test message
import random
message={"px": 447, "py": 143, "bbw": 18, "bbh": 18, "prob": 0.76, "prob_int": 760, "score": 8, "activity": 0.003, "id": 18, "source_id": 0, "ts": "2024-03-04 18:11:51", "ts_date": "2024-03-04", "ts_time": "18:11:51", "ts_file": "20240304-181151", "project": "APSOUTH", "camcalib": "../gcfg/camcalib_apsouth_202308.json", "dist": 979, "bearing": 148.36, "lat": 41.53+(random.randint(1,9))/1000, "lon": -70.67+(random.randint(1,9))/1000, "path": "/media/active/ws/2024/03/04/18", "file": "20240304-181151_x447y143_prob0760_score8_id18_APSOUTH_cam0.mp4", "base_path": "ws_apsouth", "sample_path": "/mnt/ws_data/ws_apsouth/2024/03/04/18", "sample_rgbfile": null, "x_offset": null, "new_label": "1", "tag_label": null, "exclude_tag": null, "parent": null, "child": null, "manual": null, "user": null, "last_modified": null, "comment": null, "project_id": 6, "evaluation_id": 9, "distance_str": "979 m", "video_url": "http://131.188.117.95:8881/data/ws_apsouth/2024/03/04/18/20240304-181151_x447y143_prob0760_score8_id18_APSOUTH_cam0.mp4", "username": "RT_team", "last_modified_ts": "2024-03-04 18:12:04", "species_name": "Killer Whale", "cue_ir": null, "cue_vis": null, "project_name": "APSOUTH", "timestamp": "2024-03-04 18:11:51", "event_id": 18, "prev_not_true": true, "first_modified": "2024-03-04 18:12:04"}



sendMSG(cfg.channel, cfg.rbmq_exchange, cfg.rbmq_routing_key, message)
print("RBMQ msg -> success")
