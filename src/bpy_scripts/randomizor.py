import bpy
import random
import math
import bpy_scripts.prefab_loader as pfl
from mathutils import Vector
from utils.scene_setups import CameraSetup


def randomize_all():
    randomize_materials()
    randomize_position()
    randomize_camera()
    # print( bpy.data.objects.get('focus').location)


def randomize_materials():
    '''
    '''
    instance_col =  pfl.get_instance_col()
    materials = bpy.data.materials
    objects = instance_col.all_objects
    max = len(pfl.get_materials()) - 1
    if max == 0:
        return
    for o in objects:
        ran_idx = random.randint(0, max)
        mat = materials.get(pfl.get_materials()[ran_idx])
        o.data.materials[0] = mat


def randomize_position():
    objects = pfl.get_instance_col().all_objects
    # 弃用的接口.
    # set_random_position(objects)
    randomize_scatter(radius=.1, scatter_scale=2)


def randomize_background():
    background = bpy.data.collections.get('background')


def randomize_camera():
    ins_col = pfl.get_instance_col()
    if len(ins_col.all_objects) == 0:
        return

    pos = Vector()
    for o in ins_col.all_objects:
        pos += o.location
    pos /= len(ins_col.all_objects)
    focus = pfl.get_focus()
    a = pfl.get_instance_col().all_objects
    t = a[random.randint(0, len(a) - 1)]
    focus.location = t.location.copy() + Vector((0, 0, .1))
    cam_set = CameraSetup()
    cam_set.set_camera_at_random_direction(.9)


# 弃用的接口.
# 当scatter_scale过小时, 会导致时间成本暴涨.
def set_random_position(targets, radius = .1, scatter_scale = 8):
    pos_arr = []
    scatter_scale = max(scatter_scale, 1.5)
    dist_range = scatter_scale * radius * math.sqrt(len(targets))
    for t in targets:
        flag = True
        while flag:
            flag = False
            pos = Vector((random.random(), random.random(), 0)) 
            pos = pos * dist_range
            for p in pos_arr:
                dist = (pos - p).magnitude
                if dist < radius * 1.5:
                    flag = True
        t.location = pos
        t.rotation_euler = Vector((0, 0, random.random())) * 360
        t.dimensions = radius * Vector((1, 1, 1))
        pos_arr.append(t.location)
    
    return


def make_grid(dim, tars: list):
    '''
    形成一个宽度为dim的正方形网格, 并返回一组数量为count的格点的随机二维坐标.
    返回值为一个二元组列表: [(x, y), ...]
    '''
    dim = int(dim)
    count = len(tars)
    dim = dim if count < dim ** 2 else int(math.sqrt(count)) + 1
    samplee = list(range(dim**2))
    sam_res = random.sample(samplee, count)
    for i in range(count):
        pos = Vector((sam_res[i] % 10,sam_res[i] // 10, 0))
        tars[i].location = pos
    return 


def get_value_on_texture(x, y, tex=None):
    # t_names = bpy.data.textures.keys()
    if not tex:
        tex = bpy.data.textures.get('vector_cloud_tex')
        if not tex:
            tex = bpy.data.textures.new('vector_cloud_tex', type='CLOUDS')
    tex.cloud_type = 'COLOR'

    res = tex.evaluate(Vector((x, y, 0)))
    return (res[0] - .5, res[1] - .5) 


def get_value_by_image(x, y, img):
    return


VELOCITY_FACTOR = 10
DIST_THRESHOLD = 2.001
ENABLE_COLLISION_DETECT = True


def iterate_once(radius):
    '''
    进行一个步长的迭代.
    '''
    global VELOCITY_FACTOR 
    global DIST_THRESHOLD 
    global ENABLE_COLLISION_DETECT 

    tars = pfl.get_instance_col().all_objects

    for t in tars:
        loc = t.location
        delta = get_value_on_texture(loc.x, loc.y)
        delta_v = Vector((delta[0], delta[1], 0))
        post_loc = t.location + delta_v * VELOCITY_FACTOR
        if not ENABLE_COLLISION_DETECT:
            t.location = post_loc
            continue

        # TODO: 使用Blender内置的碰撞检测方法进行替换.
        # 进行碰撞检测.
        flag = True
        for t_exc in tars:
            if t_exc == t:
                continue
            dist = (t_exc.location - post_loc).magnitude
            if dist < DIST_THRESHOLD:
                flag = False
        if flag:
            t.location = post_loc


def randomize_scatter(radius=.1, scatter_scale=5):
    '''
    随机分散.
    后面使用刚体模拟.
    '''
    max_dist = radius * scatter_scale
    tars = pfl.get_instance_col().all_objects
    for t in tars:
        t.rotation_euler = Vector((0, 0, random.random())) * 360
        t.dimensions = radius * Vector((1, 1, 1))
    make_grid(int(max_dist), tars)
    iterate_once(radius)
