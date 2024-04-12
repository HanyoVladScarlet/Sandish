import sys

sys.path.append('./src')
sys.path.append('./.venv/Lib/site-packages')

import config
from bpy_scripts.generator import SampleGenerator
import bpy_scripts.prefab_loader as pfl
import bpy_scripts.randomizor as rdr

import os
import traceback

from nefx.logger import info


from datetime import datetime as dt
from bpy_scripts.blender_python_scriptor import BlenderPythonScriptBuilder

import time


fd = None


def main():
    # 激活信息输出模块, 将log输出到redis
    bps = BlenderPythonScriptBuilder().build()
    bps.run()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(traceback.format_exc())
        os._exit(-1)
