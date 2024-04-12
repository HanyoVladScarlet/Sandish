import subprocess
import traceback


from nefx.logger import info, warn
from nefx.secret import get_random_combination
from typing import Callable
from flask_sse import sse

from utils.redis_remote import RedisClient


class BlenderProcessManager():
    '''
    *单例模式*
    Blender子进程管理, 监视Blender进程数量,
    防止出现子进程数量异常报错
    '''
    _instance = None

    def __init__(self) -> None:
        self.p = None
        self._blender_token = None

    @property
    def exists_blender_process(self):
        return self.p is not None


    def start_rendering(self):
        try:
            if self.p is not None:
                warn('未启成功启动, 已经存在正在运行的Blender进程!')
                return
            self._blender_token = get_random_combination()
            self.p = subprocess.Popen(r'blender.exe blend_files\base\base.blend -b -P src/bpy_scripts/main.py')
            info('Blender正在运行!')
            return True
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            return False


    def end_rendering(self):
        '''
        结束渲染进程.
        '''
        try:
            if self.p is None:
                warn('中止进程失败, 没有正在运行的Blender进程! ')
                return
            self.p.terminate()
            # 从redis中清除blender进程.
            self.p = None
            self._blender_token = None
            warn('Blender程序已退出! ')
            return True
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            return False

    @staticmethod
    def get_bpm():
        '''
        单例模式, 获得实例对象.
        :return: <BlenderProcessManager>
        '''
        if BlenderProcessManager._instance == None:
            BlenderProcessManager._instance = BlenderProcessManager()
        return BlenderProcessManager._instance


def emitBackendEvent(event_type: str):
    '''
    使用这个装饰器来通知前端属性变动.
    其中 event_type 用于制定前端事件.
    data 来自于被装饰函数的参数, 是字典类型.
    '''
    def outer_wrapper(func: Callable):
        def wrapper(data={}, *args, **kargs):
            res = func(*args, **kargs)
            sse.publish(data, event_type)
            return res
        return wrapper
    return outer_wrapper


class BlenderEventEmitter():
    '''
    *单例模式*
    用于触发消息推送事件
    '''
    def emit(self, func, name, data):
        
        return


    @staticmethod
    def get_blender_event_emitter():
        if BlenderEventEmitter._instance == None:
            BlenderEventEmitter._instance = BlenderEventEmitter()
        return BlenderEventEmitter._instance