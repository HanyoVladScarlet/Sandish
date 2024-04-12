import asyncio
import websockets


from threading import Thread
from typing import Callable


# TODO: 解决异步和多线程的混用问题.
class WebsocketAgent():
    def __init__(self, url: str) -> None:
        ''''''
        self._handlers = []
        self._url = url

    def run(self):
        '''
        在生成WebsocketAgent之后记得启动!
        '''
        t = Thread(target=self.open)
        t.start()

    async def open(self):
        async with websockets.connect(self._url) as websocket:
            while True:
                response = await websocket.recv()
                self.on_message_handler(response)

    async def send_message(self, message):
        await self._ws.send(message)
        return message

    def on_message_handler(self, raw_data):
        '''
        多线程执行handlers列表中的所有绑定函数.
        这里的raw_data是来自wsserver的原始dict.
        '''
        for h in self._handlers:
            t = Thread(target=h, args=[raw_data,], daemon=True)
            t.start()
        return

    def add_event_handler(self, func: Callable):
        '''
        eventhandler要求的函数签名, 有且只有一个字典类型的参数.
        在定义add_event_handler时, 要注意函数签名.
        '''
        self._handlers.append(func)

    def remove_event_handler(self, func: Callable):
        while func in self._handlers:
            self._handlers.remove(func)
        return

