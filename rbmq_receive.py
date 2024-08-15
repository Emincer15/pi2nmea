import pika
from pika.exchange_type import ExchangeType
from datetime import datetime
import json
import functions
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
cfg.rbmq_routing_key = 'sample_validated.*'
cfg.rbmq_heartbeat_s = 300
cfg.rbmq_queue = 'ais_broadcast'


# this is the callback that will run everytime your receive a message, your processing code goes here
def on_message_received(ch, method, properties, body):
    # print(f"received new message: {body}")
    # do some work, send nmea broadcast
    lat,lon=functions.getlatlon(body)
    print(lat)
    print(lon)
    message=functions.createmessage(lat,lon)
    functions.sendmessage(message)
    # # acknowledge msg on succe, uncomment for debugging so you can read the same message again and again
    channel.basic_ack(method.delivery_tag)


credentials = pika.PlainCredentials(cfg.rbmq_user,cfg.rbmq_password)
connection_parameters = pika.ConnectionParameters(cfg.rbmq_host,
                                                  cfg.rbmq_port,
                                                  cfg.rbmq_vhost,
                                                  credentials)
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

queue = channel.queue_declare(queue=cfg.rbmq_queue, exclusive=False, durable=True)


channel.queue_bind(exchange=cfg.rbmq_exchange, queue=queue.method.queue, routing_key=cfg.rbmq_routing_key)
channel.basic_qos(prefetch_count=1) # use first available worker
channel.basic_consume(queue=queue.method.queue, auto_ack=False,   on_message_callback=on_message_received)

channel_rdy = connection.channel()

print("Starting Consuming")
channel.start_consuming()
