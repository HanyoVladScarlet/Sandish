import bpy
import random
import math
import prefab_loader as pfl
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
    for o in objects:
        ran_idx = random.randint(0, len(pfl.get_materials()) - 1)
        mat = materials.get(pfl.get_materials()[ran_idx])
        o.data.materials[0] = mat

def randomize_position():
    objects = pfl.get_instance_col().all_objects
    set_random_position(objects)


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


def randomize_scatter(targets, min_dist = 2.9, max_dist = 5):
    '''
    随机分散
    后面使用刚体模拟
    '''
    