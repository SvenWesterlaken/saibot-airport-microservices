import json
import uuid

from ..rabbitmq import rabbitmq_publish
from ..util.rabbitmq_message import RabbitmqMessage

class Message_publisher:

    def __init__(self, host, exchange):
        self.host = host
        self.exchange = exchange

    def publish_message(self, message, queue, routing_key):
        rabbitmq_publish.channel.queue_declare(queue=queue)



        rabbitmq_publish.channel.basic_publish(exchange='',
                                       routing_key=routing_key,
                                       body=json.dumps(message))
