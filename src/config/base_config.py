# Author: Lyapunov
from config.config_loader import get_config, get_item
from utils.logger import error
import random

CONFIG = get_config()


def get_object_count():
    '''
    参与随机的物体个数
    '''
    key = 'instantiator'
    ins = get_item(key)
    return random.randint(ins['count_min'], ins['count_max'])


def get_base_path():
    '''
    存放base.blend文件的路径
    '''
    key = 'base_path'
    return get_item(key)


def get_background_paths():
    key = 'background_paths'
    return get_item(key)


def get_model_paths():
    '''
    存放models的.blend文件路径
    '''
    key = 'model_paths'
    return get_item(key)


def get_material_paths():
    '''
    存放material的.blend文件路径列表
    '''
    key = 'material_paths'
    return get_item(key)


def get_sand_volume_path():
    '''
    存放不同weather_volumes的.blend文件路径列表
    '''
    key = 'sand_volume_paths'
    return get_item(key)

