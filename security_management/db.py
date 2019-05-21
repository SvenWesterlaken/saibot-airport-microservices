import redis, arrow, json
from retrying import retry
from env import redis_settings

class RedisWrapper:

    def __init__(self, settings):
        self._con_settings = settings

    @retry(stop_max_attempt_number=3, wait_fixed=10000, retry_on_result=lambda r: r is None)
    def connect(self):
        print(' x', 'Connecting to Redis')
        self.edis = redis.Redis(**self._con_settings)
        success = self.edis.ping()

        if success:
            print(' x', 'Connected to Redis')

        return self.edis if success else None

    def reconnect(self):
        try:
            self.edis.ping()
        except:
            self.connect()

    def save_event(self, ns_postfix, msg):
        namespace = 'events:' + ns_postfix
        timestamp =  arrow.now().timestamp

        pipe = self.edis.pipeline()
        pipe.zadd(namespace, {msg:timestamp}, nx=True)
        pipe.zadd('events', {msg:timestamp}, nx=True)

        return pipe.execute()

    def __convert_event(self, event):
        e, ts = event

        timestamp = arrow.get(ts).format('YYYY-MM-DD HH:mm:ss')
        event = json.loads(e.decode('UTF-8'))

        return {'ts': timestamp, 'event': event}

    def __convert_logs(self, event):
        e, ts = event

        timestamp = arrow.get(ts).format('YYYY-MM-DD HH:mm:ss')
        event = json.loads(e.decode('UTF-8'))

        return f'[{timestamp}] ' + event['message']

    def get_events(self, ns='events', min_date=False, max_date=False, desc=False ,logs=False):

        min = arrow.get(min_date).timestamp if min_date else '-inf'
        max = arrow.get(max_date).timestamp if max_date else '+inf'
        name = ns if ns is 'events' else 'events:' + ns
        map_fun = self.__convert_logs if logs else self.__convert_event

        result = []

        if not desc:
            result = self.edis.zrangebyscore(name, min, max, withscores=True, score_cast_func=int)
        else:
            result = self.edis.zrevrangebyscore(name, max, min, withscores=True, score_cast_func=int)

        if len(result) > 0:
            result = list(map(map_fun, result))

        return (result, logs)

r = RedisWrapper(redis_settings)
