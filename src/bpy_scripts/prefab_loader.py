import os
import bpy
import config

from nefx.logger import error, log, info, warn
import config

TARGET_COL = 'target'
MATERIALS = []
LABELS = []


def get_background_col():
    background_col = bpy.data.collections.get('background')
    if background_col is None:
        background_col = bpy.data.collections.new('background')
        bpy.context.scene.collection.children.link(background_col)
    return background_col


def get_bpy_collection(name):
    '''bpy.data.collections.get(name)的便捷形式''' 
    res = bpy.data.collections.get(name)
    if res is None:
        warn(f'名字为{name}的collection不存在！')
    return res


def get_bpy_object(name):
    '''
    bpy.data.objects.get(name)的便捷形式
    '''
    res = bpy.data.objects.get(name)
    if res is None:
        print(f'名字为{name}的object不存在！')
    return res


def get_camera():
    camera_data = bpy.data.cameras.get('Camera')
    if camera_data is None:
        camera_data = bpy.data.cameras.new('Camera')
        camera_obj = bpy.data.objects.new("Camera", camera_data)
        camera_col = get_camera_col()
        camera_col.objects.link(camera_obj)

    camera_data.clip_start = .1
    camera_data.clip_end = 1e6

    return camera_data


def get_camera_col():
    camera_col = bpy.data.collections.get('camera')
    if camera_col is None:
        camera_col = bpy.data.collections.new('camera')
        bpy.context.scene.collection.children.link(camera_col)
    return camera_col


def get_focus():
    '''
    镜头组的焦点物体，设定LookAt和虚焦的时候使用
    '''
    focus = bpy.data.objects.get("focus")
    if focus is None:
        focus = bpy.data.objects.new('focus', None)
        camera_col = get_camera_col()
        camera_col.objects.link(focus)
    return focus


def get_instance_col():
    instance_col = bpy.data.collections.get('instance')
    if instance_col is None:
        instance_col = bpy.data.collections.new('instance')
        bpy.context.scene.collection.children.link(instance_col)
    return instance_col


def get_labels():
    return LABELS


def get_materials():
    if len(MATERIALS) == 0:
        load_materials()
    return MATERIALS


def get_sand_volume():
    dust_volume = bpy.data.objects.get('dust_volume')
    if dust_volume is None:
        dust_volume = load_sand_volume()
    return dust_volume


def get_target_col():
    '''
    复制源targets作为所有源模型集合的父集合
    '''
    target_col = bpy.data.collections.get(TARGET_COL)
    if target_col is None:
        bpy.ops.collection.create(name=TARGET_COL)
        target_col = bpy.data.collections.get(TARGET_COL)
        bpy.context.scene.collection.children.link(target_col)
    target_col.hide_render = True
    return target_col


def load_all(enable_sand_volume=True):
    log('prefab_loader 工作中...')
    load_background()
    load_materials()
    load_models()
    if enable_sand_volume:
        load_sand_volume()
    log('prefab_loader 任务完成! ')


def load_models():
    '''
    按照config.json文件加载model文件夹下的blend_file的资源
    每个路径下是一个物体名称的列表
    以.blend文件的名称建立集合
    这些集合将被挂载到targets集合之下, 并作为复制的源
    '''
    global LABELS
    model_paths = config.get_model_paths()
    target_col = get_target_col()
    count = 0
    for path in model_paths:
        full_path = f"{os.getcwd()}/blend_files/model/" + path
        if not os.path.exists(full_path):
            error(f'路径"{full_path}"不存在！')
            continue
        
        col_name = str.split(path, '.blend')[0]
        if len(col_name) == 0:
            col_name += 'default_name'
        collection = bpy.data.collections.new(col_name)
        target_col.children.link(collection)
        # 读取models.blend文件中的目标
        with bpy.data.libraries.load(full_path) as (data_from, data_to):
            # model_paths[path]是物体名称列表
            # data_to.collections.append
            for o_name in model_paths[path]:
                data_to.objects.append(o_name)
        for o_name in model_paths[path]:
            object = get_bpy_object(o_name)
            if object is not None:
                log(f'加载一个物体: {path}/{object}.obj')
                collection.objects.link(object)
                count += 1
                label = str.split(o_name, '.')[0]
                if len(label) == 0 or label in LABELS:
                    continue
                LABELS.append(label)
    info(f'models加载完成, 共计: {count} 模型, {len(LABELS)} 标签.')


def load_materials():
    '''
    加载material文件夹下的material目录
    '''
    global MATERIALS
    materials = config.get_material_paths()
    for mat_path in materials:
        f_mat_path = f"{os.getcwd()}/blend_files/material/" + mat_path
        if not os.path.exists(f_mat_path):
            error(f'路径"{f_mat_path}"不存在！')
            continue
        with bpy.data.libraries.load(f_mat_path) as (data_from, data_to):
            for mat_name in materials[mat_path]:
                data_to.materials.append(mat_name)
                MATERIALS.append(mat_name)
    info(f'materials加载完成: 共计: {len(MATERIALS)} 种材质.')


def load_background():
    '''
    包括材质集和平面
    '''
    backgrounds = config.get_background_paths()
    for path in backgrounds:
        f_path = f"{os.getcwd()}/blend_files/base/" + path
        if not os.path.exists(f_path):
            print(f'路径"{f_path}"不存在！')
            continue
        with bpy.data.libraries.load(f_path) as (data_from, data_to):
            for bg_name in backgrounds[path]:
                data_to.objects.append(bg_name)
        background = bpy.data.objects.get('background')
        background_col = get_background_col()
        background_col.objects.link(background)
    info(f'background加载完成。')


def load_sand_volume():
    ''''''
    dust = config.get_sand_volume_path()
    full_path = f"{os.getcwd()}/blend_files/base/" + dust
    if not os.path.exists(full_path):
        error(f'路径"{full_path}"不存在！')
        return
    with bpy.data.libraries.load(full_path) as (data_from, data_to):
        data_to.objects.append('dust_volume')
    dust_volume = bpy.data.objects.get('dust_volume')
    background_col = get_background_col()
    background_col.objects.link(dust_volume)


# TODO: 针对物体散布模块做针对性重构
def instantiate_all():
    instance_col = get_instance_col()
    # 清除全部的实例对象.
    for col in instance_col.children:
        bpy.data.collections.remove(col)
    for o in instance_col.all_objects:
        bpy.data.objects.remove(o)
    # 获得基因原体.
    target_col = bpy.data.collections.get('target')
    count = config.get_object_count()
    for tars in target_col.children:
        collection = bpy.data.collections.new(tars.name)
        instance_col.children.link(collection)
        LABELS.append(collection.name)
        for tar in tars.objects:
            for i in range(count):
                new = tar.copy()
                collection.objects.link(new)


if __name__ == "__main__":
    get_target_col()