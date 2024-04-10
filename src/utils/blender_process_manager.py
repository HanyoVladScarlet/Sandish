import subprocess


from nefx.logger import info, warn
from nefx.secret import get_random_combination
from typing import Callable
from flask_sse import sse


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
    def blender_token(self):
        '''
        返回一个确认 Blender 进程
        '''
        return self._blender_token


    def start_rendering(self):
        if self.p is not None:
            warn('未启成功启动, 已经存在正在运行的Blender进程!')
            return
        self._blender_token = get_random_combination()
        # 在这里将blendertoken以命令行形式传递
        self.p = subprocess.Popen(r'blender.exe blend_files\base\base.blend -b -P src/bpy_scripts/main.py')
        info('Blender正在运行!')
        return 


    def end_rendering(self):
        '''
        结束渲染进程.
        '''
        if self.p is None:
            warn('中止进程失败, 没有正在运行的Blender进程! ')
            return
        self.p.terminate()
        self.p = None
        self._blender_token = None
        warn('Blender程序已退出! ')
        return


    @staticmethod
    def get_bpm():
        '''
        单例模式, 获得实例对象
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