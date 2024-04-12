# 此文件用于创建 Flask 服务器
# 由此文件启用子进程来调用 Blender

import json
import os
import traceback


from flask import Flask, request, render_template
from flask_sse import sse
from flask_socketio import SocketIO, emit
from utils.redis_remote import RedisClient
from utils.blender_process_manager import BlenderProcessManager


app = Flask(__name__)
app.config['SECTRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['REDIS_URL'] = 'redis://:114514@localhost:6379/0'


# sse 注册.
app.register_blueprint(sse, url_prefix='/api/stream')
socketio = SocketIO(app, async_mode='threading') 


G_BEGIN = '\033[0;32;40m'
R_BEGIN = '\033[0;31;40m'
Y_BEGIN = '\033[0;33;40m'
COLOR_END = '\033[0m'


Q_SIZE = 10


rc = RedisClient(flush=True)


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/api/end-rendering', methods=['GET'])
def end_rendering():
    if BlenderProcessManager.get_bpm().end_rendering():
        sse.publish({'exists_blender': False}, 'update_slow')
    return '{}'


@app.route('/api/start-rendering', methods=['POST'])
def start_rendering():
    data = request.data
    if BlenderProcessManager.get_bpm().start_rendering():
        sse.publish({'exists_blender': True}, 'update_slow')
    return '{}'


@app.route('/api/get-message-queue', methods=['GET'])
def update_message_queue():
    l = rc.get_messages()
    res = json.dumps(l)
    return res


@app.route('/api/push-one-message', methods=['POST'])
def push_one_message():
    # ip地址过滤, 在不涉及集群的情况下, 暂时如此实现
    if request.remote_addr != '127.0.0.1':
        return '臭外地的来百京儿要饭来啦!'
    data = json.loads(request.data)
    print(data)
    if 'event_type' not in data:
        return '未指定事件类型'
    try:
        sse.publish(data, type=data['event_type'])
    except Exception as e:
        print(traceback.format_exc())
        print(e)
    return '{}'


@app.route('/api/stream')
def stream():
    return sse.stream()


@socketio.on('message')
def message_handler(message):
    '''
    ⚠注意: message是一个json字符串.
    '''
    try:
        data = json.loads(message)
        sse.publish(data, type='update_slow')
    except Exception as e:
        print(traceback.format_exc())
        print(e)


def main():
    try:
        # 注意flask默认单线程, 如果存在异步请求则可能造成线程阻塞
        socketio.run(app, host='0.0.0.0', port=11133)
        # app.run(host='0.0.0.0', port=11133, threaded=True)
    except Exception as e:
        print(traceback.format_exc())
        print(e)
        os._exit(-1)


if __name__ == '__main__':
    # start_rendering_process()
    try:
        main()
    except KeyboardInterrupt as e:
        BlenderProcessManager.get_bpm().end_rendering()
        print(e.__traceback__)