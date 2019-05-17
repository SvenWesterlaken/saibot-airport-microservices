from . import rabbitmq

exchange = 'events'

def send_message_to_exchange(topic, message):
    rabbitmq.connect()

    channel = rabbitmq.channel
    channel.exchange_declare(
        exchange = exchange,
        exchange_type = 'fanout'
    )

    channel.basic_publish(
        exchange = exchange,
        routing_key = topic,
        body = message
    )

    rabbitmq.connection.close()
