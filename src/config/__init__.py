import os
import json

from config.config_loader import *
from config.base_config import *
from config.render_config import *

__all__ = ['CONFIG', 'initialize']

CONFIG = {}

def read(base="./config/"):
    config = {}
    if(not base.endswith('/')):
        base += '/'
    for i in os.listdir(base):
        if not i.endswith('.json'):
            continue 
        p = base + i
        try:
            with open(p, encoding='utf-8') as f:
                new = json.load(f)
                for k in new:
                    config[k] = new[k]
        except:
            print(f'一个文件加载出错：{p}')
    return config


def initialize():
    '''
    初始化配置
    '''
    global CONFIG
    CONFIG = read()


if(len(CONFIG) == 0):
    initialize()


if __name__ == "__main__":
    initialize()
    print(CONFIG)