# 暂时先这样实现了
from nefx.extension_methods import extension_method
from nefx.night_edge import NefxCoreBuilder
import os
import time
# import requests

import queue
from typing import Callable
from threading import Thread


enable_log = False
enable_info = True

# 解决Windows NT平台无法变色bug[1]
if os.name == 'nt':
    os.system('')

message_queue = queue.Queue()
Q_SIZE = 10


handlers = []

G_BEGIN = '\033[0;32;40m'
R_BEGIN = '\033[0;31;40m'
Y_BEGIN = '\033[0;33;40m'
COLOR_END = '\033[0m'

@extension_method
def use_logger(self: NefxCoreBuilder, max_size=10):
    Q_SIZE = max_size
    return self


def error(text, enable_remote=True):
    '''
    这是一条错误!
    '''
    text = f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] {text}'
    if enable_remote:
        on_message({
            'timestamp': time.time(),
            'message': text,
            'level': 3
        })
    print(get_formatted_text(text, '3'))


def info(text, enable_remote=True):
    '''
    这是一条信息!
    '''
    text = f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] {text}'
    if enable_info:
        if enable_remote:
            on_message({
                'timestamp': time.time(),
                'message': text,
                'level': 1
            })
        print(get_formatted_text(text, '1'))


def log(text, enable_remote=True):
    '''
    这是一条日志!
    '''
    text = f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] {text}'
    if enable_log:
        if enable_remote:
            on_message({
                'timestamp': time.time(),
                'message': text,
                'level': 0
            })
        print(text)


def warn(text, enable_remote=True):
    '''
    这是一条警告!
    '''
    text = f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] {text}'
    if enable_remote:
        on_message({
            'timestamp': time.time(),
            'message': text,
            'level': 2
        })
    print(get_formatted_text(text, '2'))


# 本模块不涉及任何下游模块适配, 仅提供消息提取接口
def append_msg(msg, level, timestamp):
    '''
    向队列中添加一条消息
    '''
    data = {
        "timestamp": timestamp,
        'level': level,
        'message': msg
    }
    message_queue.put(data)
    if message_queue.qsize() > Q_SIZE:
        message_queue.get()
    # proxies = { 'http': None, 'https': None }
    # headers = { 'content-type': 'application/json' }
    # try:
    #     res = requests.post(remote_url, data=data, proxies=proxies)
    #     if res.status_code == 200:
    #         log(res.text, False)
    #     else:
    #         error('服务器返回错误信息!', False)
    # except:
    #     error(f'连接错误! 在文件 `{__file__}` 当中. ', False)
    return


def get_formatted_text(text, level):
    if level == '1':
        text = f'{G_BEGIN}{text}{COLOR_END}'
    if level == '2':
        text = f'{Y_BEGIN}{text}{COLOR_END}'
    if level == '3':
        text = f'{R_BEGIN}{text}{COLOR_END}'
    return text


def on_message(message):
    global handlers
    # print(f'Handler count: {len(handlers)}')
    for h in handlers:
        t = Thread(target=h, args=[message], daemon=True)
        t.start()
    return 


def add_event_handler(func: Callable):
    global handlers
    handlers.append(func)
    return


def remove_event_handler(func: Callable):
    while func in handlers:
        handlers.remove(func)
    return


def get_message_queue():
    '''
    返回一个队列, 其数据结构格式为:
    消息id: id
    verbose_level: level
    message_content: message
    '''
    return message_queue


if __name__ == '__main__':
    log('这是一条日志! ')
    info('这是一条信息! ')
    error('这是一条错误! ')
    warn('这是一条警告! ')


# 参考文献：
# [1] XiangZhong888@csdn. python无法print彩色字体. https://blog.csdn.net/m0_55186589/article/details/113745410.