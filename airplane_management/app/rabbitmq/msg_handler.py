from ..rabbitmq import rabbitmq_consume

class Message_consumer:

    def __init__(self, exchange):
        self.exchange = exchange

    def consume_message(self, routing_key):

        if rabbitmq_consume.connection.is_closed:
            rabbitmq_consume.connect()

        rabbitmq_consume.channel.exchange_declare(exchange='events', exchange_type='topic')

        result = rabbitmq_consume.channel.queue_declare('airplane-management', durable=True)
        queue_name = result.method.queue

        rabbitmq_consume.channel.queue_bind(
        exchange='events', queue=queue_name, routing_key=routing_key)

        def callback(ch, method, properties, body):
            print(" [x] %r:%r" % (method.routing_key, body))

        rabbitmq_consume.channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        rabbitmq_consume.channel.start_consuming()