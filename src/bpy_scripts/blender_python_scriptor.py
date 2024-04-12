import asyncio
import os
import time 
import traceback
from datetime import datetime as dt


from bpy_scripts.message_manager import MessageManager
from nefx.logger import info
from threading import Thread
from utils.redis_remote import RedisClient
from bpy_scripts.generator import SampleGenerator


import config
import bpy_scripts.prefab_loader as pfl
import bpy_scripts.randomizor as rdr 
from nefx.ws_client import WebsocketAgent


DEFAULT_WS_URL = 'ws://localhost:11133/api/bps/'


class BlenderPythonScriptBuilder():
    '''
    建造者模式.
    用于创造bps主进程.
    '''
    def __init__(self) -> None:
        self._mm = None
        self._rc = None
        self._ws_url = None

    def add_ws_url(self, url):
        self._ws_url = url
        return self

    def build(self):
        '''
        建造bps实例, 如果没有额外配置则使用默认配置.
        '''
        # 以下为默认配置
        if not self._mm:
            self._mm = MessageManager(port=11133, route='/api/push-one-message')
        if not self._rc:
            self._rc = RedisClient.get_redis_client()
        if not self._ws_url:
            global DEFAULT_WS_URL
            self._ws_url = DEFAULT_WS_URL
        bps = BlenderPythonScript(
            message_manager=self._mm,
            redis_client=self._rc,
            websockets_url=self._ws_url
        )
        return bps


class BlenderPythonScript():
    def __init__(self, message_manager: MessageManager, redis_client: RedisClient, websockets_url) -> None:
        self._msg_mgr = message_manager
        self._rds_cli = redis_client
        # 启动WebsocketAgent
        # self._ws_agt = WebsocketAgent(websockets_url)
        # self._ws_agt.add_event_handler(self.message_event_handler)
        # self._ws_agt.run()

    def run(self):
        '''
        运行Blender脚本.
        '''
        info(f'开始运行Blender脚本, [blender_pid: {os.getpid()}].')
        # t = Thread(target=self.get_event_loop)
        # t.start()
        # asyncio.run(self.get_event_loop())
        self.render()

    # TODO: 实现事件循环.
    def get_event_loop(self):
        while True:
            time.sleep(5)

    def send_message(self, message):
        return self._ws_agt.send_message(message)

    def message_event_handler(self, message):
        if message:
            try:
                begin_render = self._rds_cli.r.get('begin_render')
                if begin_render:
                    self.render()
            except Exception as e:
                print(traceback.format_exc())
                print(e)

    def render(self):
        t0 = dt.now()
        t_last = t0
        pfl.load_all()
        iteration = config.get_render_count()
        for i in range(iteration):
            # pfl 在实例化原型物体时会重置 ins_col 以防止每次迭代重新创建物体
            res = {}
            t_pre_ins = dt.now()
            pfl.instantiate_all()
            t_pre_rdr = dt.now()
            res['time_ins'] = t_pre_rdr - t_pre_ins
            rdr.randomize_all()
            t_pre_gen = dt.now()
            res['time_rdr'] = t_pre_gen - t_pre_rdr

            # 每次运行 blender python 都会初始化这个类的单例，有且仅有一次
            # 单例的初始化意味着此次输出的文件夹是固定的
            res.update(SampleGenerator.get_sample_generator().output_one())
            res['time_total'] = dt.now() - t_pre_ins
            info(f"图像 ({i} of {iteration}) 渲染完成.")
            info(f"保存路径: {res['path_image']}.")
            info(f"实例化耗时: {res['time_ins']}.")
            info(f"随机化耗时: {res['time_rdr']}.")
            info(f"渲染耗时: {res['time_image']}.")
            info(f"标签耗时: {res['time_label']}.")
            info(f"累计耗时: {res['time_total']}.")
            info(f"bpy已运行时常: {dt.now() - t0}.")
            info('=' * 20)
        info(self.get_complete_text(iteration, dt.now() - t0)) 

    def get_complete_text(self, count, time):
        text = f'@   渲染任务已全部完成! 共计 {count} 枚图像, 耗时  {time} .   @'
        lens = 16 + len(text)
        line2 = '\n@' + ' ' * (lens - 2) + '@\n'
        return '\n' * 3 + '@' * lens + line2 + f'{text}' + line2 + '@'  * lens