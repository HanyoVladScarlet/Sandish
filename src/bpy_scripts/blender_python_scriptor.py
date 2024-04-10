import time 

from bpy_scripts.message_manager import MessageManager
from nefx.logger import info
from threading import Thread
from utils.redis_remote import RedisClient



class BlenderPythonScriptBuilder():

    def __init__(self) -> None:
        self._bps = BlenderPythonScript()
        self._message_manager = MessageManager(port=11133, route='/api/push-one-message')
        self._rc = RedisClient.get_redis_client()


    def build(self):
        return self._bps


class BlenderPythonScript():
    def run(self):
        '''
        运行Blender脚本.
        '''
        info('开始运行Blender脚本.')
        t = Thread(target=self.get_event_loop)
        t.start()


    # TODO: 实现事件循环.
    def get_event_loop(self):
        while True:
            time.sleep(5)