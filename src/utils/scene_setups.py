import bpy
import math
import random
from mathutils import Vector
import bpy_scripts.prefab_loader as pfl


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner


@singleton
class CameraSetup():
    '''
    Use this class to set camera looking at exact one target.
    An empty object is recommended to be used as target.
    '''
    def __init__(self, camera_name = 'Camera', target_name = 'focus') -> None:
        '''
        Initialize, especially create camera target.
        '''
        obj = bpy.data.objects.get(target_name)
        # Create an empty object at zero point if target is not found.
        if obj is None:
            self.target = bpy.data.objects.new(target_name, None)
            pfl.get_camera_col().objects.link(self.target)
            self.target.empty_display_type = 'PLAIN_AXES'
        else:
            self.target = obj

        self.camera_name = camera_name
        self.camera = bpy.data.objects[camera_name]


    def set_camera(self, distance: float, rot_x: float, rot_z: float):
        '''
        Look at target
        '''
        rot_x = min(rot_x, math.pi / 2)
        rot_x = max(rot_x, 0)
        x = self.target.location[0] + distance * math.sin(rot_x) * math.sin(rot_z)
        y = self.target.location[1] - distance * math.sin(rot_x) * math.cos(rot_z)
        z = self.target.location[2] + distance * math.cos(rot_x)

        self.camera.location = (x, y, z)
        self.camera.rotation_euler = (rot_x, 0, rot_z)


    def set_camera_fuzzed(self, distance: float, rot_x: float, rot_z: float, fuzz_d = .8, fuzz_x = .8, fuzz_z = .8):
        '''
        Look at target with random bias
        '''
        distance *= (random.random() * 2 - 1) * fuzz_d + 1
        # rot_x *= (random.random() * 2 - 1) * fuzz_x + 1
        rot_z *= (random.random() * 2 - 1) * fuzz_z + 1

        self.set_camera(distance, rot_x, rot_z)


    def set_camera_at_random_direction(self, distance: float, fuzz_d = .8, fuzz_x = .8, fuzz_z = .8):
        '''
        Look at target at random direction
        '''
        rot_x = random.random() * math.pi / 2
        rot_z = random.random() * 2 * math.pi

        self.set_camera_fuzzed(distance, rot_x, rot_z, fuzz_d, fuzz_x, fuzz_z)


class ObjectsSetup():
    '''
    Used for basic oject import, instantiation and distribution.
    '''
    def set_random_position(self, targets, min_dist = 2, max_dist = 5):
        pos_arr = []
        _range = max_dist - min_dist
        for t in targets:
            flag = False
            while not flag:
                flag = True
                x = random.random() * _range + min_dist
                y = random.random() * _range + min_dist
                z = 0       # 防止一些物体到处乱飞
                for pos in pos_arr:
                    dist = math.sqrt(
                        (x - pos.x) ** 2 + (y - pos.y) ** 2 + (z - pos.z) ** 2
                    )
                    if dist > min_dist:
                        flag = False
            t.location = Vector((x, y, z))
            pos_arr.append(t.location)

        return pos_arr

    def get_target_objects(self, collection_name = 'Objects'):
        '''
        '''
        return list(bpy.data.collections[collection_name].all_objects)


class Renderer():
    '''
    '''
    def set_output_path(self, path):
        bpy.context.scene.render.filepath = path


if __name__ == '__main__':
    setup = ObjectsSetup()
    objs = setup.get_target_objects()
    setup.set_random_position(objs)

