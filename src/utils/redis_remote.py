import json
import redis
import time


from nefx.logger import add_event_handler, get_formatted_text, error


MESSAGE_QUEUE = 'message_queue'
MAX_SIZE = 20


class RedisClient():
    '''
    用于承载redis通讯
    '''
    # statics
    redis_client = None


    def __init__(self, host='localhost', port='6379', decode_responses=True,password=114514, charset='utf-8', flush=False) -> None:
        '''
        flush参数为真时, 重置消息队列.
        '''
        self.host = host
        self.port = port
        self.password = password
        self.decode_responses = decode_responses
        self.charset = charset
        self.r = self.open_connect()
        if MESSAGE_QUEUE in self.r and flush:
            self.r.delete(MESSAGE_QUEUE)
        add_event_handler(self.r_query)


    def open_connect(self):
        return redis.Redis(host=self.host, port=self.port, decode_responses=self.decode_responses,password=self.password,charset=self.charset)


    def r_query(self, message):
        '''向redis服务器发送一条消息'''
        item = json.dumps(message)
        self.r.zadd(MESSAGE_QUEUE, {str(item): time.time()})


    def get_messages(self) -> list:
        '''
        返回一个列表, 其数据结构格式为:
        消息id: id
        verbose_level: level
        message_content: message
        '''
        content = self.r.zrange(MESSAGE_QUEUE, 0, int(time.time()), desc=True)
        try:
            return [json.loads(v) for v in content][0: MAX_SIZE]
        except Exception as e:
            error(e, False)
            return []


    def print_message(self):
        '''
        ⚠本函数用于测试
        '''
        l = []
        messages = self.get_messages()
        if messages is None or len(messages) == 0:
            print('message is empty')
            return
        for i in messages:
            l.append(get_formatted_text(i['message'], i['level']))
        print('\n'.join(l))
        return 


    # Singleton
    @staticmethod
    def get_redis_client(host='localhost',port='6379',decode_responses=True,password=114514,charset='utf-8',flush=False):
        if RedisClient.redis_client is None:
            RedisClient.redis_client = RedisClient(host=host, port=port, decode_responses=decode_responses,password=password,charset=charset,flush=flush)
        return RedisClient.redis_client