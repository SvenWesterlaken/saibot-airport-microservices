from . import rabbitmq

def send_message_to_queue(queue, message):
    rabbitmq.connect()

    channel = rabbitmq.channel
    channel.queue_declare(queue = queue)

    channel.basic_publish(
        exchange = '',
        routing_key = queue,
        body = message
    )

    rabbitmq.connection.close()
