import sys

sys.path.append('./src')

import config
import bpy
import generator as ge
import prefab_loader as pfl
import randomizor as rdr
import time 
import datetime
import os


from mathutils import Vector
from utils.logger import info


from datetime import datetime as dt

fd = None


COMPLETE_TXT = '渲染任务已全部完成! 共计'


def main():
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
        pfl.instantiate_all()
        rdr.randomize_all()
        ge.output_one()
        t_curr = dt.now()
        info(f'图像 ({i + 1} of {iteration}) 输出完成, 已耗时：{t_curr - t_last}, 累计耗时: {t_curr - t0}')
        t_last = t_curr
    info(get_complete_text(iteration, stretch)) 


def get_complete_text(count, time):
    text = f'@   渲染任务已全部完成! 共计 {count} 枚图像, 耗时 {time} .   @'
    lens = 16 + len(text)
    line2 = '\n@' + ' ' * (lens - 2) + '@\n'
    return '\n' * 3 + '@' * lens + line2 + f'{text}' + line2 + '@' * lens

if __name__ == '__main__':
    sys.stdout = open(os.devnull, 'w')
    main()
    # sys.stdout = sys.__stdout__