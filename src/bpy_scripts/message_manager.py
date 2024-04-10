import json
import requests
from threading import Thread

from nefx.logger import add_event_handler


class MessageManager():
    '''
    用于向服务器发送消息.
    '''


    def __init__(self, host='127.0.0.1', port='5847', route='/api') -> None:
        self._host = host
        self._port = port
        self._route = route
        add_event_handler(self.push_logger_message)


    @property
    def target_url(self):
        return f'http://{self._host}:{self._port}{self._route}'


    def push_logger_message(self, message):
        '''
        修饰由logger发送来的message.
        具体来讲就是添加event_type.
        '''
        message['event_type'] = 'console_message'
        return self.push_message(message=message)


    def push_message(self, message):
        '''
        向服务器推送一条消息.
        '''
        data = json.dumps(message)
        return requests.post(url=self.target_url, data=data)


if __name__ == '__main__':
    data = {
        'message': 'I\'m a message.',
        'type': 'test'
    }

    mm = MessageManager(port=11133)
    res = mm.push_message(data=data)