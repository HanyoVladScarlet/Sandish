# 暂时先这样实现了

import time
import os
import requests
import asyncio


enable_log = False
enable_info = True

remote_url = 'http://localhost:11133/blenderpost'

# 解决Windows NT平台无法变色bug[1]
if os.name == 'nt':
    os.system('')


G_BEGIN = '\033[0;32;40m'
R_BEGIN = '\033[0;31;40m'
Y_BEGIN = '\033[0;33;40m'
COLOR_END = '\033[0m'


def error(text, enable_remote=True):
    '''
    这是一条错误!
    '''
    text = f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] {text}'
    if enable_remote:
        asyncio.run(send_msg(text, '3'))
    print(get_formatted_text(text, '3'))


def info(text, enable_remote=True):
    '''
    这是一条信息!
    '''
    text = f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] {text}'
    if enable_info:
        if enable_remote:
            asyncio.run(send_msg(text, '1'))
        print(get_formatted_text(text, '1'))



def log(text, enable_remote=True):
    '''
    这是一条日志!
    '''
    text = f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] {text}'
    if enable_log:
        if enable_remote:
            asyncio.run(send_msg(text, '0'))
        print(text)


def warn(text, enable_remote=True):
    '''
    这是一条警告!
    '''
    text = f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] {text}'
    if enable_remote:
        asyncio.run(send_msg(text, '2'))
    print(get_formatted_text(text, '2'))


async def send_msg(msg, level):
    data = {
        "id": 0,
        'level': level,
        'message': msg
    }
    proxies = { 'http': None, 'https': None }
    headers = { 'content-type': 'application/json' }
    try:
        res = requests.post(remote_url, data=data, proxies=proxies)
        if res.status_code == 200:
            log(res.text, False)
        else:
            error('服务器返回错误信息!', False)
    except:
        error(f'连接错误! 在文件 `{__file__}` 当中. ', False)
    return


def get_formatted_text(text, level):
    if level == '1':
        text = f'{G_BEGIN}{text}{COLOR_END}'
    if level == '2':
        text = f'{Y_BEGIN}{text}{COLOR_END}'
    if level == '3':
        text = f'{R_BEGIN}{text}{COLOR_END}'
    return text


if __name__ == '__main__':
    log('这是一条日志! ')
    info('这是一条信息! ')
    error('这是一条错误! ')
    warn('这是一条警告! ')


# 参考文献：
# [1] XiangZhong888@csdn. python无法print彩色字体. https://blog.csdn.net/m0_55186589/article/details/113745410.