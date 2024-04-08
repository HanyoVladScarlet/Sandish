# Author: Lyapunov.
import json
import os

from utils.logger import error, log, info

__all__ = ['get_config']

CONFIG = {}
config_path = './config/'


def get_config():
    global CONFIG
    if len(CONFIG) == 0:        
        CONFIG = load_config(config_path)
    return CONFIG


def get_item(key):
    '''
    基方法
    '''
    if not key in CONFIG:
        error(f'key: `{key}` 不在配置文件当中! ')
    return None if not key in CONFIG else CONFIG[key]


def load_config(base):
    config = {}
    if(not base.endswith('/')):
        base += '/'
    log(f'读取配置文件：{os.path.abspath(base)}')
    jsons = os.listdir(base)
    count = 0
    for i in jsons:
        if not i.endswith('.json'):
            continue 
        p = os.path.abspath(base + i)
        try:
            with open(p, encoding='utf-8') as f:
                new = json.load(f)
                for k in new:
                    config[k] = new[k]
                log(f'成功加载一页配置 ({count}/{len(jsons)}): `{p}`.')
                count += 1
        except:
            error(f'一个文件加载出错: `{p}`.')
    info(f'配置加载完成：共计: {count}页! ')
    return config