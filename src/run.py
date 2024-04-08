# 此文件用于创建 Flask 服务器
# 由此文件启用子进程来调用 Blender

from flask import Flask, request, render_template
from flask_socketio import SocketIO
import queue
import json


from utils.logger import get_formatted_text


app = Flask(__name__)
app.config['SECTRET_KEY'] = 'secret!'
socketio = SocketIO(app)
message_queue = queue.Queue()


G_BEGIN = '\033[0;32;40m'
R_BEGIN = '\033[0;31;40m'
Y_BEGIN = '\033[0;33;40m'
COLOR_END = '\033[0m'


Q_SIZE = 10


@app.route('/',methods=['GET'])
def hello_world():
    data = {

    }
    return render_template('index.html', data=data)

@app.route('/blenderpost', methods=['POST'])
def recv_msg():
    data = request.form
    # print(data)
    text = data['message']
    level = data['level']
    print(get_formatted_text(text, level))
    message_queue.put(data)
    if message_queue.qsize() > Q_SIZE:
        message_queue.get()
    return 'One piece of info has been received by remote.'


@app.route('/api/get-message-queue', methods=['GET'])
def update_message_queue():
    res = []
    for i in message_queue.queue:
        res.append(i)
    # print(res)
    return json.dumps(res)
    # return 'haoye!'

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=11133)