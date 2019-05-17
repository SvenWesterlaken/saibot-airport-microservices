
def message_callback(ch, basic_deliver, properties, body):

    print(f" [x] {method.routing_key}: {body}")

    ch.basic_ack(delivery_tag=method.delivery_tag)
