import sys

sys.path.append('./src')
sys.path.append('./.venv/Lib/site-packages')

import config
from blender_codes.generator import SampleGenerator
import blender_codes.prefab_loader as pfl
import blender_codes.randomizor as rdr

import os
import traceback

from nefx.logger import info, get_message_queue
from utils.redis_remote import RedisClient


from datetime import datetime as dt

fd = None


def main():
    # 激活信息输出模块, 将log输出到redis
    rc = RedisClient.get_redis_client()
    render()
    # rdr.randomize_camera()
    # plr.get_camera()
    # info(sys.argv[-1])

def render():
    t0 = dt.now()
    t_last = t0
    t_curr = t0
    pfl.load_all()
    iteration = config.get_render_count()
    for i in range(iteration):
        # pfl 在实例化原型物体时会重置 ins_col 以防止每次迭代重新创建物体
        pfl.instantiate_all()
        rdr.randomize_all()

        # 每次运行 blender python 都会初始化这个类的单例，有且仅有一次
        # 单例的初始化意味着此次输出的文件夹是固定的
        SampleGenerator.get_sample_generator().output_one()
        t_curr = dt.now()
        info(f'图像 ({i + 1} of {iteration}) 输出完成, 已耗时：{t_curr - t_last}, 累计耗时: {t_curr - t0}')
        t_last = t_curr
    info(get_complete_text(iteration, dt.now() - t0)) 


def get_complete_text(count, time):
    text = f'@   渲染任务已全部完成! 共计 {count} 枚图像, 耗时 {time} .   @'
    lens = 16 + len(text)
    line2 = '\n@' + ' ' * (lens - 2) + '@\n'
    return '\n' * 3 + '@' * lens + line2 + f'{text}' + line2 + '@' * lens

if __name__ == '__main__':
    # sys.stdout = open(os.devnull, 'w')
    try:
        main()
    except Exception as e:
        print(traceback.format_exc())
        # print(e.args)
        os._exit(-1)
        # raise
    # sys.stdout = sys.__stdout__