import json
import sys
import pika

from ..rabbitmq import rabbitmq_publish

class Message_publisher:

    def __init__(self, exchange):
        self.exchange = exchange

    def publish_message(self, message, routing_key):

        if rabbitmq_publish.connection.is_closed:
            rabbitmq_publish.connect()

        rabbitmq_publish.channel.exchange_declare(exchange=self.exchange, exchange_type='topic')

        routing_key = sys.argv[1] if len(sys.argv) > 2 else routing_key

        rabbitmq_publish.channel.basic_publish(exchange=self.exchange,
                                       routing_key=routing_key,
                                       body=json.dumps(message),
                                        properties=pika.BasicProperties(delivery_mode=2,))

        print(" [x] Sent %r:%r" % (routing_key, message))