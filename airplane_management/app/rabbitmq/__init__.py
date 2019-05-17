import pika
from retrying import retry


class RabbitMQ:

    @retry(stop_max_attempt_number=3, wait_fixed=10000)
    def connect(self):
        print(' x', 'Trying to connect to RabbitMQ...')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        print(' x', 'Connected to RabbitMQ')

        self.connection = connection
        self.channel = channel

        return connection, channel


rabbitmq_publish = RabbitMQ()
rabbitmq_consume = RabbitMQ()
