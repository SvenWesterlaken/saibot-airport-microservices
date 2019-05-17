import pika, functools, time
from . import msg_handler

class RabbitMQConsumer:
    EXCHANGE = 'events'
    EXCHANGE_TYPE = 'topic'

    def __init__(self, amqp_url, q_name, routing_key):
        self.pers_properties = pika.BasicProperties(delivery_mode=2)

        self.should_reconnect = False
        self.was_consuming = False

        self._queue = q_name
        self._routing_key = routing_key

        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._url = amqp_url
        self._prefetch_count = 1
        self._closing = False
        self._consuming = False

    def connect(self):
        print(' x', 'Trying to connect to RabbitMQ on', self._url)

        return pika.SelectConnection(
            parameters=pika.URLParameters(self._url),
            on_open_callback=self.on_con_open,
            on_open_error_callback=self.on_con_open_error_cb,
            on_close_callback=self.on_close_cb
        )

    def close_connection(self):
        self._consuming = False

        if self._connection.is_closing or self._connection.is_closed:
            print(' x', 'Connection is closing or already closed')
        else:
            print(' x', 'Closing connection')
            self._connection.close()

    def on_con_open(self, _unused_connection):
        print(' x', 'Connected to RabbitMQ')
        self.open_channel()

    def on_con_open_error_cb(self, _unused_connection, err):
        print(' x', 'Couldn\'t connect to RabbitMQ:', err)
        self.reconnect()

    def on_close_cb(self, _unused_connection, reason):
        self._channel = None

        if self._closing:
            self._connection.ioloop.stop()
        else:
            print(' x', 'Connection closed, reconnect necessary', reason)
            self.reconnect()

    def reconnect(self):
        self.should_reconnect = True
        self.stop()

    def open_channel(self):
        print(' x', 'Creating new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        print(' x', 'Channel Opened')
        self._channel = channel
        self._channel.add_on_close_callback(self.on_channel_closed)
        self.setup_exchange(self.EXCHANGE)

    def on_channel_closed(self, channel, reason):
        print(' x', 'Channel', channel, 'was closed:', reason)
        self.close_connection()

    def setup_exchange(self, name):
        cb = functools.partial(self.on_exchange_declareok, userdata=name)
        self._channel.exchange_declare(exchange=name, exchange_type=self.EXCHANGE_TYPE, callback=cb)

    def on_exchange_declareok(self, _unused_frame, userdata):
        print(' x', 'Exchange declared', userdata)
        self.setup_queue(self._queue)

    def setup_queue(self, q_name):
        cb = functools.partial(self.on_queue_declareok, userdata=q_name)
        self._channel.queue_declare(queue=q_name, callback=cb, durable=True)

    def on_queue_declareok(self, _unused_frame, userdata):
        print(' x', 'Binding', self.EXCHANGE, 'to', userdata, 'with', self._routing_key)
        cb = functools.partial(self.on_bindok, userdata=userdata)
        self._channel.queue_bind(q_name, self.EXCHANGE, routing_key=self._routing_key, callback=cb)

    def on_bindok(self, _unused_frame, userdata):
        print(' x', 'Queue bound:', userdata)
        self.set_qos()

    def set_qos(self):
        self._channel.basic_qos(prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, _unused_frame, userdata):
        print(' x', 'QOS set for', userdata[0], 'to:', self._prefetch_count)
        self.start_consuming(userdata)

    def start_consuming(self):
        print(' x', 'Issuing consumer related RPC commands')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)
        consumer_tag = self._channel.basic_consume(self._queue, self.on_message)
        self.was_consuming = True
        self._consuming = True

    def on_consumer_cancelled(self, method_frame):
        print(' x', 'Consumer was cancelled remotely, shutting down', method_frame)

        if self._channel:
            self._channel.close()

    def on_message(ch, basic_deliver, properties, body):
        print(f" [x] {method.routing_key}: {body}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        if not self._closing:
            self._closing = True
            print(' x', 'Stopping RabbitMQ')

        if self._consuming:
            self._stop_consuming()
            self._connection.ioloop.start()
        else:
            self._connection.ioloop.stop()

        print(' x', 'Stopped RabbitMQ')

class RabbitMQ:
    def __init__(self, amqp_url, consumers):
        self._reconnect_delay = 0
        self._reconnect_tries = 0
        self._amqp_url = amqp_url

        for q_name, rk in consumers:
            self._q_name = q_name
            self._rk = rk
            self._consumer = RabbitMQConsumer(self._amqp_url, q_name, rk)

    def run(self):
        while self._reconnect_tries < 3:
            try:
                self._consumer.run()
            except KeyboardInterrupt:
                self._consumer.stop()
                break

            self._maybe_reconnect()

    def _maybe_reconnect(self):
        if self._consumer.should_reconnect:
            self._consumer.stop()
            reconnect_delay = self._get_reconnect_delay()
            print(f'Reconnecting after {reconnect_delay} seconds')
            time.sleep(reconnect_delay)
            self._consumer = RabbitMQConsumer(self._amqp_url, self._q_name, self._rk)

    def _get_reconnect_delay(self):
        if self._consumer.was_consuming:
            self._reconnect_delay = 0
        else:
            self._reconnect_delay += 1
        if self._reconnect_delay > 30:
            self._reconnect_delay = 30
        return self._reconnect_delay




rabbitmq = RabbitMQ('amqp://guest:guest@rabbitmq:5672/', consumers=[('f_mn_test', 'test')])
