# 此文件用于创建 Flask 服务器
# 由此文件启用子进程来调用 Blender

from flask import Flask, request, render_template
from utils.redis_remote import RedisClient
import json
import os
import subprocess
import traceback
import signal
import time
from nefx.logger import info, warn


from nefx.logger import get_formatted_text


app = Flask(__name__)
app.config['SECTRET_KEY'] = 'secret!'


G_BEGIN = '\033[0;32;40m'
R_BEGIN = '\033[0;31;40m'
Y_BEGIN = '\033[0;33;40m'
COLOR_END = '\033[0m'


Q_SIZE = 10


blender_pid = -1


rc = RedisClient(flush=True)


class BlenderProcessManager():
    '''
    Blender子进程管理, 监视Blender进程数量,
    防止出现子进程数量异常报错
    '''
    _instance = None

    def __init__(self) -> None:
        self.p = None


    def start_rendering(self):
        if self.p is not None:
            warn('未启成功启动, 已经存在正在运行的Blender进程!')
            return
        self.p = subprocess.Popen(r'blender.exe blend_files\base\base.blend -b -P src/blender_codes/main.py')
        info('Blender正在运行!')
        return 


    def end_rendering(self):
        if self.p is None:
            warn('中止进程失败, 没有正在运行的Blender进程! ')
            return
        self.p.terminate()
        self.p = None
        info('Blender程序已退出! ')
        return


    @staticmethod
    def get_bpm():
        if BlenderProcessManager._instance == None:
            BlenderProcessManager._instance = BlenderProcessManager()
        return BlenderProcessManager._instance


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/api/end-rendering', methods=['GET'])
def end_rendering():
    BlenderProcessManager.get_bpm().end_rendering()
    return '{}'



@app.route('/api/start-rendering', methods=['POST'])
def start_rendering():
    data = request.data
    BlenderProcessManager.get_bpm().start_rendering()
    return '{}'


@app.route('/api/get-message-queue', methods=['GET'])
def update_message_queue():
    l = rc.get_messages()
    res = json.dumps(l)
    return res


def main():
    try:
        app.run(host='0.0.0.0', port=11133)
    except Exception as e:
        print(traceback.format_exc())
        os._exit(-1)


# def message_out():
#     for i in range(20):
#         message = {
#             'timestamp': time.time(),
#             'message': f'information{i}',
#             'level': 2
#         }
#         item = json.dumps(message)
#         rc.r.zadd('message_queue', {item: time.time()})
#     print(rc.r.zrange('message_queue', 0, -1, withscores=True))
#         # info(f'This is message {i}!')


if __name__ == '__main__':
    # start_rendering_process()
    main()
    # message_out()